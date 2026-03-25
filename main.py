"""
╔══════════════════════════════════════════════════════════╗
║     SUPER FAST AI CHATBOT — Terminal Version             ║
║     Text: Groq | Images: Segmind/HuggingFace (FREE!)    ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("❌ Missing: pip install python-dotenv")

try:
    from groq import Groq
except ImportError:
    sys.exit("❌ Missing: pip install groq")

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    sys.exit("❌ Missing: pip install colorama")

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    sys.exit("❌ Missing: pip install requests")

colorama_init(autoreset=True)
load_dotenv()

MODEL = "llama-3.1-8b-instant"
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)
SYSTEM_PROMPT = "You are a helpful, concise, and friendly AI assistant."


def banner():
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════════════════╗
║       🚀  SUPER FAST AI CHATBOT  (Groq + Llama 3.1)     ║
╠══════════════════════════════════════════════════════════╣
║  • Type message to chat                                  ║
║  • /image <prompt>  →  AI image (3 free engines!)        ║
║  • /history         →  view conversation                 ║
║  • /clear           →  wipe memory                       ║
║  • /help            →  show menu                         ║
║  • exit / quit      →  leave                             ║
╚══════════════════════════════════════════════════════════╝
""")


def slugify(text: str, max_len: int = 40) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:max_len]


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ══════════════════════════════════════════════════════════
#  IMAGE ENGINE 1: Segmind (FASTEST & MOST RELIABLE)
# ══════════════════════════════════════════════════════════

def generate_image_segmind(prompt: str) -> dict:
    """Segmind — 99% success rate, 5-10 seconds"""
    url = "https://api.segmind.com/v1/sd1.5-txt2img"
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, bad quality",
        "samples": 1,
        "scheduler": "DDIM",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": int(time.time()),
        "img_width": 512,
        "img_height": 512,
    }
    try:
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code == 200:
            save_path = IMAGE_DIR / f"{slugify(prompt)}_{timestamp()}.png"
            save_path.write_bytes(resp.content)
            return {"success": True, "path": save_path, "size_kb": len(resp.content) / 1024}
        return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)[:80]}


# ══════════════════════════════════════════════════════════
#  IMAGE ENGINE 2: Hugging Face (Backup)
# ══════════════════════════════════════════════════════════

def generate_image_huggingface(prompt: str) -> dict:
    """Hugging Face — good quality, slower"""
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    try:
        resp = requests.post(API_URL, json={"inputs": prompt}, timeout=90)
        if resp.status_code == 200:
            img = resp.content
            if img[:8] == b"\x89PNG\r\n\x1a\n" or img[:3] == b"\xff\xd8\xff":
                save_path = IMAGE_DIR / f"{slugify(prompt)}_{timestamp()}.png"
                save_path.write_bytes(img)
                return {"success": True, "path": save_path, "size_kb": len(img) / 1024}
        return {"success": False, "error": "Model loading or error"}
    except Exception as e:
        return {"success": False, "error": str(e)[:80]}


# ══════════════════════════════════════════════════════════
#  IMAGE ENGINE 3: Pollinations (Last resort)
# ══════════════════════════════════════════════════════════

def generate_image_pollinations(prompt: str) -> dict:
    """Pollinations — slowest, least reliable"""
    encoded = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?model=flux&width=512&height=512&nologo=true&seed={int(time.time())}"
    try:
        time.sleep(2)
        resp = requests.get(url, timeout=60, verify=False)
        if resp.status_code == 200 and len(resp.content) > 2000:
            if resp.content[:3] == b"\xff\xd8\xff" or resp.content[:8] == b"\x89PNG\r\n\x1a\n":
                save_path = IMAGE_DIR / f"{slugify(prompt)}_{timestamp()}.jpg"
                save_path.write_bytes(resp.content)
                return {"success": True, "path": save_path, "size_kb": len(resp.content) / 1024}
        return {"success": False, "error": "Service busy"}
    except Exception as e:
        return {"success": False, "error": str(e)[:80]}


# ══════════════════════════════════════════════════════════
#  MASTER IMAGE GENERATOR (Auto-fallback)
# ══════════════════════════════════════════════════════════

