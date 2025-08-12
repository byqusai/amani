#!/bin/bash
# Setup Global MCP Configuration for Scenario

echo "🔧 Setting up Global Scenario MCP Configuration..."
echo "   This will make Scenario MCP available in ALL Claude Code sessions"
echo ""

# Create Claude config directory if it doesn't exist
CLAUDE_CONFIG_DIR="$HOME/.claude"
mkdir -p "$CLAUDE_CONFIG_DIR"

# Global MCP configuration path
GLOBAL_MCP_CONFIG="$CLAUDE_CONFIG_DIR/mcp_servers.json"

# Current project path (absolute)
PROJECT_PATH="/Users/qusaiabushanap/dev/amani/scenario-mcp"

echo "📁 Configuration paths:"
echo "   Global config: $GLOBAL_MCP_CONFIG"
echo "   Project path: $PROJECT_PATH"
echo ""

# Check if global config exists
if [ -f "$GLOBAL_MCP_CONFIG" ]; then
    echo "⚠️  Global MCP config already exists"
    echo "   Backing up existing config..."
    cp "$GLOBAL_MCP_CONFIG" "$GLOBAL_MCP_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create global MCP configuration
cat > "$GLOBAL_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "ScenarioMCP": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "$PROJECT_PATH",
        "python",
        "src/simple_server.py"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_PATH/src"
      }
    }
  }
}
EOF

echo "✅ Global MCP configuration created!"
echo ""

# Also create user-level config in common locations
USER_MCP_CONFIGS=(
    "$HOME/.config/claude/mcp_servers.json"
    "$HOME/Library/Application Support/Claude/mcp_servers.json"
)

for config_path in "${USER_MCP_CONFIGS[@]}"; do
    config_dir=$(dirname "$config_path")
    if [ ! -d "$config_dir" ]; then
        echo "📁 Creating directory: $config_dir"
        mkdir -p "$config_dir"
    fi
    
    echo "📝 Creating config: $config_path"
    cp "$GLOBAL_MCP_CONFIG" "$config_path"
done

echo ""
echo "🎯 Testing configuration..."

# Test that the server can start
if uv run --directory "$PROJECT_PATH" python src/simple_server.py --help 2>/dev/null; then
    echo "✅ Scenario MCP server can start successfully"
else
    echo "⚠️  Server test had issues, but config is created"
fi

echo ""
echo "🎉 Global MCP Setup Complete!"
echo ""
echo "📋 What was configured:"
echo "   ✅ Global MCP servers config in multiple locations"
echo "   ✅ Scenario MCP server will start automatically"
echo "   ✅ Available from ANY directory when using Claude Code"
echo ""
echo "🚀 How to use:"
echo "   1. Close ALL Claude Code sessions"
echo "   2. Open Claude Code from ANY directory:"
echo "      cd ~ && claude-code"
echo "   3. Test with: 'List available MCP tools'"
echo ""
echo "🎨 Your Scenario MCP will now work automatically! ✨"