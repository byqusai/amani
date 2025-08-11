#!/bin/bash

# Unity WebGL Build and Deploy Script for Amani Project
# This script builds the Unity project locally and deploys to Vercel

echo "🎮 Starting Unity WebGL build for Amani..."

# Check if Unity exists
UNITY_PATH="/Applications/Unity/Hub/Editor"
if [ ! -d "$UNITY_PATH" ]; then
    echo "❌ Unity not found. Please install Unity through Unity Hub."
    exit 1
fi

# Get the latest Unity LTS version installed
UNITY_VERSION=$(ls "$UNITY_PATH" | grep "2022.3" | tail -1)
if [ -z "$UNITY_VERSION" ]; then
    echo "❌ Unity 2022.3 LTS not found. Please install Unity 2022.3 LTS."
    exit 1
fi

UNITY_EXEC="$UNITY_PATH/$UNITY_VERSION/Unity.app/Contents/MacOS/Unity"
echo "📦 Using Unity: $UNITY_VERSION"

# Clean previous build
rm -rf WebGLBuild/

# Build Unity WebGL
echo "🔨 Building Unity WebGL..."
"$UNITY_EXEC" \
  -batchmode \
  -nographics \
  -silent-crashes \
  -logFile build.log \
  -projectPath . \
  -buildTarget WebGL \
  -executeMethod BuildScript.BuildWebGL \
  -quit

# Check if build was successful
if [ $? -eq 0 ] && [ -d "WebGLBuild" ]; then
    echo "✅ Unity build successful!"
    
    # Display build log if there were warnings
    if grep -q "warning" build.log; then
        echo "⚠️  Build warnings found:"
        grep "warning" build.log
    fi
    
    # Deploy to Vercel if requested
    read -p "🚀 Deploy to Vercel? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd WebGLBuild
        echo "📤 Deploying to Vercel..."
        vercel --prod
        echo "✅ Deployment complete!"
    else
        echo "📁 Build available in WebGLBuild/ directory"
        echo "💡 To test locally: cd WebGLBuild && python3 -m http.server 8080"
    fi
    
else
    echo "❌ Build failed! Check build.log for details:"
    tail -20 build.log
    exit 1
fi