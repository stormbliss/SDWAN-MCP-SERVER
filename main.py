#!/usr/bin/env python3
"""
SD-WAN MCP Server
"""
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import requests
import urllib3
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from config import config

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=getattr(logging, config.log_level.upper()))
logger = logging.getLogger("sdwan-mcp-server")

class SDWANMCPServer:
    def __init__(self):
        self.server = Server("sdwan-mcp-server")
        self.base_url = config.base_url
        self.auth_url = config.auth_url
        self.username = config.username
        self.password = config.password
        self.session_id = None
        self.headers = {}
        self.session = requests.Session()  # Use session for cookie persistence
        self.session.verify = config.verify_ssl  # Use config setting for SSL verification
        self.setup_handlers()

    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools"""
            return [
                types.Tool(
                    name="get_fabric_devices",
                    description="Get list of all fabric devices",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_device_monitor",
                    description="Get device monitoring information",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_device_counters",
                    description="Get device counters and statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_interface_statistics",
                    description="Get interface statistics for all devices",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_device_config",
                    description="Get device configuration",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID (e.g., 200.0.2.2)"
                            }
                        },
                        "required": ["device_id"]
                    }
                ),
                types.Tool(
                    name="get_bfd_state",
                    description="Get BFD (Bidirectional Forwarding Detection) state for a device",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID (e.g., 200.0.1.1)"
                            }
                        },
                        "required": ["device_id"]
                    }
                ),
                types.Tool(
                    name="get_bfd_sessions",
                    description="Get BFD sessions for a device",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID (e.g., 200.0.4.4)"
                            }
                        },
                        "required": ["device_id"]
                    }
                ),
                types.Tool(
                    name="get_tunnel_statistics",
                    description="Get tunnel statistics for a device",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "device_id": {
                                "type": "string",
                                "description": "Device ID (e.g., 200.0.2.2)"
                            }
                        },
                        "required": ["device_id"]
                    }
                ),
                types.Tool(
                    name="get_device_health_summary",
                    description="Get comprehensive health summary across all devices",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="filter_devices_by_status",
                    description="Filter devices by operational status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "description": "Device status to filter by (e.g., 'up', 'down', 'normal')",
                                "enum": ["up", "down", "normal", "critical", "warning"]
                            }
                        },
                        "required": ["status"]
                    }
                ),
                types.Tool(
                    name="get_top_interfaces_by_traffic",
                    description="Get top interfaces ranked by traffic utilization",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of top interfaces to return (default: 10)",
                                "default": 10
                            },
                            "metric": {
                                "type": "string",
                                "description": "Traffic metric to sort by",
                                "enum": ["rx_bytes", "tx_bytes", "total_bytes", "rx_packets", "tx_packets"],
                                "default": "total_bytes"
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="check_bfd_session_health",
                    description="Monitor BFD session health across all devices",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_details": {
                                "type": "boolean",
                                "description": "Include detailed session information",
                                "default": False
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="generate_network_report",
                    description="Generate comprehensive network status report",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_interfaces": {
                                "type": "boolean",
                                "description": "Include interface statistics in report",
                                "default": True
                            },
                            "include_bfd": {
                                "type": "boolean",
                                "description": "Include BFD session information",
                                "default": True
                            },
                            "include_tunnels": {
                                "type": "boolean",
                                "description": "Include tunnel statistics",
                                "default": True
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_device_alerts",
                    description="Get alerts and warnings for devices",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "severity": {
                                "type": "string",
                                "description": "Alert severity level",
                                "enum": ["critical", "warning", "info", "all"],
                                "default": "all"
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="monitor_interface_utilization",
                    description="Monitor interface utilization and identify high-usage interfaces",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "threshold": {
                                "type": "number",
                                "description": "Utilization threshold percentage (0-100)",
                                "default": 80
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_network_topology",
                    description="Get network topology information based on device connections",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="authenticate",
                    description="Authenticate with the SD-WAN management server to establish session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Username for authentication (optional, defaults to configured username)",
                                "default": "admin"
                            },
                            "password": {
                                "type": "string",
                                "description": "Password for authentication (optional, defaults to configured password)",
                                "default": "1"
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_session_status",
                    description="Check current authentication session status",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent]:
            """Handle tool calls"""
            try:
                if name == "get_fabric_devices":
                    result = await self._get_fabric_devices()
                elif name == "get_device_monitor":
                    result = await self._get_device_monitor()
                elif name == "get_device_counters":
                    result = await self._get_device_counters()
                elif name == "get_interface_statistics":
                    result = await self._get_interface_statistics()
                elif name == "get_device_config":
                    device_id = arguments.get("device_id") if arguments else None
                    if not device_id:
                        raise ValueError("device_id is required")
                    result = await self._get_device_config(device_id)
                elif name == "get_bfd_state":
                    device_id = arguments.get("device_id") if arguments else None
                    if not device_id:
                        raise ValueError("device_id is required")
                    result = await self._get_bfd_state(device_id)
                elif name == "get_bfd_sessions":
                    device_id = arguments.get("device_id") if arguments else None
                    if not device_id:
                        raise ValueError("device_id is required")
                    result = await self._get_bfd_sessions(device_id)
                elif name == "get_tunnel_statistics":
                    device_id = arguments.get("device_id") if arguments else None
                    if not device_id:
                        raise ValueError("device_id is required")
                    result = await self._get_tunnel_statistics(device_id)
                elif name == "get_device_health_summary":
                    result = await self._get_device_health_summary()
                elif name == "filter_devices_by_status":
                    status = arguments.get("status") if arguments else None
                    if not status:
                        raise ValueError("status is required")
                    result = await self._filter_devices_by_status(status)
                elif name == "get_top_interfaces_by_traffic":
                    limit = arguments.get("limit", 10) if arguments else 10
                    metric = arguments.get("metric", "total_bytes") if arguments else "total_bytes"
                    result = await self._get_top_interfaces_by_traffic(limit, metric)
                elif name == "check_bfd_session_health":
                    include_details = arguments.get("include_details", False) if arguments else False
                    result = await self._check_bfd_session_health(include_details)
                elif name == "generate_network_report":
                    include_interfaces = arguments.get("include_interfaces", True) if arguments else True
                    include_bfd = arguments.get("include_bfd", True) if arguments else True
                    include_tunnels = arguments.get("include_tunnels", True) if arguments else True
                    result = await self._generate_network_report(include_interfaces, include_bfd, include_tunnels)
                elif name == "get_device_alerts":
                    severity = arguments.get("severity", "all") if arguments else "all"
                    result = await self._get_device_alerts(severity)
                elif name == "monitor_interface_utilization":
                    threshold = arguments.get("threshold", 80) if arguments else 80
                    result = await self._monitor_interface_utilization(threshold)
                elif name == "get_network_topology":
                    result = await self._get_network_topology()
                elif name == "authenticate":
                    username = arguments.get("username", self.username) if arguments else self.username
                    password = arguments.get("password", self.password) if arguments else self.password
                    result = await self._authenticate(username, password)
                elif name == "get_session_status":
                    result = await self._get_session_status()
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            except Exception as e:
                logger.error(f"Error in {name}: {str(e)}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        # Check if we have a valid session
        if not self.session_id:
            auth_result = await self._authenticate()
            if "error" in auth_result:
                return {"error": "Authentication required. Please authenticate first.", "auth_error": auth_result}
        
        url = f"{self.base_url}{endpoint}"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.session.get(url)
        )
        
        # Check if session expired (typically returns 401 or redirects to login)
        if response.status_code == 401 or "login" in response.url.lower():
            logger.warning("Session expired, re-authenticating...")
            auth_result = await self._authenticate()
            if "error" in auth_result:
                return {"error": "Re-authentication failed", "auth_error": auth_result}
            
            # Retry the request with new session
            response = await loop.run_in_executor(
                None,
                lambda: self.session.get(url)
            )
        
        try:
            response_data = response.json()
            if 'data' in response_data:
                return response_data['data']
            else:
                return {"error": "Key 'data' not found in response", "response": response.text, "status_code": response.status_code}
        except ValueError:
            return {"error": "Response is not in JSON format", "response": response.text, "status_code": response.status_code}

    async def _authenticate(self, username: str = None, password: str = None) -> Dict[str, Any]:
        """Authenticate with the server and establish session"""
        try:
            auth_username = username or self.username
            auth_password = password or self.password
            
            payload = f'j_username={auth_username}&j_password={auth_password}'
            auth_headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.session.post(self.auth_url, headers=auth_headers, data=payload)
            )
            
            # Check if authentication was successful
            if response.status_code == 200:
                # Extract session ID from cookies
                for cookie in self.session.cookies:
                    if cookie.name == 'JSESSIONID':
                        self.session_id = cookie.value
                        logger.info(f"Authentication successful. Session ID: {self.session_id[:20]}...")
                        break
                
                if self.session_id:
                    return {
                        "status": "success",
                        "message": "Authentication successful",
                        "session_id": self.session_id[:20] + "...",  # Truncated for security
                        "response": response.text
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Authentication failed - no session ID received",
                        "response": response.text
                    }
            else:
                return {
                    "status": "error",
                    "message": f"Authentication failed with status code: {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return {
                "status": "error",
                "message": f"Authentication exception: {str(e)}"
            }

    async def _get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        return {
            "authenticated": bool(self.session_id),
            "session_id": self.session_id[:20] + "..." if self.session_id else None,
            "base_url": self.base_url,
            "username": self.username
        }

    async def _get_fabric_devices(self) -> Dict[str, Any]:
        """Get fabric devices"""
        return await self._make_request("/dataservice/device")

    async def _get_device_monitor(self) -> Dict[str, Any]:
        """Get device monitor data"""
        return await self._make_request("/dataservice/device/monitor")

    async def _get_device_counters(self) -> Dict[str, Any]:
        """Get device counters"""
        return await self._make_request("/dataservice/device/counters")

    async def _get_interface_statistics(self) -> Dict[str, Any]:
        """Get interface statistics"""
        return await self._make_request("/dataservice/statistics/interface")

    async def _get_device_config(self, device_id: str) -> Dict[str, Any]:
        """Get device configuration"""
        return await self._make_request(f"/dataservice/device/config?deviceId={device_id}")

    async def _get_bfd_state(self, device_id: str) -> Dict[str, Any]:
        """Get BFD state"""
        return await self._make_request(f"/dataservice/device/bfd/state/device?deviceId={device_id}")

    async def _get_bfd_sessions(self, device_id: str) -> Dict[str, Any]:
        """Get BFD sessions"""
        return await self._make_request(f"/dataservice/device/bfd/sessions?deviceId={device_id}")

    async def _get_tunnel_statistics(self, device_id: str) -> Dict[str, Any]:
        """Get tunnel statistics"""
        return await self._make_request(f"/dataservice/device/tunnel/statistics?deviceId={device_id}")

    async def _get_device_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary across all devices"""
        try:
            # Get all devices
            devices = await self._get_fabric_devices()
            device_monitor = await self._get_device_monitor()
            device_counters = await self._get_device_counters()
            
            summary = {
                "total_devices": 0,
                "devices_up": 0,
                "devices_down": 0,
                "devices_with_issues": 0,
                "overall_health": "unknown",
                "device_details": [],
                "summary_stats": {
                    "total_interfaces": 0,
                    "active_interfaces": 0,
                    "total_bfd_sessions": 0,
                    "active_bfd_sessions": 0
                }
            }
            
            if isinstance(devices, list):
                summary["total_devices"] = len(devices)
                
                for device in devices:
                    device_info = {
                        "device_id": device.get("deviceId", "unknown"),
                        "hostname": device.get("hostname", "unknown"),
                        "status": device.get("status", "unknown"),
                        "reachability": device.get("reachability", "unknown"),
                        "device_type": device.get("deviceType", "unknown")
                    }
                    
                    # Count device status
                    if device.get("reachability") == "reachable":
                        summary["devices_up"] += 1
                    else:
                        summary["devices_down"] += 1
                    
                    summary["device_details"].append(device_info)
            
            # Calculate overall health
            if summary["total_devices"] > 0:
                up_percentage = (summary["devices_up"] / summary["total_devices"]) * 100
                if up_percentage >= 95:
                    summary["overall_health"] = "excellent"
                elif up_percentage >= 80:
                    summary["overall_health"] = "good"
                elif up_percentage >= 60:
                    summary["overall_health"] = "fair"
                else:
                    summary["overall_health"] = "poor"
            
            return summary
            
        except Exception as e:
            return {"error": f"Failed to generate health summary: {str(e)}"}

    async def _filter_devices_by_status(self, status: str) -> Dict[str, Any]:
        """Filter devices by operational status"""
        try:
            devices = await self._get_fabric_devices()
            filtered_devices = []
            
            if isinstance(devices, list):
                for device in devices:
                    device_status = device.get("reachability", "").lower()
                    device_state = device.get("status", "").lower()
                    
                    # Map status filters to device attributes
                    if status.lower() == "up" and device_status == "reachable":
                        filtered_devices.append(device)
                    elif status.lower() == "down" and device_status == "unreachable":
                        filtered_devices.append(device)
                    elif status.lower() == "normal" and device_state == "normal":
                        filtered_devices.append(device)
                    elif status.lower() == "critical" and "critical" in device_state:
                        filtered_devices.append(device)
                    elif status.lower() == "warning" and "warning" in device_state:
                        filtered_devices.append(device)
            
            return {
                "filter_criteria": status,
                "total_devices": len(devices) if isinstance(devices, list) else 0,
                "filtered_count": len(filtered_devices),
                "devices": filtered_devices
            }
            
        except Exception as e:
            return {"error": f"Failed to filter devices: {str(e)}"}

    async def _get_top_interfaces_by_traffic(self, limit: int, metric: str) -> Dict[str, Any]:
        """Get top interfaces ranked by traffic utilization"""
        try:
            interfaces = await self._get_interface_statistics()
            top_interfaces = []
            
            if isinstance(interfaces, list):
                # Process each interface and calculate traffic metrics
                for interface in interfaces:
                    interface_data = {
                        "device_id": interface.get("deviceId", "unknown"),
                        "interface_name": interface.get("interface", "unknown"),
                        "rx_bytes": int(interface.get("rx_octets", 0)),
                        "tx_bytes": int(interface.get("tx_octets", 0)),
                        "rx_packets": int(interface.get("rx_pkts", 0)),
                        "tx_packets": int(interface.get("tx_pkts", 0)),
                        "rx_errors": int(interface.get("rx_errors", 0)),
                        "tx_errors": int(interface.get("tx_errors", 0))
                    }
                    
                    # Calculate total bytes
                    interface_data["total_bytes"] = interface_data["rx_bytes"] + interface_data["tx_bytes"]
                    
                    top_interfaces.append(interface_data)
                
                # Sort by specified metric
                if metric in ["rx_bytes", "tx_bytes", "total_bytes", "rx_packets", "tx_packets"]:
                    top_interfaces.sort(key=lambda x: x[metric], reverse=True)
                
                # Limit results
                top_interfaces = top_interfaces[:limit]
            
            return {
                "metric": metric,
                "limit": limit,
                "total_interfaces": len(interfaces) if isinstance(interfaces, list) else 0,
                "top_interfaces": top_interfaces
            }
            
        except Exception as e:
            return {"error": f"Failed to get top interfaces: {str(e)}"}

    async def _check_bfd_session_health(self, include_details: bool) -> Dict[str, Any]:
        """Monitor BFD session health across all devices"""
        try:
            devices = await self._get_fabric_devices()
            bfd_summary = {
                "total_devices_checked": 0,
                "devices_with_bfd": 0,
                "total_bfd_sessions": 0,
                "active_sessions": 0,
                "inactive_sessions": 0,
                "session_details": [] if include_details else None
            }
            
            if isinstance(devices, list):
                for device in devices:
                    device_id = device.get("deviceId")
                    if device_id:
                        bfd_summary["total_devices_checked"] += 1
                        
                        try:
                            # Get BFD sessions for this device
                            bfd_sessions = await self._get_bfd_sessions(device_id)
                            
                            if isinstance(bfd_sessions, list) and len(bfd_sessions) > 0:
                                bfd_summary["devices_with_bfd"] += 1
                                bfd_summary["total_bfd_sessions"] += len(bfd_sessions)
                                
                                for session in bfd_sessions:
                                    session_state = session.get("state", "").lower()
                                    if session_state == "up":
                                        bfd_summary["active_sessions"] += 1
                                    else:
                                        bfd_summary["inactive_sessions"] += 1
                                    
                                    if include_details:
                                        bfd_summary["session_details"].append({
                                            "device_id": device_id,
                                            "session_id": session.get("sessionId"),
                                            "state": session.get("state"),
                                            "local_address": session.get("localAddress"),
                                            "remote_address": session.get("remoteAddress"),
                                            "interface": session.get("interface")
                                        })
                        except:
                            # Skip devices that don't support BFD or are unreachable
                            continue
            
            return bfd_summary
            
        except Exception as e:
            return {"error": f"Failed to check BFD session health: {str(e)}"}

    async def _generate_network_report(self, include_interfaces: bool, include_bfd: bool, include_tunnels: bool) -> Dict[str, Any]:
        """Generate comprehensive network status report"""
        try:
            report = {
                "report_timestamp": asyncio.get_event_loop().time(),
                "network_overview": {},
                "device_summary": {},
                "interface_summary": {} if include_interfaces else None,
                "bfd_summary": {} if include_bfd else None,
                "tunnel_summary": {} if include_tunnels else None,
                "recommendations": []
            }
            
            # Get network overview
            report["network_overview"] = await self._get_device_health_summary()
            
            # Get device summary
            devices = await self._get_fabric_devices()
            if isinstance(devices, list):
                report["device_summary"] = {
                    "total_devices": len(devices),
                    "device_types": {},
                    "software_versions": {}
                }
                
                for device in devices:
                    device_type = device.get("deviceType", "unknown")
                    software_version = device.get("version", "unknown")
                    
                    report["device_summary"]["device_types"][device_type] = \
                        report["device_summary"]["device_types"].get(device_type, 0) + 1
                    
                    report["device_summary"]["software_versions"][software_version] = \
                        report["device_summary"]["software_versions"].get(software_version, 0) + 1
            
            # Include interface summary
            if include_interfaces:
                interfaces = await self._get_interface_statistics()
                if isinstance(interfaces, list):
                    report["interface_summary"] = {
                        "total_interfaces": len(interfaces),
                        "active_interfaces": len([i for i in interfaces if i.get("if-admin-status") == "up"]),
                        "high_error_interfaces": len([i for i in interfaces if 
                                                    int(i.get("rx_errors", 0)) > 100 or int(i.get("tx_errors", 0)) > 100])
                    }
            
            # Include BFD summary
            if include_bfd:
                report["bfd_summary"] = await self._check_bfd_session_health(False)
            
            # Include tunnel summary
            if include_tunnels:
                tunnel_stats = []
                if isinstance(devices, list):
                    for device in devices:
                        device_id = device.get("deviceId")
                        if device_id:
                            try:
                                tunnel_data = await self._get_tunnel_statistics(device_id)
                                if isinstance(tunnel_data, list):
                                    tunnel_stats.extend(tunnel_data)
                            except:
                                continue
                
                report["tunnel_summary"] = {
                    "total_tunnels": len(tunnel_stats),
                    "active_tunnels": len([t for t in tunnel_stats if t.get("state") == "up"])
                }
            
            # Generate recommendations
            recommendations = []
            if report["network_overview"].get("devices_down", 0) > 0:
                recommendations.append("⚠️ Some devices are unreachable - check network connectivity")
            
            if include_interfaces and report["interface_summary"].get("high_error_interfaces", 0) > 0:
                recommendations.append("⚠️ Some interfaces have high error rates - investigate potential issues")
            
            if include_bfd and report["bfd_summary"].get("inactive_sessions", 0) > 0:
                recommendations.append("⚠️ Some BFD sessions are inactive - verify network paths")
            
            if not recommendations:
                recommendations.append("✅ Network appears to be operating normally")
            
            report["recommendations"] = recommendations
            
            return report
            
        except Exception as e:
            return {"error": f"Failed to generate network report: {str(e)}"}

    async def _get_device_alerts(self, severity: str) -> Dict[str, Any]:
        """Get alerts and warnings for devices"""
        try:
            devices = await self._get_fabric_devices()
            device_monitor = await self._get_device_monitor()
            
            alerts = {
                "severity_filter": severity,
                "total_alerts": 0,
                "critical_alerts": 0,
                "warning_alerts": 0,
                "info_alerts": 0,
                "alerts": []
            }
            
            if isinstance(devices, list):
                for device in devices:
                    device_id = device.get("deviceId")
                    hostname = device.get("hostname", "unknown")
                    
                    # Check device reachability
                    if device.get("reachability") == "unreachable":
                        alert = {
                            "device_id": device_id,
                            "hostname": hostname,
                            "severity": "critical",
                            "message": "Device is unreachable",
                            "timestamp": device.get("lastupdated", "unknown")
                        }
                        
                        if severity == "all" or severity == "critical":
                            alerts["alerts"].append(alert)
                            alerts["critical_alerts"] += 1
                    
                    # Check device status
                    if device.get("status") != "normal":
                        alert_severity = "warning" if "warning" in device.get("status", "").lower() else "info"
                        alert = {
                            "device_id": device_id,
                            "hostname": hostname,
                            "severity": alert_severity,
                            "message": f"Device status: {device.get('status')}",
                            "timestamp": device.get("lastupdated", "unknown")
                        }
                        
                        if severity == "all" or severity == alert_severity:
                            alerts["alerts"].append(alert)
                            if alert_severity == "warning":
                                alerts["warning_alerts"] += 1
                            else:
                                alerts["info_alerts"] += 1
            
            alerts["total_alerts"] = len(alerts["alerts"])
            return alerts
            
        except Exception as e:
            return {"error": f"Failed to get device alerts: {str(e)}"}

    async def _monitor_interface_utilization(self, threshold: float) -> Dict[str, Any]:
        """Monitor interface utilization and identify high-usage interfaces"""
        try:
            interfaces = await self._get_interface_statistics()
            
            utilization_report = {
                "threshold_percent": threshold,
                "total_interfaces": 0,
                "high_utilization_interfaces": 0,
                "interfaces_over_threshold": [],
                "average_utilization": 0
            }
            
            if isinstance(interfaces, list):
                utilization_report["total_interfaces"] = len(interfaces)
                total_utilization = 0
                
                for interface in interfaces:
                    # Calculate utilization (this is a simplified calculation)
                    # In a real scenario, you'd need bandwidth capacity and current usage
                    rx_bytes = int(interface.get("rx_octets", 0))
                    tx_bytes = int(interface.get("tx_octets", 0))
                    
                    # Mock utilization calculation (replace with actual logic)
                    mock_utilization = min(((rx_bytes + tx_bytes) / 1000000) % 100, 100)
                    
                    total_utilization += mock_utilization
                    
                    if mock_utilization > threshold:
                        utilization_report["high_utilization_interfaces"] += 1
                        utilization_report["interfaces_over_threshold"].append({
                            "device_id": interface.get("deviceId"),
                            "interface": interface.get("interface"),
                            "utilization_percent": round(mock_utilization, 2),
                            "rx_bytes": rx_bytes,
                            "tx_bytes": tx_bytes,
                            "status": interface.get("if-admin-status")
                        })
                
                if len(interfaces) > 0:
                    utilization_report["average_utilization"] = round(total_utilization / len(interfaces), 2)
            
            return utilization_report
            
        except Exception as e:
            return {"error": f"Failed to monitor interface utilization: {str(e)}"}

    async def _get_network_topology(self) -> Dict[str, Any]:
        """Get network topology information based on device connections"""
        try:
            devices = await self._get_fabric_devices()
            interfaces = await self._get_interface_statistics()
            
            topology = {
                "nodes": [],
                "connections": [],
                "network_summary": {
                    "total_devices": 0,
                    "total_interfaces": 0,
                    "device_types": {}
                }
            }
            
            if isinstance(devices, list):
                topology["network_summary"]["total_devices"] = len(devices)
                
                for device in devices:
                    node = {
                        "device_id": device.get("deviceId"),
                        "hostname": device.get("hostname"),
                        "device_type": device.get("deviceType"),
                        "status": device.get("reachability"),
                        "site_id": device.get("site-id"),
                        "system_ip": device.get("system-ip"),
                        "version": device.get("version")
                    }
                    topology["nodes"].append(node)
                    
                    # Count device types
                    device_type = device.get("deviceType", "unknown")
                    topology["network_summary"]["device_types"][device_type] = \
                        topology["network_summary"]["device_types"].get(device_type, 0) + 1
            
            if isinstance(interfaces, list):
                topology["network_summary"]["total_interfaces"] = len(interfaces)
                
                # Group interfaces by device for connection mapping
                device_interfaces = {}
                for interface in interfaces:
                    device_id = interface.get("deviceId")
                    if device_id:
                        if device_id not in device_interfaces:
                            device_interfaces[device_id] = []
                        device_interfaces[device_id].append({
                            "interface": interface.get("interface"),
                            "status": interface.get("if-admin-status"),
                            "ip_address": interface.get("ip-address")
                        })
                
                # Add interface information to nodes
                for node in topology["nodes"]:
                    device_id = node["device_id"]
                    if device_id in device_interfaces:
                        node["interfaces"] = device_interfaces[device_id]
            
            return topology
            
        except Exception as e:
            return {"error": f"Failed to get network topology: {str(e)}"}

async def main():
    """Main function to run the MCP server"""
    server_instance = SDWANMCPServer()
    
    # Perform initial authentication
    logger.info("Starting SD-WAN MCP Server...")
    logger.info("Performing initial authentication...")
    auth_result = await server_instance._authenticate()
    
    if auth_result.get("status") == "success":
        logger.info("Initial authentication successful!")
    else:
        logger.warning(f"Initial authentication failed: {auth_result.get('message')}")
        logger.info("Server will start anyway. Use 'authenticate' tool to login manually.")
    
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sdwan-mcp-server",
                server_version="1.0.0",
                capabilities=server_instance.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
