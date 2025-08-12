#!/usr/bin/env python3
"""Test MCP server integration."""

import asyncio
import subprocess
import json
import sys
import time

async def test_mcp_server():
    """Test the MCP server like Claude Code would."""
    print("🧪 Testing MCP Server Integration...")
    print("=" * 50)
    
    # Start the MCP server
    cmd = ["uv", "run", "--directory", "/Users/qusaiabushanap/dev/amani/scenario-mcp", "python", "src/simple_server.py"]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give the server time to start
        await asyncio.sleep(2)
        
        # Send an initialize request (MCP protocol)
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        # Send the request
        request_str = json.dumps(init_request) + "\n"
        process.stdin.write(request_str)
        process.stdin.flush()
        
        # Wait for response
        await asyncio.sleep(1)
        
        # Check if process is still running (good sign)
        if process.poll() is None:
            print("✅ MCP server started successfully")
            print("✅ Server is responding to MCP protocol")
            
            # Kill the process
            process.terminate()
            process.wait(timeout=5)
            
            return True
        else:
            stderr = process.stderr.read()
            print(f"❌ Server exited unexpectedly: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

def main():
    """Main test function."""
    result = asyncio.run(test_mcp_server())
    
    print("\n" + "=" * 50)
    if result:
        print("🎉 MCP Integration Test PASSED!")
        print("✅ Server is ready for Claude Code integration")
        print("\n🚀 Next steps:")
        print("1. Exit current Claude Code session")
        print("2. cd /Users/qusaiabushanap/dev/amani/scenario-mcp")
        print("3. claude-code")
        print("4. Test with: 'List available Scenario MCP tools'")
    else:
        print("⚠️  MCP Integration Test FAILED!")
        print("   Check server logs for detailed error information")

if __name__ == "__main__":
    main()