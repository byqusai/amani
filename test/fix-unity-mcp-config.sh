#!/bin/bash
# Unity MCP Configuration Fix Script

echo "🔧 Fixing Unity MCP Configuration..."

# 1. Create/update .claude.json in home directory
echo "📝 Creating .claude.json configuration..."
cat > ~/.claude.json << 'EOF'
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
EOF

# 2. Create symbolic link to claude executable where Unity expects it
echo "🔗 Creating claude executable link..."
sudo mkdir -p /usr/local/bin
sudo ln -sf /opt/homebrew/bin/claude /usr/local/bin/claude

# 3. Verify the setup
echo "✅ Verifying setup..."
echo "Claude executable location: $(which claude)"
echo "Claude config file exists: $(test -f ~/.claude.json && echo 'YES' || echo 'NO')"

echo ""
echo "🎉 Configuration fixed! Now:"
echo "1. Go back to Unity"
echo "2. Click 'Register with Claude Code' button"
echo "3. Look for green 🟢 'Connected' status"
echo ""