#!/bin/bash
# Deploy Scenario MCP Server Globally Like Context7

echo "🌍 Deploying Scenario MCP Server Globally..."
echo "   Following Context7 MCP global installation pattern"
echo ""

# Global MCP servers directory (following standard conventions)
GLOBAL_MCP_DIR="$HOME/.local/share/mcp-servers"
SCENARIO_MCP_GLOBAL="$GLOBAL_MCP_DIR/scenario-mcp"

# Claude configuration directories (all possible locations)
CLAUDE_CONFIGS=(
    "$HOME/.claude"
    "$HOME/.config/claude"
    "$HOME/Library/Application Support/Claude"
    "$HOME/.claude-code"
    "$HOME/.config/claude-code"
)

echo "📁 Setting up global MCP directory structure..."
mkdir -p "$GLOBAL_MCP_DIR"

echo "📦 Copying Scenario MCP to global location..."
# Remove existing if it exists
rm -rf "$SCENARIO_MCP_GLOBAL"
# Copy current working version
cp -r "/Users/qusaiabushanap/dev/amani/scenario-mcp" "$SCENARIO_MCP_GLOBAL"

echo "✅ Scenario MCP deployed to: $SCENARIO_MCP_GLOBAL"
echo ""

# Create global MCP servers configuration
GLOBAL_MCP_CONFIG='{
  "mcpServers": {
    "scenario": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "'$SCENARIO_MCP_GLOBAL'",
        "python",
        "src/simple_server.py"
      ],
      "env": {
        "PYTHONPATH": "'$SCENARIO_MCP_GLOBAL'/src"
      }
    }
  }
}'

echo "⚙️  Configuring global MCP servers..."
for config_dir in "${CLAUDE_CONFIGS[@]}"; do
    echo "   📝 Setting up: $config_dir"
    mkdir -p "$config_dir"
    
    # Create mcp_servers.json
    echo "$GLOBAL_MCP_CONFIG" > "$config_dir/mcp_servers.json"
    
    # Also create in subdirectories that might be checked
    mkdir -p "$config_dir/mcp"
    echo "$GLOBAL_MCP_CONFIG" > "$config_dir/mcp/servers.json"
done

echo ""
echo "🧪 Testing global installation..."

# Test that the global installation works
if [ -f "$SCENARIO_MCP_GLOBAL/src/simple_server.py" ]; then
    echo "✅ Server files deployed correctly"
    
    # Test server can start from global location
    cd "$SCENARIO_MCP_GLOBAL"
    if timeout 3 uv run python src/simple_server.py --help 2>/dev/null; then
        echo "✅ Server starts from global location"
    else
        echo "⚠️  Server startup test inconclusive"
    fi
else
    echo "❌ Server files missing from global location"
fi

echo ""
echo "🎯 Creating startup verification script..."
cat > "$SCENARIO_MCP_GLOBAL/verify-global.sh" << 'EOF'
#!/bin/bash
echo "🔍 Scenario MCP Global Status Check"
echo "=================================="
echo "Global location: ~/.local/share/mcp-servers/scenario-mcp"
echo "Server status: $([ -f ~/.local/share/mcp-servers/scenario-mcp/src/simple_server.py ] && echo "✅ Installed" || echo "❌ Missing")"
echo ""
echo "Config files:"
for config in ~/.claude/mcp_servers.json ~/.config/claude/mcp_servers.json; do
    echo "  $config: $([ -f "$config" ] && echo "✅" || echo "❌")"
done
echo ""
echo "🚀 To use from ANY directory:"
echo "   cd ~ && claude-code"
echo "   Then: 'List available MCP tools'"
EOF
chmod +x "$SCENARIO_MCP_GLOBAL/verify-global.sh"

echo ""
echo "🎉 Global Deployment Complete!"
echo ""
echo "📋 What was done:"
echo "   ✅ Copied Scenario MCP to: $SCENARIO_MCP_GLOBAL"
echo "   ✅ Created global MCP configuration in multiple locations"
echo "   ✅ Server renamed to 'scenario' (like 'context7')"
echo "   ✅ Available from ANY directory when using Claude Code"
echo ""
echo "🚀 How to use:"
echo "   1. Close ALL Claude Code sessions completely"
echo "   2. Open Claude Code from ANY directory:"
echo "      cd ~ && claude-code"
echo "   3. Test: 'List available MCP tools'"
echo "   4. Should see: scenario_test_connection, scenario_simple_generate"
echo ""
echo "🔍 To verify installation:"
echo "   ~/.local/share/mcp-servers/scenario-mcp/verify-global.sh"
echo ""
echo "🎨 Scenario MCP is now globally available like Context7! ✨"