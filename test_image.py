"""
Image API Diagnostic Tool
Run this to see which engines work and why others fail
"""

import requests
import time
from pathlib import Path

IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("🔍 TESTING ALL IMAGE GENERATION APIS")
print("=" * 60)

test_prompt = "a red car"

# ══════════════════════════════════════════════════════════
#  TEST 1: Segmind
# ══════════════════════════════════════════════════════════

print("\n📍 TEST 1: Segmind API")
print("-" * 60)

try:
    url = "https://api.segmind.com/v1/sd1.5-txt2img"
    payload = {
        "prompt": test_prompt,
        "negative_prompt": "blurry",
        "samples": 1,
        "scheduler": "DDIM",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": 12345,
        "img_width": 512,
        "img_height": 512,
    }
    
    print(f"   URL: {url}")
    print(f"   Prompt: {test_prompt}")
    print("   Sending request...")
    
    resp = requests.post(url, json=payload, timeout=30)
    
    print(f"   Status Code: {resp.status_code}")
    print(f"   Response Size: {len(resp.content)} bytes")
    print(f"   Content Type: {resp.headers.get('Content-Type', 'unknown')}")
    
    if resp.status_code == 200:
        # Check if it's actually an image
        if len(resp.content) > 1000:
            save_path = IMAGE_DIR / "test_segmind.png"
            save_path.write_bytes(resp.content)
            print(f"   ✅ SUCCESS! Saved to {save_path}")
        else:
            print(f"   ❌ Response too small (not an image)")
            print(f"   Response: {resp.text[:200]}")
    else:
        print(f"   ❌ FAILED: HTTP {resp.status_code}")
        print(f"   Error: {resp.text[:200]}")

except Exception as e:
    print(f"   ❌ EXCEPTION: {e}")

# ══════════════════════════════════════════════════════════
#  TEST 2: Hugging Face
# ══════════════════════════════════════════════════════════

print("\n📍 TEST 2: Hugging Face API")
print("-" * 60)

try:
    url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    
    print(f"   URL: {url}")
    print(f"   Prompt: {test_prompt}")
    print("   Sending request...")
    
    resp = requests.post(url, json={"inputs": test_prompt}, timeout=30)
    
    print(f"   Status Code: {resp.status_code}")
    print(f"   Response Size: {len(resp.content)} bytes")
    print(f"   Content Type: {resp.headers.get('Content-Type', 'unknown')}")
    
    if resp.status_code == 200:
        img = resp.content
        # Check if it's an image (PNG or JPEG magic bytes)
        is_png = img[:8] == b"\x89PNG\r\n\x1a\n"
        is_jpg = img[:3] == b"\xff\xd8\xff"
        
        if is_png or is_jpg:
            save_path = IMAGE_DIR / "test_huggingface.png"
            save_path.write_bytes(img)
            print(f"   ✅ SUCCESS! Saved to {save_path}")
        else:
            print(f"   ❌ Not an image (might be JSON error)")
            print(f"   Response: {resp.text[:200]}")
    elif resp.status_code == 503:
        print(f"   ⚠️  Model is loading (try again in 20 seconds)")
    else:
        print(f"   ❌ FAILED: HTTP {resp.status_code}")
        print(f"   Error: {resp.text[:200]}")

except Exception as e:
    print(f"   ❌ EXCEPTION: {e}")

# ══════════════════════════════════════════════════════════
#  TEST 3: Pollinations
# ══════════════════════════════════════════════════════════

print("\n📍 TEST 3: Pollinations API")
print("-" * 60)

try:
    from urllib.parse import quote
    encoded = quote(test_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true&seed=12345"
    
    print(f"   URL: {url}")
    print(f"   Prompt: {test_prompt}")
    print("   Sending request (may take 30-60 seconds)...")
    
    resp = requests.get(url, timeout=90, verify=False)
    
    print(f"   Status Code: {resp.status_code}")
    print(f"   Response Size: {len(resp.content)} bytes")
    print(f"   Content Type: {resp.headers.get('Content-Type', 'unknown')}")
    
    if resp.status_code == 200:
        if len(resp.content) > 2000:
            is_jpg = resp.content[:3] == b"\xff\xd8\xff"
            is_png = resp.content[:8] == b"\x89PNG\r\n\x1a\n"
            
            if is_jpg or is_png:
                save_path = IMAGE_DIR / "test_pollinations.jpg"
                save_path.write_bytes(resp.content)
                print(f"   ✅ SUCCESS! Saved to {save_path}")
            else:
                print(f"   ❌ Not an image")
                print(f"   Response start: {resp.content[:100]}")
        else:
            print(f"   ❌ Response too small")
    elif resp.status_code == 530:
        print(f"   ❌ Rate limited or server busy")
    else:
        print(f"   ❌ FAILED: HTTP {resp.status_code}")

except Exception as e:
    print(f"   ❌ EXCEPTION: {e}")

# ══════════════════════════════════════════════════════════
#  TEST 4: Alternative - DreamStudio (needs key)
# ══════════════════════════════════════════════════════════

print("\n📍 TEST 4: DreamStudio (Stability AI)")
print("-" * 60)
print("   ℹ️  Requires API key (skipping test)")
print("   Get free key at: https://beta.dreamstudio.ai/")

# ══════════════════════════════════════════════════════════
#  Summary
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("📊 DIAGNOSTIC COMPLETE")
print("=" * 60)
print("\nCheck the 'generated_images' folder for test results.")
print("If all failed, check:")
print("  1. Internet connection")
print("  2. Firewall/antivirus blocking requests")
print("  3. ISP/network restrictions")
print("\nTry: ping google.com")
print("     curl https://httpbin.org/get")
print("=" * 60)

input("\nPress Enter to exit...")