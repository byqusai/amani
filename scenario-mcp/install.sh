#!/bin/bash
# Scenario MCP Server Installation Script
# Author: Qusai Saleem (hi@qusai.org)

set -e  # Exit on any error

echo "🎨 Installing Scenario MCP Server..."
echo "   Author: Qusai Saleem"
echo "   Purpose: AI Asset Generation for Agent 4"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install UV first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ UV found: $(uv --version)"

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Scenario API credentials:"
    echo "   - SCENARIO_API_KEY=your_api_key_here"
    echo "   - SCENARIO_API_SECRET=your_api_secret_here"
    echo ""
fi

# Test basic import
echo "🧪 Testing basic imports..."
uv run python -c "
import sys
sys.path.append('src')
try:
    from config import config
    from scenario_client import ScenarioAPIClient
    from tools import register_all_tools
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Create run script
cat > run_server.sh << 'EOF'
#!/bin/bash
# Scenario MCP Server Runner
echo "🚀 Starting Scenario MCP Server..."
uv run src/server.py
EOF

chmod +x run_server.sh

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Scenario API credentials"
echo "2. Test the server: ./run_server.sh"
echo "3. Add to MCP config in Claude Code"
echo ""
echo "🔧 MCP Configuration:"
echo '   Add this to your .mcp.json:'
echo '   {'
echo '     "mcpServers": {'
echo '       "ScenarioMCP": {'
echo '         "command": "uv",'
echo '         "args": ['
echo '           "run",'
echo '           "--directory",'
echo '           "'$(pwd)'/src",'
echo '           "server.py"'
echo '         ]'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "📚 Read README.md for detailed usage instructions"
echo "💬 Support: hi@qusai.org"