def generate_image(prompt: str) -> None:
    """Try all 3 engines with auto-fallback"""
    clean = prompt.strip()
    if not clean:
        print(Fore.RED + "⚠  Please provide a prompt after /image")
        return

    print(Fore.YELLOW + f"\n🎨  Generating: \"{clean}\"")
    
    # Try Segmind first (fastest)
    print(Fore.YELLOW + "⏳  Trying Segmind (fastest)...")
    result = generate_image_segmind(clean)
    
    if result["success"]:
        print(Fore.GREEN + Style.BRIGHT + f"✅  Segmind success!")
        print(Fore.GREEN + f"📁  Saved → {result['path']}")
        print(Fore.GREEN + f"📐  Size: {result['size_kb']:.1f} KB\n")
        return
    
    # Fallback to Hugging Face
    print(Fore.YELLOW + "⏳  Segmind failed, trying Hugging Face...")
    result = generate_image_huggingface(clean)
    
    if result["success"]:
        print(Fore.GREEN + Style.BRIGHT + f"✅  Hugging Face success!")
        print(Fore.GREEN + f"📁  Saved → {result['path']}")
        print(Fore.GREEN + f"📐  Size: {result['size_kb']:.1f} KB\n")
        return
    
    # Last resort: Pollinations
    print(Fore.YELLOW + "⏳  Trying Pollinations (may take 30-60s)...")
    result = generate_image_pollinations(clean)
    
    if result["success"]:
        print(Fore.GREEN + Style.BRIGHT + f"✅  Pollinations success!")
        print(Fore.GREEN + f"📁  Saved → {result['path']}")
        print(Fore.GREEN + f"📐  Size: {result['size_kb']:.1f} KB\n")
        return
    
    # All failed
    print(Fore.RED + "\n❌  All 3 engines failed.")
    print(Fore.YELLOW + "💡  Try:")
    print(Fore.YELLOW + "    • Simpler prompt (e.g., 'a red car')")
    print(Fore.YELLOW + "    • Check internet connection")
    print(Fore.YELLOW + "    • Wait 10 seconds and retry\n")


# ══════════════════════════════════════════════════════════
#  Chat
# ══════════════════════════════════════════════════════════

def chat(client: Groq, history: list, user_input: str) -> str:
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        temperature=0.7,
        max_tokens=1024,
    )
    reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    return reply


# ══════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════

def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(Fore.RED + Style.BRIGHT +
              "❌  GROQ_API_KEY not found in .env\n"
              "    Add: GROQ_API_KEY=your_key_here\n"
              "    Get key: https://console.groq.com/keys")
        sys.exit(1)

    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(Fore.RED + f"❌  Groq init failed: {e}")
        sys.exit(1)

    banner()
    history = []

    while True:
        try:
            raw = input(Fore.CYAN + Style.BRIGHT + "You ➤  " + Style.RESET_ALL)
        except (EOFError, KeyboardInterrupt):
            print(Fore.YELLOW + "\n\n👋  Goodbye!\n")
            break

        user_input = raw.strip()
        if not user_input:
            continue

        lower = user_input.lower()

        if lower in ("exit", "quit", "bye"):
            print(Fore.YELLOW + "\n👋  Goodbye!\n")
            break

        if lower == "/help":
            banner()
            continue

        if lower == "/clear":
            history.clear()
            print(Fore.YELLOW + "🗑   Memory cleared.\n")
            continue

        if lower == "/history":
            if not history:
                print(Fore.YELLOW + "📭  No history yet.\n")
            else:
                print(Fore.YELLOW + "\n── Conversation History ─────────────────")
                for msg in history:
                    label = Fore.CYAN + "You" if msg["role"] == "user" else Fore.GREEN + "AI "
                    print(f"{label}{Style.RESET_ALL} │ {msg['content']}")
                print(Fore.YELLOW + "─────────────────────────────────────────\n")
            continue

        if lower.startswith("/image"):
            image_prompt = user_input[len("/image"):].strip()
            generate_image(image_prompt)
            continue

        if user_input.startswith("/"):
            print(Fore.RED + "⚠  Unknown command. Type /help\n")
            continue

        # Chat
        try:
            print(Fore.YELLOW + "⏳  Thinking…", end="\r")
            reply = chat(client, history, user_input)
            print(" " * 30, end="\r")
            print(Fore.GREEN + Style.BRIGHT + "AI  ➤  " +
                  Style.RESET_ALL + Fore.GREEN + reply + "\n")
        except Exception as e:
            print(" " * 30, end="\r")
            err = str(e)
            if "authentication" in err.lower():
                print(Fore.RED + "❌  Auth failed — check API key.\n")
            elif "rate limit" in err.lower():
                print(Fore.RED + "❌  Rate limit — wait.\n")
            else:
                print(Fore.RED + f"❌  Error: {err}\n")
            if history and history[-1]["role"] == "user":
                history.pop()


if __name__ == "__main__":
    main()