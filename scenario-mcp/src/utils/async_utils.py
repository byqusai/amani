"""Async utilities for rate limiting and throttling."""

import asyncio
from typing import List, Any, Callable, Optional, Dict
import structlog
from asyncio_throttle import Throttler
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import aiohttp

from ..exceptions import RateLimitError, ConnectionError as ScenarioConnectionError

logger = structlog.get_logger(__name__)


class AsyncThrottler:
    """Manages async operation throttling and rate limiting."""
    
    def __init__(self, max_concurrent: int = 5, rate_limit: float = 10.0):
        self.max_concurrent = max_concurrent
        self.throttler = Throttler(rate_limit=rate_limit)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._active_tasks: Dict[str, asyncio.Task] = {}
    
    async def execute_with_throttle(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute operation with throttling."""
        async with self.semaphore:
            async with self.throttler:
                return await operation(*args, **kwargs)
    
    async def execute_batch(self, operations: List[tuple], 
                          progress_callback: Optional[Callable] = None) -> List[Any]:
        """Execute batch of operations with throttling."""
        results = []
        completed = 0
        total = len(operations)
        
        async def execute_single(op_data):
            nonlocal completed
            try:
                operation, args, kwargs = op_data
                result = await self.execute_with_throttle(operation, *args, **kwargs)
                completed += 1
                
                if progress_callback:
                    await progress_callback(completed, total, None)
                
                return {'success': True, 'result': result}
            
            except Exception as e:
                completed += 1
                error_info = {'success': False, 'error': str(e), 'type': type(e).__name__}
                
                if progress_callback:
                    await progress_callback(completed, total, error_info)
                
                return error_info
        
        # Execute all operations concurrently with throttling
        tasks = [execute_single(op) for op in operations]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        return results
    
    def track_task(self, task_id: str, task: asyncio.Task):
        """Track a task for monitoring."""
        self._active_tasks[task_id] = task
    
    def get_active_tasks(self) -> Dict[str, str]:
        """Get status of active tasks."""
        status = {}
        for task_id, task in list(self._active_tasks.items()):
            if task.done():
                del self._active_tasks[task_id]
            else:
                status[task_id] = 'running'
        return status
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a tracked task."""
        if task_id in self._active_tasks:
            task = self._active_tasks[task_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self._active_tasks[task_id]
            return True
        return False


class RetryableHTTPClient:
    """HTTP client with intelligent retry logic."""
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
    )
    async def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        """Make HTTP request with retry logic."""
        try:
            async with self.session.request(method, url, **kwargs) as response:
                # Handle rate limiting
                if response.status == 429:
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        try:
                            retry_after = int(retry_after)
                        except ValueError:
                            retry_after = 60  # Default to 1 minute
                    else:
                        retry_after = 60
                    
                    logger.warning(f"Rate limited, retrying after {retry_after} seconds")
                    raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
                
                # Handle other HTTP errors
                if response.status >= 400:
                    error_data = None
                    try:
                        error_data = await response.json()
                    except:
                        error_data = await response.text()
                    
                    if response.status == 401:
                        raise ScenarioConnectionError(f"Authentication failed: {error_data}")
                    elif response.status == 403:
                        raise ScenarioConnectionError(f"Access forbidden: {error_data}")
                    elif response.status >= 500:
                        raise ScenarioConnectionError(f"Server error {response.status}: {error_data}")
                    else:
                        raise ScenarioConnectionError(f"HTTP {response.status}: {error_data}")
                
                return response
        
        except aiohttp.ClientError as e:
            logger.error(f"HTTP client error: {str(e)}")
            raise ScenarioConnectionError(f"Connection failed: {str(e)}")
        except asyncio.TimeoutError:
            logger.error("HTTP request timed out")
            raise ScenarioConnectionError("Request timed out")
    
    async def get_json(self, url: str, **kwargs) -> Dict[str, Any]:
        """GET request returning JSON."""
        response = await self.request('GET', url, **kwargs)
        return await response.json()
    
    async def post_json(self, url: str, json_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """POST request with JSON payload returning JSON."""
        response = await self.request('POST', url, json=json_data, **kwargs)
        return await response.json()


async def poll_until_complete(check_function: Callable, 
                            check_interval: float = 2.0,
                            max_attempts: int = 150) -> Any:
    """Poll a function until it returns a completed status."""
    for attempt in range(max_attempts):
        try:
            result = await check_function()
            
            # Assume function returns dict with 'status' field
            if isinstance(result, dict):
                status = result.get('status', '').lower()
                if status in ['completed', 'success', 'done']:
                    return result
                elif status in ['failed', 'error', 'cancelled']:
                    raise Exception(f"Operation failed with status: {status}")
            
            # Wait before next check
            await asyncio.sleep(check_interval)
            
            # Increase interval slightly to reduce API load
            if attempt % 10 == 9:  # Every 10 attempts
                check_interval = min(check_interval * 1.2, 30.0)  # Cap at 30 seconds
        
        except Exception as e:
            logger.error(f"Error during polling attempt {attempt + 1}: {str(e)}")
            if attempt < max_attempts - 1:
                await asyncio.sleep(check_interval)
            else:
                raise
    
    raise TimeoutError(f"Operation did not complete within {max_attempts} attempts")


async def batch_download_assets(download_functions: List[Callable],
                              max_concurrent: int = 5,
                              progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
    """Download multiple assets concurrently."""
    throttler = AsyncThrottler(max_concurrent=max_concurrent, rate_limit=10.0)
    
    async def progress_wrapper(completed: int, total: int, error: Optional[Dict]):
        if progress_callback:
            percentage = (completed / total) * 100
            await progress_callback(completed, total, percentage, error)
    
    # Convert functions to operation tuples
    operations = [(func, (), {}) for func in download_functions]
    
    results = await throttler.execute_batch(operations, progress_wrapper)
    return results