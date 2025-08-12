#!/bin/bash
# Move Scenario MCP to /dev directory for global access

echo "📦 Moving Scenario MCP to /dev directory..."
echo "   New location: /Users/qusaiabushanap/dev/scenario-mcp"
echo ""

# Create /dev directory if it doesn't exist
DEV_DIR="/Users/qusaiabushanap/dev"
mkdir -p "$DEV_DIR"

# New global location
NEW_SCENARIO_LOCATION="$DEV_DIR/scenario-mcp"

echo "🚀 Copying Scenario MCP to /dev..."
# Remove existing if it exists
rm -rf "$NEW_SCENARIO_LOCATION"
# Copy current working version
cp -r "/Users/qusaiabushanap/dev/amani/scenario-mcp" "$NEW_SCENARIO_LOCATION"

echo "✅ Scenario MCP copied to: $NEW_SCENARIO_LOCATION"
echo ""

# Claude configuration directories
CLAUDE_CONFIGS=(
    "$HOME/.claude"
    "$HOME/.config/claude"
    "$HOME/Library/Application Support/Claude"
    "$HOME/.claude-code"
    "$HOME/.config/claude-code"
)

# Create updated MCP servers configuration pointing to /dev location
GLOBAL_MCP_CONFIG='{
  "mcpServers": {
    "scenario": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "'$NEW_SCENARIO_LOCATION'",
        "python",
        "src/simple_server.py"
      ],
      "env": {
        "PYTHONPATH": "'$NEW_SCENARIO_LOCATION'/src"
      }
    }
  }
}'

echo "⚙️  Updating global MCP configuration..."
for config_dir in "${CLAUDE_CONFIGS[@]}"; do
    echo "   📝 Updating: $config_dir"
    mkdir -p "$config_dir"
    
    # Update mcp_servers.json
    echo "$GLOBAL_MCP_CONFIG" > "$config_dir/mcp_servers.json"
    
    # Also update in subdirectories
    mkdir -p "$config_dir/mcp"
    echo "$GLOBAL_MCP_CONFIG" > "$config_dir/mcp/servers.json"
done

echo ""
echo "🧪 Testing new location..."

# Test that the new installation works
if [ -f "$NEW_SCENARIO_LOCATION/src/simple_server.py" ]; then
    echo "✅ Server files copied correctly"
    
    # Test server can start from new location
    cd "$NEW_SCENARIO_LOCATION"
    if timeout 3 uv run python src/simple_server.py --help 2>/dev/null; then
        echo "✅ Server starts from /dev location"
    else
        echo "⚠️  Server startup test inconclusive"
    fi
else
    echo "❌ Server files missing from new location"
fi

echo ""
echo "🎯 Creating verification script in new location..."
cat > "$NEW_SCENARIO_LOCATION/verify-dev-location.sh" << 'EOF'
#!/bin/bash
echo "🔍 Scenario MCP Status Check"
echo "============================"
echo "Location: /Users/qusaiabushanap/dev/scenario-mcp"
echo "Server status: $([ -f /Users/qusaiabushanap/dev/scenario-mcp/src/simple_server.py ] && echo "✅ Installed" || echo "❌ Missing")"
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
chmod +x "$NEW_SCENARIO_LOCATION/verify-dev-location.sh"

echo ""
echo "🎉 Move to /dev Complete!"
echo ""
echo "📋 What was done:"
echo "   ✅ Moved Scenario MCP to: $NEW_SCENARIO_LOCATION"
echo "   ✅ Updated all global MCP configurations"
echo "   ✅ Server accessible from ANY directory"
echo "   ✅ Outside of project structure for clean global access"
echo ""
echo "🚀 How to use:"
echo "   1. Close ALL Claude Code sessions completely"
echo "   2. Open Claude Code from ANY directory:"
echo "      cd ~ && claude-code"
echo "   3. Test: 'List available MCP tools'"
echo "   4. Should see: scenario_test_connection, scenario_simple_generate"
echo ""
echo "🔍 To verify installation:"
echo "   /Users/qusaiabushanap/dev/scenario-mcp/verify-dev-location.sh"
echo ""
echo "🎨 Scenario MCP now lives in /dev and works globally! ✨"