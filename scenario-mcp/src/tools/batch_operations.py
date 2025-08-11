"""Batch operations MCP tools for efficient processing."""

import asyncio
import structlog
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from mcp.server.fastmcp import Context

from ..utils.response import ResponseHelper
from ..utils.validation import validate_request
from ..utils.async_utils import AsyncThrottler
from ..models.requests import BatchGenerationRequest, TextToImageRequest
from ..models.responses import BatchResult, GenerationJob
from ..scenario_client import ScenarioAPIClient
from ..exceptions import *

logger = structlog.get_logger(__name__)


def register_batch_tools(mcp):
    """Register batch processing tools."""
    
    @mcp.tool()
    async def scenario_batch_generate(
        ctx: Context,
        prompts: List[str],
        model_id: str,
        batch_settings: Optional[Dict[str, Any]] = None,
        max_concurrent: int = 5,
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """
        Execute batch text-to-image generation with Agent 4's prompt strategies.
        
        Perfect for Agent 4's batch generation workflows where they have
        multiple engineered prompts to process efficiently.
        
        Args:
            prompts: List of text prompts to generate (Agent 4's engineered prompts)
            model_id: Scenario model ID for all generations
            batch_settings: Shared settings for all generations
            max_concurrent: Maximum concurrent requests (1-10)
            wait_for_completion: Wait for all generations to complete
            
        Returns:
            Dict containing batch results and individual generation status
        """
        try:
            # Validate batch request
            request_data = {
                "prompts": prompts,
                "model_id": model_id,
                "batch_settings": batch_settings or {},
                "max_concurrent": max_concurrent
            }
            batch_request = validate_request(request_data, BatchGenerationRequest)
            
            logger.info(f"Starting batch generation: {len(prompts)} prompts with {model_id}")
            
            # Default settings
            default_settings = {
                "width": 1024,
                "height": 1024,
                "guidance": 3.5,
                "num_inference_steps": 28,
                "scheduler": "EulerAncestralDiscrete",
                "num_samples": 1
            }
            default_settings.update(batch_request.batch_settings)
            
            # Initialize throttling
            throttler = AsyncThrottler(
                max_concurrent=batch_request.max_concurrent,
                rate_limit=10.0
            )
            
            batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            batch_start_time = datetime.now()
            
            async with ScenarioAPIClient() as client:
                
                async def process_single_prompt(prompt_data):
                    """Process a single prompt in the batch."""
                    index, prompt = prompt_data
                    try:
                        logger.info(f"Processing batch item {index + 1}/{len(prompts)}: {prompt[:50]}...")
                        
                        # Create individual request
                        request_data = {
                            "prompt": prompt,
                            "model_id": model_id,
                            **default_settings
                        }
                        individual_request = validate_request(request_data, TextToImageRequest)
                        
                        # Submit generation
                        job = await client.text_to_image(individual_request)
                        
                        if wait_for_completion:
                            # Wait for completion
                            completed_job = await client.wait_for_completion(job.id, max_wait_time=300)
                            return {
                                "index": index,
                                "prompt": prompt,
                                "job_id": completed_job.id,
                                "status": completed_job.status.value,
                                "assets": [
                                    {
                                        "id": asset.id,
                                        "url": asset.url,
                                        "width": asset.width,
                                        "height": asset.height
                                    }
                                    for asset in completed_job.assets
                                ],
                                "credits_used": completed_job.credits_used,
                                "generation_time_seconds": (completed_job.completed_at - completed_job.created_at).total_seconds() if completed_job.completed_at else None
                            }
                        else:
                            # Return job info for monitoring
                            return {
                                "index": index,
                                "prompt": prompt,
                                "job_id": job.id,
                                "status": job.status.value,
                                "submitted_at": job.created_at.isoformat()
                            }
                    
                    except Exception as e:
                        logger.error(f"Failed to process prompt {index}: {str(e)}")
                        return {
                            "index": index,
                            "prompt": prompt,
                            "error": str(e),
                            "status": "failed"
                        }
                
                # Process batch with throttling
                prompt_operations = [(process_single_prompt, ((i, prompt),), {}) 
                                   for i, prompt in enumerate(prompts)]
                
                # Progress tracking
                progress_updates = []
                
                async def progress_callback(completed, total, error_info):
                    progress = (completed / total) * 100
                    progress_updates.append({
                        "completed": completed,
                        "total": total,
                        "progress_percent": progress,
                        "timestamp": datetime.now().isoformat()
                    })
                    logger.info(f"Batch progress: {completed}/{total} ({progress:.1f}%)")
                
                # Execute batch
                results = await throttler.execute_batch(prompt_operations, progress_callback)
                
                batch_end_time = datetime.now()
                
                # Analyze results
                successful_results = [r for r in results if r.get("success", True) and "error" not in r.get("result", {})]
                failed_results = [r for r in results if not r.get("success", True) or "error" in r.get("result", {})]
                
                # Extract actual results
                processed_results = []
                total_assets = 0
                total_credits = 0.0
                
                for result in results:
                    if result.get("success", True):
                        result_data = result.get("result", result)
                        processed_results.append(result_data)
                        
                        if "assets" in result_data:
                            total_assets += len(result_data.get("assets", []))
                        if "credits_used" in result_data:
                            total_credits += result_data.get("credits_used", 0)
                
                # Create batch summary
                batch_summary = {
                    "batch_id": batch_id,
                    "started_at": batch_start_time.isoformat(),
                    "completed_at": batch_end_time.isoformat(),
                    "total_time_seconds": (batch_end_time - batch_start_time).total_seconds(),
                    "total_prompts": len(prompts),
                    "successful_generations": len(successful_results),
                    "failed_generations": len(failed_results),
                    "success_rate_percent": (len(successful_results) / len(prompts)) * 100,
                    "total_assets_generated": total_assets,
                    "total_credits_used": total_credits,
                    "average_credits_per_prompt": total_credits / len(prompts) if prompts else 0,
                    "batch_settings": default_settings,
                    "progress_updates": progress_updates
                }
                
                if wait_for_completion:
                    message = f"Batch completed: {len(successful_results)}/{len(prompts)} successful ({batch_summary['success_rate_percent']:.1f}%)"
                else:
                    message = f"Batch submitted: {len(prompts)} generations started"
                
                return ResponseHelper.success(
                    message,
                    data={
                        "batch_summary": batch_summary,
                        "results": processed_results,
                        "model_used": model_id,
                        "throttling_settings": {
                            "max_concurrent": max_concurrent,
                            "rate_limit": 10.0
                        }
                    }
                )
        
        except ValidationError as e:
            return ResponseHelper.validation_error("batch_generation", str(e))
        except Exception as e:
            logger.exception("Error in scenario_batch_generate")
            return ResponseHelper.error(f"Batch generation failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_batch_monitor(
        ctx: Context,
        job_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Monitor status of multiple generation jobs.
        
        Perfect for Agent 4 to monitor batch operations progress.
        
        Args:
            job_ids: List of job IDs to monitor
            
        Returns:
            Dict containing status of all jobs
        """
        try:
            if not job_ids:
                return ResponseHelper.validation_error("job_ids", "At least one job ID is required")
            
            logger.info(f"Monitoring {len(job_ids)} jobs")
            
            async with ScenarioAPIClient() as client:
                
                async def check_single_job(job_id):
                    try:
                        job_status = await client.get_generation_status(job_id)
                        return {
                            "job_id": job_id,
                            "status": job_status.status.value,
                            "progress": job_status.progress,
                            "assets_count": len(job_status.assets),
                            "credits_used": job_status.credits_used,
                            "created_at": job_status.created_at.isoformat(),
                            "completed_at": job_status.completed_at.isoformat() if job_status.completed_at else None,
                            "error_message": job_status.error_message
                        }
                    except Exception as e:
                        return {
                            "job_id": job_id,
                            "status": "error",
                            "error": str(e)
                        }
                
                # Check all jobs concurrently
                tasks = [check_single_job(job_id) for job_id in job_ids]
                job_statuses = await asyncio.gather(*tasks)
                
                # Analyze batch status
                status_counts = {}
                completed_jobs = 0
                total_assets = 0
                total_credits = 0.0
                
                for job_status in job_statuses:
                    status = job_status.get("status", "unknown")
                    status_counts[status] = status_counts.get(status, 0) + 1
                    
                    if status == "completed":
                        completed_jobs += 1
                        total_assets += job_status.get("assets_count", 0)
                        total_credits += job_status.get("credits_used", 0)
                
                overall_progress = (completed_jobs / len(job_ids)) * 100
                
                return ResponseHelper.success(
                    f"Monitoring {len(job_ids)} jobs: {completed_jobs} completed ({overall_progress:.1f}%)",
                    data={
                        "total_jobs": len(job_ids),
                        "completed_jobs": completed_jobs,
                        "overall_progress_percent": overall_progress,
                        "status_breakdown": status_counts,
                        "total_assets_generated": total_assets,
                        "total_credits_used": total_credits,
                        "job_details": job_statuses,
                        "all_completed": completed_jobs == len(job_ids),
                        "has_failures": "failed" in status_counts or "error" in status_counts
                    }
                )
        
        except Exception as e:
            logger.exception("Error in scenario_batch_monitor")
            return ResponseHelper.error(f"Batch monitoring failed: {str(e)}")
    
    @mcp.tool()
    async def scenario_agent4_batch_execute(
        ctx: Context,
        agent4_batch_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute Agent 4's complete batch generation plan.
        
        This is the ultimate tool for Agent 4 - takes their complete
        batch strategy and executes it with full automation.
        
        Args:
            agent4_batch_plan: Agent 4's complete generation plan containing:
                - engineered_prompts: List of optimized prompts
                - selected_model: Chosen model ID  
                - generation_settings: Optimized settings
                - organization_config: How to organize results
                - quality_criteria: Quality checking parameters
                
        Returns:
            Dict containing complete execution results ready for Agent 4's next steps
        """
        try:
            # Validate Agent 4's plan
            required_fields = ["engineered_prompts", "selected_model"]
            for field in required_fields:
                if field not in agent4_batch_plan:
                    return ResponseHelper.validation_error(
                        "agent4_batch_plan", 
                        f"Required field '{field}' missing from Agent 4's plan"
                    )
            
            engineered_prompts = agent4_batch_plan["engineered_prompts"]
            selected_model = agent4_batch_plan["selected_model"]
            generation_settings = agent4_batch_plan.get("generation_settings", {})
            organization_config = agent4_batch_plan.get("organization_config", {})
            
            logger.info(f"🎯 Executing Agent 4's batch plan: {len(engineered_prompts)} prompts with {selected_model}")
            
            # Execute the batch generation using Agent 4's specifications
            batch_result = await scenario_batch_generate(
                ctx,
                prompts=engineered_prompts,
                model_id=selected_model,
                batch_settings=generation_settings,
                max_concurrent=organization_config.get("max_concurrent", 5),
                wait_for_completion=True
            )
            
            if not batch_result.get("success"):
                return batch_result  # Return the error from batch generation
            
            # Agent 4's results are ready
            batch_data = batch_result["data"]
            results = batch_data["results"]
            
            # Organize results according to Agent 4's preferences
            organized_results = {
                "agent4_execution_summary": {
                    "execution_timestamp": datetime.now().isoformat(),
                    "agent4_plan_executed": True,
                    "original_plan": agent4_batch_plan,
                    "execution_stats": batch_data["batch_summary"]
                },
                "generated_assets": [],
                "asset_organization": organization_config,
                "quality_analysis": {
                    "total_generated": len([r for r in results if r.get("status") == "completed"]),
                    "failed_generations": len([r for r in results if r.get("status") == "failed"]),
                    "quality_score": "pending_agent4_review"
                },
                "ready_for_next_step": True
            }
            
            # Process each result for Agent 4's next workflow step
            for result in results:
                if result.get("status") == "completed" and "assets" in result:
                    for asset in result["assets"]:
                        organized_results["generated_assets"].append({
                            "asset_id": asset["id"],
                            "download_url": asset["url"],
                            "source_prompt": result["prompt"],
                            "prompt_index": result.get("index", 0),
                            "dimensions": f"{asset.get('width', 'unknown')}x{asset.get('height', 'unknown')}",
                            "ready_for_download": True,
                            "agent4_metadata": {
                                "generation_job_id": result.get("job_id"),
                                "credits_used": result.get("credits_used"),
                                "generation_time": result.get("generation_time_seconds")
                            }
                        })
            
            return ResponseHelper.success(
                f"🎯 Agent 4's batch plan executed successfully! Generated {len(organized_results['generated_assets'])} assets ready for next workflow step.",
                data=organized_results
            )
        
        except Exception as e:
            logger.exception("Error in scenario_agent4_batch_execute")
            return ResponseHelper.error(f"Agent 4's batch execution failed: {str(e)}")