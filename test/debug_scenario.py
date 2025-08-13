#!/usr/bin/env python3
"""Debug Scenario AI generation issues."""

import asyncio
import sys
sys.path.append('/Users/qusaiabushanap/dev/amani/scenario-mcp')
from enhanced_art_direction_analyst import RiyadhSkyGuardianStyleAnalyst

async def debug_single_generation():
    """Debug a single generation to see what's happening."""
    analyst = RiyadhSkyGuardianStyleAnalyst()
    
    print("🔍 Testing single image generation...")
    
    # Test with a simple prompt
    test_prompt = "majestic Saudi falcon, detailed feathers, traditional falconry bird, game character, photorealistic, ultra-detailed"
    
    print(f"📝 Prompt: {test_prompt}")
    print("⏳ Starting generation...")
    
    try:
        generation_result = await analyst.scenario_ai.generate_image(
            prompt=test_prompt,
            model_id="flux.1-dev",
            width=512,
            height=512,
            num_inference_steps=30,
            guidance=7
        )
        
        print(f"🎯 Generation result: {generation_result}")
        
        if generation_result["success"]:
            job_id = generation_result["data"]["job_id"]
            print(f"✅ Job started successfully: {job_id}")
            
            print("⏳ Waiting for completion...")
            completion_result = await analyst.wait_for_generation_complete(job_id, max_wait_time=120)
            
            print(f"🏁 Completion result: {completion_result}")
            
            if completion_result["success"]:
                images = completion_result["data"]["images"]
                print(f"🖼️  Generated {len(images)} images")
                
                for i, image in enumerate(images):
                    print(f"  Image {i+1}: {image.get('url', 'No URL')}")
            else:
                print(f"❌ Generation failed: {completion_result['message']}")
        else:
            print(f"❌ Failed to start generation: {generation_result['message']}")
            
    except Exception as e:
        print(f"💥 Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_single_generation())