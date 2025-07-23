# SD-WAN MCP Server

A comprehensive Model Context Protocol (MCP) server for monitoring and managing SD-WAN devices through REST API endpoints. This server exposes SD-WAN device monitoring and management functionality that can be integrated with Cursor and other MCP-compatible tools.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)

## 🚀 Features

- **🔧 Device Management**: List and monitor SD-WAN fabric devices
- **📊 Statistics Collection**: Interface statistics, device counters, tunnel statistics
- **🔍 BFD Monitoring**: Bidirectional Forwarding Detection state and sessions
- **⚙️ Configuration Access**: Device configuration retrieval
- **📈 Advanced Analytics**: Health summaries, traffic analysis, and alerting
- **🔐 Session Management**: Automatic authentication and session handling
- **⚡ Async Support**: Full async/await support for non-blocking operations
- **🎯 Cursor Integration**: Seamless integration with Cursor IDE

## 📋 Available Tools

### Basic Monitoring Tools
1. **get_fabric_devices** - Get list of all SD-WAN fabric devices
2. **get_device_monitor** - Get SD-WAN device monitoring information
3. **get_device_counters** - Get SD-WAN device counters and statistics
4. **get_interface_statistics** - Get interface statistics for all SD-WAN devices
5. **get_device_config** - Get SD-WAN device configuration (requires device_id)
6. **get_bfd_state** - Get BFD state for an SD-WAN device (requires device_id)
7. **get_bfd_sessions** - Get BFD sessions for an SD-WAN device (requires device_id)
8. **get_tunnel_statistics** - Get tunnel statistics for an SD-WAN device (requires device_id)

### Authentication Tools
9. **authenticate** - Authenticate with the SD-WAN management server
10. **get_session_status** - Check current authentication session status

### Advanced Analytics Tools
11. **get_device_health_summary** - Comprehensive health summary across all SD-WAN devices
12. **filter_devices_by_status** - Filter SD-WAN devices by operational status
13. **get_top_interfaces_by_traffic** - Get top interfaces ranked by traffic utilization
14. **check_bfd_session_health** - Monitor BFD session health across all SD-WAN devices
15. **generate_network_report** - Generate comprehensive SD-WAN network status report
16. **get_device_alerts** - Get alerts and warnings for SD-WAN devices by severity
17. **monitor_interface_utilization** - Monitor interface utilization with configurable thresholds
18. **get_network_topology** - Get SD-WAN network topology information

## 🛠️ Quick Start

### Prerequisites

