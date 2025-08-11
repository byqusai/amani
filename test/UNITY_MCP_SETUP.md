# Unity MCP Setup Documentation

## Installation Status: ✅ COMPLETED

### Dependencies Installed:
- ✅ Python 3.13.5 (already available)  
- ✅ uv 0.8.8 (installed via Homebrew)
- ✅ Unity MCP repository cloned to `unity-mcp/`

### Configuration Files:
- ✅ `.mcp.json` created with UnityMCP server configuration
- ✅ Unity package added to `My project/Packages/manifest.json`

### MCP Configuration:
```json
{
  "mcpServers": {
    "UnityMCP": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/qusaiabushanap/dev/amani/unity-mcp/UnityMcpServer/src",
        "server.py"
      ]
    }
  }
}
```

### Unity Package Integration:
Added to manifest.json:
```json
"com.coplaydev.unity-mcp": "https://github.com/CoplayDev/unity-mcp.git?path=/UnityMcpBridge",
"com.unity.nuget.newtonsoft-json": "3.0.2"
```

**Package Installation Methods Used:**
1. ✅ Git URL in manifest.json (fixed package name)
2. ✅ Local copy in Packages folder as backup  
3. ✅ Added required Newtonsoft JSON dependency

## Next Steps:

1. **Open Unity Project**: Launch Unity and open the "My project" folder
2. **Verify Package Installation**: Check Window > Package Manager for Unity MCP Bridge
3. **Configure Unity MCP**: Go to Window > Unity MCP to set up the connection
4. **Test Connection**: Look for green status indicator 🟢 "Connected"

## Available Unity MCP Tools:
- `manage_script`: Create/edit C# scripts  
- `manage_scene`: Load, save, manipulate scenes
- `manage_asset`: Import and modify assets
- `manage_gameobject`: Create and modify game objects
- `manage_editor`: Control Unity Editor functions
- `read_console`: Access Unity console output

## Troubleshooting:

### If you can't find Unity MCP Bridge:
1. **Close Unity completely** and reopen the project
2. **Check Package Manager**: Window > Package Manager > In Project (dropdown)
3. **Look for "Unity MCP Bridge"** - it should appear with display name, not package name
4. **Check Console**: Look for any import/dependency errors
5. **Alternative search**: Search for "MCP" in Package Manager search box

### Connection Issues:
- If connection fails, restart Claude Code after opening Unity  
- Verify the server path in `.mcp.json` matches your project location
- Check Unity console for any package import errors
- Try the Window > Unity MCP menu item - it should appear after successful installation

### Issues Fixed:
- ✅ Corrected package name from `com.coplay.unity-mcp` to `com.coplaydev.unity-mcp`
- ✅ Added both git URL and local copy installation methods  
- ✅ Added required Newtonsoft JSON dependency
- ✅ Fixed Claude Code executable path (was `/usr/local/bin/claude`, now `/opt/homebrew/bin/claude`)
- ✅ Created proper `.claude.json` configuration for Unity MCP registration

### Configuration Fix Required:
If you see "Claude CLI registration failed" error, run this script:

```bash
./test/fix-unity-mcp-config.sh
```

This fixes:
1. Creates correct `.claude.json` in home directory
2. Creates symbolic link to Claude executable where Unity expects it  
3. Uses correct server path for your project