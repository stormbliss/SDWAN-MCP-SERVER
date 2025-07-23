# SD-WAN MCP Server Setup Guide

This guide will walk you through setting up the SD-WAN MCP Server from GitHub.

## 📋 Prerequisites

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Git installed
- [ ] Access to your SD-WAN management server
- [ ] Admin credentials for your SD-WAN system
- [ ] Cursor IDE installed (for integration)

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/sdwan-mcp-server.git

# Navigate to the project directory
cd sdwan-mcp-server

# Verify files are present
ls -la
```

You should see these files:
```
main.py
config.py
test_client.py
requirements.txt
setup.py
mcp_config.json
.env.example
.gitignore
LICENSE
README.md
SETUP_GUIDE.md
```

### Step 2: Create Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv sdwan-mcp-env

# Activate virtual environment
# On Linux/Mac:
source sdwan-mcp-env/bin/activate

# On Windows:
sdwan-mcp-env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 4: Configure Environment Variables

⚠️ **CRITICAL**: You must update the IP address to match your SD-WAN server!

```bash
# Copy the example environment file
cp .env.example .env

# Edit the environment file
nano .env  # or use your preferred editor
```

**Update these required settings in `.env`:**

```bash
# CHANGE THIS TO YOUR SD-WAN SERVER IP
SDWAN_BASE_URL="https://YOUR_ACTUAL_SDWAN_IP:8443"

# UPDATE WITH YOUR CREDENTIALS
SDWAN_USERNAME="your_actual_username"
SDWAN_PASSWORD="your_actual_password"

# OPTIONAL: SSL Settings
VERIFY_SSL="false"  # Set to "true" for production with valid certificates
LOG_LEVEL="INFO"
```

**Example configurations:**

```bash
# Lab Environment
SDWAN_BASE_URL="https://192.168.1.100:8443"
SDWAN_USERNAME="admin"
SDWAN_PASSWORD="admin123"

# Production Environment
SDWAN_BASE_URL="https://sdwan-controller.company.com:8443"
SDWAN_USERNAME="service_account"
SDWAN_PASSWORD="secure_password"
```

### Step 5: Test the Configuration

```bash
# Load environment variables
source .env  # Linux/Mac
# or
set -a; source .env; set +a  # Alternative for Linux/Mac

# Test authentication
python -c "
import asyncio
from main import SDWANMCPServer

async def test_auth():
    server = SDWANMCPServer()
    result = await server._authenticate()
    print('Authentication Result:', result)

asyncio.run(test_auth())
"
```

### Step 6: Run the Test Client

```bash
# Run the comprehensive test
python test_client.py
```

**Expected output:**
```
Testing authentication...
Authentication result:
{
  "status": "success",
  "message": "Authentication successful",
  "session_id": "ABC123...",
  "response": "..."
}

Available tools:
  - get_fabric_devices: Get list of all SD-WAN fabric devices
  - authenticate: Authenticate with the SD-WAN management server
  ...
```

### Step 7: Start the MCP Server

```bash
# Start the server
python main.py
```

**Expected output:**
```
INFO:sdwan-mcp-server:Starting SD-WAN MCP Server...
INFO:sdwan-mcp-server:Performing initial authentication...
INFO:sdwan-mcp-server:Authentication successful. Session ID: ABC123...
INFO:sdwan-mcp-server:Initial authentication successful!
```

### Step 8: Integrate with Cursor

#### Option A: MCP Configuration File

1. **Create MCP configuration:**
   ```bash
   # Copy the template
   cp mcp_config.json ~/.cursor/mcp_config.json
   
   # Edit with your actual path
   nano ~/.cursor/mcp_config.json
   ```

2. **Update the configuration:**
   ```json
   {
     "mcpServers": {
       "sdwan-mcp-server": {
         "command": "python",
         "args": ["/full/path/to/your/sdwan-mcp-server/main.py"],
         "env": {
           "SDWAN_BASE_URL": "https://your-sdwan-server:8443",
           "SDWAN_USERNAME": "your_username",
           "SDWAN_PASSWORD": "your_password"
         }
       }
     }
   }
   ```

3. **Restart Cursor**

#### Option B: Direct Cursor Settings

1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "MCP"
3. Add this configuration:
   ```json
   {
     "mcp": {
       "servers": {
         "sdwan-mcp-server": {
           "command": "python",
           "args": ["/full/path/to/your/sdwan-mcp-server/main.py"]
         }
       }
     }
   }
   ```

### Step 9: Test Cursor Integration

1. **Open Cursor**
2. **Start a new chat**
3. **Try these queries:**
   ```
   "Show me all SD-WAN fabric devices"
   "Check if I'm authenticated to the SD-WAN server"
   "Give me a health summary of the SD-WAN network"
   ```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Connection Refused
```bash
# Test connectivity to your SD-WAN server
curl -k https://YOUR_SDWAN_IP:8443

# If this fails, check:
# - IP address is correct
# - Port 8443 is accessible
# - SD-WAN server is running
```

#### 2. Authentication Failed
```bash
# Verify credentials by logging into web interface
# Check username/password in .env file
# Ensure account has API access permissions
```

#### 3. SSL Certificate Errors
```bash
# For self-signed certificates, use:
export VERIFY_SSL="false"

# For production with valid certificates:
export VERIFY_SSL="true"
```

#### 4. Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

#### 5. Environment Variables Not Loading
```bash
# Manually export variables
export SDWAN_BASE_URL="https://your-server:8443"
export SDWAN_USERNAME="your_username"
export SDWAN_PASSWORD="your_password"

# Then run
python main.py
```

### Debug Mode

Enable detailed logging:
```bash
export LOG_LEVEL="DEBUG"
python main.py
```

### Verify Setup Checklist

- [ ] Repository cloned successfully
- [ ] Dependencies installed (`pip list` shows mcp, requests, urllib3)
- [ ] `.env` file created and configured with correct IP
- [ ] Authentication test passes
- [ ] Test client runs successfully
- [ ] MCP server starts without errors
- [ ] Cursor integration configured
- [ ] Can query SD-WAN data from Cursor

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** for error messages
2. **Verify network connectivity** to your SD-WAN server
3. **Test authentication** manually
4. **Check permissions** for your user account
5. **Open an issue** on GitHub with:
   - Error messages
   - Your environment details
   - Steps you've tried

## 🎉 Success!

Once everything is working, you should be able to:

- ✅ Query SD-WAN devices from Cursor using natural language
- ✅ Get real-time network statistics and health information
- ✅ Monitor BFD sessions and tunnel status
- ✅ Generate comprehensive network reports
- ✅ Troubleshoot network issues efficiently

**Next Steps:**
- Explore all available tools in Cursor
- Set up monitoring dashboards
- Create custom queries for your specific needs
- Share with your team!