- Python 3.8 or higher
- Access to SD-WAN management server
- Cursor IDE (for integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sdwan-mcp-server.git
   cd sdwan-mcp-server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   nano .env
   ```

4. **Update configuration**
   
   ⚠️ **IMPORTANT**: You must update the IP address in your configuration!
   
   Edit your `.env` file:
   ```bash
   # REQUIRED: Change this to your SD-WAN management server IP
   SDWAN_BASE_URL="https://YOUR_SDWAN_SERVER_IP:8443"
   
   # Update credentials
   SDWAN_USERNAME="your_username"
   SDWAN_PASSWORD="your_password"
   
   # Optional settings
   VERIFY_SSL="false"
   LOG_LEVEL="INFO"
   ```

5. **Test the server**
   ```bash
   python test_client.py
   ```

6. **Run the server**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SDWAN_BASE_URL` | SD-WAN server base URL | `https://192.168.10.130:8443` | ✅ **YES** |
| `SDWAN_USERNAME` | Authentication username | `admin` | ✅ **YES** |
| `SDWAN_PASSWORD` | Authentication password | `1` | ✅ **YES** |
| `VERIFY_SSL` | Enable SSL certificate verification | `false` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | No |
| `SESSION_TIMEOUT` | Session timeout in seconds | `3600` | No |
| `AUTO_RECONNECT` | Auto-reconnect on session expiry | `true` | No |

### Configuration Methods

#### Method 1: Environment Variables (Recommended)
```bash
export SDWAN_BASE_URL="https://your-sdwan-server:8443"
export SDWAN_USERNAME="admin"
export SDWAN_PASSWORD="your_password"
python main.py
```

#### Method 2: .env File
```bash
# Create .env file
echo "SDWAN_BASE_URL=https://your-sdwan-server:8443" > .env
echo "SDWAN_USERNAME=admin" >> .env
echo "SDWAN_PASSWORD=your_password" >> .env
python main.py
```

#### Method 3: Direct Configuration
Edit `config.py` to change default values (not recommended for production).

## 🔧 Cursor Integration

### Option 1: MCP Configuration File

1. Create or update your MCP configuration file:
   ```json
   {
     "mcpServers": {
       "sdwan-mcp-server": {
         "command": "python",
         "args": ["/full/path/to/your/project/main.py"],
         "env": {
           "SDWAN_BASE_URL": "https://your-sdwan-server:8443",
           "SDWAN_USERNAME": "admin",
           "SDWAN_PASSWORD": "your_password"
         }
       }
     }
   }
   ```

2. Update the path to point to your `main.py` file
3. Restart Cursor

### Option 2: Cursor Settings

Add to your Cursor settings:
```json
{
  "mcp": {
    "servers": {
      "sdwan-mcp-server": {
        "command": "python",
        "args": ["/full/path/to/main.py"]
      }
    }
  }
}
```

## 💡 Usage Examples

Once integrated with Cursor, you can use natural language queries:

### Basic Queries
- "Show me all SD-WAN fabric devices"
- "Get the SD-WAN interface statistics"
- "Check BFD state for SD-WAN device 200.0.1.1"
- "Get tunnel statistics for SD-WAN device 200.0.2.2"

### Advanced Analytics
- "Give me a comprehensive health summary of the SD-WAN network"
- "Show me all SD-WAN devices that are currently down"
- "What are the top 10 interfaces by traffic volume?"
- "Generate a full SD-WAN network report"
- "Which interfaces are using more than 80% bandwidth?"

### Troubleshooting
- "Check if I'm authenticated to the SD-WAN server"
- "Show me all critical alerts in the SD-WAN network"
- "What SD-WAN devices need immediate attention?"

## 🏗️ Project Structure

```
sdwan-mcp-server/
├── main.py              # Main MCP server implementation
├── config.py            # Configuration management
├── test_client.py       # Test client for validation
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── mcp_config.json     # MCP configuration template
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
├── LICENSE             # MIT license
└── README.md           # This file
```

## 🔍 API Endpoints

The server connects to these SD-WAN management API endpoints:

- `/dataservice/device` - Fabric devices
- `/dataservice/device/monitor` - Device monitoring
- `/dataservice/device/counters` - Device counters
- `/dataservice/statistics/interface` - Interface statistics
- `/dataservice/device/config` - Device configuration
- `/dataservice/device/bfd/state/device` - BFD state
- `/dataservice/device/bfd/sessions` - BFD sessions
- `/dataservice/device/tunnel/statistics` - Tunnel statistics

## 🐛 Troubleshooting

### Common Issues

1. **Connection Errors**
   ```bash
   # Check if your SD-WAN server is accessible
   curl -k https://YOUR_SDWAN_SERVER_IP:8443
   ```

2. **Authentication Errors**
   ```bash
   # Verify credentials
   export SDWAN_USERNAME="correct_username"
   export SDWAN_PASSWORD="correct_password"
   ```

3. **SSL Certificate Issues**
   ```bash
   # Disable SSL verification for self-signed certificates
   export VERIFY_SSL="false"
   ```

4. **Import Errors**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   ```

### Debug Mode

Enable detailed logging:
```bash
export LOG_LEVEL="DEBUG"
python main.py
```

### Testing Connection

```bash
# Test authentication
python -c "
import asyncio
from main import SDWANMCPServer
async def test():
    server = SDWANMCPServer()
    result = await server._authenticate()
    print(result)
asyncio.run(test())
"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sdwan-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sdwan-mcp-server/discussions)

## 🙏 Acknowledgments

- Built with [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol)
- Designed for [Cursor IDE](https://cursor.sh/) and [CLAUDE DESKTOP]
- SD-WAN management capabilities

---

⚠️ **Remember**: Always update the `SDWAN_BASE_URL` to match your SD-WAN management server's IP address!
