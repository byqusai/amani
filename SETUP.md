# Amani Unity WebGL Project Setup Guide

## 🎯 Project Overview
Amani is a Unity WebGL project with automated CI/CD pipeline that:
- Builds Unity WebGL automatically on GitHub push
- Deploys to Vercel for instant web hosting
- Optimizes for fast loading and web performance

## 🚀 Quick Start

### 1. Complete Unity Setup
Since Unity Hub is already installed, follow these steps:

1. **Open Unity Hub**
   ```bash
   open -a "/Applications/Unity Hub.app"
   ```

2. **Install Unity 2022.3 LTS**
   - Click "Installs" tab
   - Click "Install Editor"
   - Select Unity 2022.3.x LTS (latest)
   - Include modules: WebGL Build Support

3. **Create New Unity Project**
   - Click "Projects" tab
   - Click "New Project"
   - Select "3D Core" template
   - Project name: "Amani"
   - Location: `/Users/qusaiabushanap/dev/amani`
   - Click "Create Project"

### 2. Configure WebGL Build Settings
Once Unity opens:

1. **File > Build Settings**
2. **Switch to WebGL platform**
3. **Player Settings > WebGL Settings**:
   - Compression Format: `Gzip`
   - Decompression Fallback: ✓
   - Exception Support: `None`
   - Memory Size: `256 MB`

### 3. Set Up GitHub Repository

```bash
cd /Users/qusaiabushanap/dev/amani
git init
git add .
git commit -m "Initial Unity WebGL project setup"
git branch -M main
git remote add origin https://github.com/byqusai/amani.git
git push -u origin main
```

### 4. Configure GitHub Secrets
Go to GitHub repository → Settings → Secrets and variables → Actions:

**Required Secrets:**
- `UNITY_LICENSE` - Unity license file content
- `VERCEL_TOKEN` - Vercel deployment token
- `VERCEL_ORG_ID` - Your Vercel organization ID
- `VERCEL_PROJECT_ID` - Vercel project ID

**Get Unity License:**
1. Follow [Game-CI activation guide](https://game-ci.com/docs/github/activation)
2. Upload the `.ulf` file content as `UNITY_LICENSE`

**Get Vercel Tokens:**
```bash
npm install -g vercel
vercel login
vercel link
# Follow prompts to connect your project
cat .vercel/project.json  # Copy orgId and projectId
```

### 5. Deploy to Vercel
**Option A: Local Build & Deploy**
```bash
./build-and-deploy.sh
```

**Option B: Push to GitHub (Auto-deploy)**
```bash
git add .
git commit -m "Add WebGL build configuration"
git push origin main
```

## 📁 Project Structure
```
amani/
├── Assets/                 # Unity assets and scripts
├── ProjectSettings/        # Unity project configuration
├── .github/workflows/      # GitHub Actions CI/CD
├── build-and-deploy.sh     # Local build script
├── vercel.json            # Vercel deployment config
└── SETUP.md               # This guide
```

## 🔧 Development Workflow

1. **Make changes in Unity**
2. **Test locally:**
   ```bash
   ./build-and-deploy.sh
   # Choose 'n' for local testing
   cd WebGLBuild && python3 -m http.server 8080
   ```
3. **Deploy to production:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   # Auto-builds and deploys via GitHub Actions
   ```

## 🎮 Recommended Unity Settings for Web

### Performance Optimizations:
- **Texture Compression**: Use DXT for desktop, ASTC for mobile
- **Audio Compression**: MP3 or Vorbis
- **Code Stripping**: High level
- **IL2CPP Code Generation**: Faster (smaller) builds

### WebGL Specific:
- **Memory Size**: 256MB (adjust based on needs)
- **Enable Exceptions**: None (smaller build size)
- **WebAssembly Streaming**: Enabled
- **Threads Support**: Disabled (better compatibility)

## 🌐 Access Your Game
- **Production**: https://amani-byqusai.vercel.app
- **Preview Builds**: Automatic URLs from pull requests

## 🛠️ Troubleshooting

### Build Fails
1. Check `build.log` for Unity errors
2. Ensure WebGL Build Support is installed
3. Verify Unity license in GitHub secrets

### Deployment Issues
1. Check Vercel token permissions
2. Verify vercel.json configuration
3. Check GitHub Actions logs

### Performance Issues
1. Optimize textures and models
2. Use Unity Profiler
3. Enable compression in build settings

## 📚 Additional Resources
- [Unity WebGL Documentation](https://docs.unity3d.com/Manual/webgl.html)
- [Game-CI Documentation](https://game-ci.com/docs)
- [Vercel Documentation](https://vercel.com/docs)

## 🎯 Next Steps
1. Create your first scene in Unity
2. Add game mechanics
3. Test WebGL build locally
4. Push to GitHub for automatic deployment
5. Share your game URL!