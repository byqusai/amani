using UnityEditor;
using UnityEngine;
using UnityEditor.Build.Reporting;

public class BuildScript
{
    [MenuItem("Build/Build WebGL")]
    public static void BuildWebGL()
    {
        // Get all scenes in build settings
        string[] scenes = GetEnabledScenes();
        
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = scenes;
        buildPlayerOptions.locationPathName = "WebGLBuild";
        buildPlayerOptions.target = BuildTarget.WebGL;
        buildPlayerOptions.options = BuildOptions.None;

        // Configure WebGL settings for optimal performance
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Gzip;
        PlayerSettings.WebGL.decompressionFallback = true;
        PlayerSettings.WebGL.exceptionSupport = WebGLExceptionSupport.None;
        PlayerSettings.WebGL.memorySize = 256; // 256MB memory limit
        
        // Enable WebAssembly streaming for faster loading
        PlayerSettings.WebGL.threadsSupport = false; // Better compatibility
        
        Debug.Log("Starting WebGL build...");
        
        BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
        BuildSummary summary = report.summary;

        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log("Build succeeded: " + summary.totalSize + " bytes");
            Debug.Log("Build time: " + summary.totalTime);
        }
        else if (summary.result == BuildResult.Failed)
        {
            Debug.LogError("Build failed");
            EditorApplication.Exit(1);
        }
    }
    
    private static string[] GetEnabledScenes()
    {
        var scenes = EditorBuildSettings.scenes;
        var enabledScenes = new string[scenes.Length];
        
        for (int i = 0; i < scenes.Length; i++)
        {
            enabledScenes[i] = scenes[i].path;
        }
        
        // If no scenes in build settings, use default scene
        if (enabledScenes.Length == 0)
        {
            enabledScenes = new string[] { "Assets/Scenes/SampleScene.unity" };
        }
        
        return enabledScenes;
    }
}