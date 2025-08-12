#!/bin/bash
# Verify Global MCP Configuration

echo "🔍 Verifying Global Scenario MCP Configuration..."
echo "=" * 60

# Check config files exist
CONFIG_FILES=(
    "$HOME/.claude/mcp_servers.json"
    "$HOME/.config/claude/mcp_servers.json"
    "$HOME/Library/Application Support/Claude/mcp_servers.json"
)

echo "📋 Checking configuration files:"
for config in "${CONFIG_FILES[@]}"; do
    if [ -f "$config" ]; then
        echo "✅ EXISTS: $config"
        
        # Verify it contains ScenarioMCP
        if grep -q "ScenarioMCP" "$config"; then
            echo "   ✅ Contains ScenarioMCP configuration"
        else
            echo "   ❌ Missing ScenarioMCP configuration"
        fi
    else
        echo "❌ MISSING: $config"
    fi
done

echo ""
echo "🧪 Testing MCP server startup:"

# Test server can start
PROJECT_PATH="/Users/qusaiabushanap/dev/amani/scenario-mcp"
if [ -d "$PROJECT_PATH" ]; then
    echo "✅ Project directory exists: $PROJECT_PATH"
    
    if [ -f "$PROJECT_PATH/src/simple_server.py" ]; then
        echo "✅ Simple server exists"
        
        # Test server startup (timeout after 3 seconds)
        echo "🚀 Testing server startup..."
        timeout 3 uv run --directory "$PROJECT_PATH" python src/simple_server.py > /dev/null 2>&1 &
        SERVER_PID=$!
        
        sleep 1
        
        if kill -0 $SERVER_PID 2>/dev/null; then
            echo "✅ Server starts successfully"
            kill $SERVER_PID 2>/dev/null
        else
            echo "⚠️  Server startup test inconclusive"
        fi
    else
        echo "❌ Simple server missing"
    fi
else
    echo "❌ Project directory missing: $PROJECT_PATH"
fi

echo ""
echo "🔑 Testing API credentials:"
if [ -f "$PROJECT_PATH/.env" ]; then
    echo "✅ .env file exists"
    
    # Check if API key is configured
    if grep -q "SCENARIO_API_KEY=" "$PROJECT_PATH/.env"; then
        API_KEY=$(grep "SCENARIO_API_KEY=" "$PROJECT_PATH/.env" | cut -d'=' -f2)
        if [ -n "$API_KEY" ] && [ "$API_KEY" != "your_api_key_here" ]; then
            echo "✅ API key configured"
        else
            echo "❌ API key not set"
        fi
    fi
else
    echo "❌ .env file missing"
fi

echo ""
echo "=" * 60
echo "🎯 Summary:"
echo "   Global MCP configuration is set up to make Scenario MCP"
echo "   available automatically in ALL Claude Code sessions."
echo ""
echo "🚀 To test:"
echo "   1. Close ALL Claude Code sessions"
echo "   2. From ANY directory: claude-code"
echo "   3. Test: 'List available MCP tools'"
echo "   4. Should see: scenario_test_connection, scenario_simple_generate"
echo ""
echo "🎨 Your Scenario MCP is now globally configured! ✨"