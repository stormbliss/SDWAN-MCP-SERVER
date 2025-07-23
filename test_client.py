#!/usr/bin/env python3
"""
Test client for SD-WAN MCP Server
"""
import asyncio
import json
import subprocess
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test the MCP server functionality"""
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # First, test authentication
            print("Testing authentication...")
            try:
                auth_result = await session.call_tool("authenticate", {})
                print("Authentication result:")
                print(json.dumps(json.loads(auth_result.content[0].text), indent=2))
            except Exception as e:
                print(f"Error during authentication: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # Check session status
            print("Checking session status...")
            try:
                status_result = await session.call_tool("get_session_status", {})
                print("Session status:")
                print(json.dumps(json.loads(status_result.content[0].text), indent=2))
            except Exception as e:
                print(f"Error getting session status: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            print("\n" + "="*50 + "\n")
            
            # Test fabric devices
            print("Testing get_fabric_devices...")
            try:
                result = await session.call_tool("get_fabric_devices", {})
                print("Fabric devices result:")
                print(json.dumps(json.loads(result.content[0].text), indent=2))
            except Exception as e:
                print(f"Error getting fabric devices: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # Test device monitor
            print("Testing get_device_monitor...")
            try:
                result = await session.call_tool("get_device_monitor", {})
                print("Device monitor result:")
                print(json.dumps(json.loads(result.content[0].text), indent=2))
            except Exception as e:
                print(f"Error getting device monitor: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # Test BFD state with a device ID
            print("Testing get_bfd_state with device ID 200.0.1.1...")
            try:
                result = await session.call_tool("get_bfd_state", {"device_id": "200.0.1.1"})
                print("BFD state result:")
                print(json.dumps(json.loads(result.content[0].text), indent=2))
            except Exception as e:
                print(f"Error getting BFD state: {e}")
            
            print("\n" + "="*50 + "\n")
            
            # Test new enhanced tools
            print("Testing enhanced tools...")
            
            # Test device health summary
            print("Testing get_device_health_summary...")
            try:
                result = await session.call_tool("get_device_health_summary", {})
                print("Device health summary:")
                print(json.dumps(json.loads(result.content[0].text), indent=2)[:500] + "...")
            except Exception as e:
                print(f"Error getting device health summary: {e}")
            
            print("\n" + "-"*30 + "\n")
            
            # Test filtering devices
            print("Testing filter_devices_by_status (up)...")
            try:
                result = await session.call_tool("filter_devices_by_status", {"status": "up"})
                print("Filtered devices result:")
                print(json.dumps(json.loads(result.content[0].text), indent=2)[:500] + "...")
            except Exception as e:
                print(f"Error filtering devices: {e}")
            
            print("\n" + "-"*30 + "\n")
            
            # Test top interfaces
            print("Testing get_top_interfaces_by_traffic...")
            try:
                result = await session.call_tool("get_top_interfaces_by_traffic", {"limit": 5, "metric": "total_bytes"})
                print("Top interfaces result:")
                print(json.dumps(json.loads(result.content[0].text), indent=2)[:500] + "...")
            except Exception as e:
                print(f"Error getting top interfaces: {e}")
            
            print("\n" + "-"*30 + "\n")
            
            # Test network report
            print("Testing generate_network_report...")
            try:
                result = await session.call_tool("generate_network_report", {
                    "include_interfaces": True,
                    "include_bfd": True,
                    "include_tunnels": False
                })
                print("Network report result:")
                print(json.dumps(json.loads(result.content[0].text), indent=2)[:800] + "...")
            except Exception as e:
                print(f"Error generating network report: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
