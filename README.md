# 🎮 Amani - Unity WebGL Game

A Unity WebGL project with automated CI/CD pipeline for seamless development and deployment.

## 🚀 Quick Start

### Project Setup Status ✅
- ✅ Unity Hub installed and ready
- ✅ GitHub repository created: [byqusai/amani](https://github.com/byqusai/amani)
- ✅ Vercel project linked: `amani-qusaiii.vercel.app`
- ✅ CI/CD pipeline configured
- ✅ Build scripts and optimization ready
- ⏳ **Next: Create Unity project in Unity Hub**

### Immediate Next Steps

1. **Open Unity Hub and Create Project:**
   ```bash
   open -a "/Applications/Unity Hub.app"
   ```
   - Install Unity 2022.3 LTS with WebGL Build Support
   - Create new 3D project named "Amani" 
   - Location: `/Users/qusaiabushanap/dev/amani`

2. **Configure WebGL Settings:**
   - File → Build Settings → Switch to WebGL
   - Player Settings → WebGL → Compression: Gzip ✓
   - Player Settings → WebGL → Decompression Fallback ✓

3. **Test Local Build:**
   ```bash
   ./build-and-deploy.sh
   ```

4. **Deploy to Production:**
   ```bash
   git add .
   git commit -m "Add Unity project files"
   git push origin main
   # Automatically builds and deploys via GitHub Actions
   ```

## 🔗 Links

- **GitHub Repository**: https://github.com/byqusai/amani
- **Vercel Project**: https://vercel.com/qusaiii/amani
- **Live Demo**: https://amani-qusaiii.vercel.app *(after first deploy)*

## 📁 Project Structure

```
amani/
├── Assets/                    # Unity game assets
├── ProjectSettings/           # Unity project configuration
├── .github/workflows/         # GitHub Actions CI/CD
├── build-and-deploy.sh       # Local build script
├── vercel.json               # Vercel deployment config
├── SETUP.md                  # Detailed setup guide
├── MCP_GAMEDEV_GUIDE.md      # MCP integration guide
└── README.md                 # This file
```

## 🛠️ Development Workflow

1. **Make changes in Unity**
2. **Test locally**: `./build-and-deploy.sh`
3. **Commit and push**: Auto-deploys via GitHub Actions
4. **Monitor**: Check Vercel deployment status

## 🎯 Features

- ⚡ **Automated WebGL Builds** via GitHub Actions
- 🚀 **Instant Deployment** to Vercel
- 📦 **Optimized for Web** with Gzip compression
- 🔄 **Git LFS** for large Unity assets
- 📊 **MCP Integration** for enhanced development workflow

## 🎮 MCP Game Development Tools

The project includes comprehensive MCP integration for:

- **Unity Documentation** via Context7 MCP
- **Error Monitoring** via Sentry MCP  
- **Repository Management** via GitHub MCP
- **Custom Game Tools** for analytics and configuration

See `MCP_GAMEDEV_GUIDE.md` for detailed setup instructions.

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide
- **[MCP_GAMEDEV_GUIDE.md](MCP_GAMEDEV_GUIDE.md)** - MCP integration for game development
- **[Unity WebGL to Vercel Guide](SETUP.md#unity-webgl-to-vercel---complete-cicd-setup-guide)** - CI/CD pipeline details

## 🎯 Next Development Phase

1. **Unity Project Creation** (pending manual setup)
2. **Game Mechanics Implementation**
3. **Asset Integration and Optimization**
4. **WebGL Performance Tuning**
5. **MCP Tool Integration**
6. **Player Analytics Setup**

---

**🤖 Generated with Claude Code**  
**Co-Authored-By: Claude <noreply@anthropic.com>**