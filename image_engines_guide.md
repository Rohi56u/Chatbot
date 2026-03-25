"""
╔══════════════════════════════════════════════════════════════╗
║     🚀 SUPER FAST AI CHATBOT — Streamlit Web Interface      ║
║     Text: Groq | Images: Segmind/HuggingFace (FREE!)        ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ══════════════════════════════════════════════════════════
#  Configuration
# ══════════════════════════════════════════════════════════

load_dotenv()

IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)

MODELS = {
    "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
    "Llama 3.3 70B (Smart)": "llama-3.3-70b-versatile",
    "Gemma 2 9B": "gemma2-9b-it",
}

SYSTEM_PROMPTS = {
    "Helpful Assistant": "You are a helpful, concise, and friendly AI assistant.",
    "Creative Writer": "You are a creative writer who helps with storytelling and creative content.",
    "Code Expert": "You are an expert programmer who explains code clearly and helps debug issues.",
    "Teacher": "You are a patient teacher who explains complex topics in simple terms.",
}

IMAGE_ENGINES = {
    "Segmind (Fastest ⚡)": "segmind",
    "Hugging Face (Reliable ✅)": "huggingface",  
    "Pollinations (Backup)": "pollinations",
}

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════

def load_css():
    st.markdown("""
    <style>
    .stApp { max-width: 1200px; margin: 0 auto; }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 15px 20px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0; max-width: 80%; margin-left: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white; padding: 15px 20px;
        border-radius: 18px 18px 18px 5px;
        margin: 10px 0; max-width: 80%; margin-right: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button {
        border-radius: 20px; padding: 10px 24px;
        font-weight: 600; transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════

def slugify(text: str, max_len: int = 40) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:max_len]

def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("🔑 GROQ_API_KEY not found in .env!")
        st.stop()
    return Groq(api_key=api_key)

def export_chat_history(format_type="txt"):
    if not st.session_state.messages:
        return None
    if format_type == "txt":
        content = "=" * 60 + "\nCHAT HISTORY\n" + "=" * 60 + "\n\n"
        for msg in st.session_state.messages:
            role = "YOU" if msg["role"] == "user" else "AI"
            content += f"{role}:\n{msg['content']}\n\n" + "-" * 60 + "\n\n"
        return content.encode()
    elif format_type == "json":
        data = {
            "exported_at": datetime.now().isoformat(),
            "messages": st.session_state.messages,
        }
        return json.dumps(data, indent=2).encode()


# ══════════════════════════════════════════════════════════
#  IMAGE ENGINE 1: Segmind (BEST — Fast & Reliable)
# ══════════════════════════════════════════════════════════

def generate_image_segmind(prompt: str) -> dict:
    """Segmind API — FREE, works 99% of time!"""
    clean = prompt.strip()
    if not clean:
        return {"success": False, "error": "Empty prompt"}
    
    url = "https://api.segmind.com/v1/sd1.5-txt2img"
    payload = {
        "prompt": clean,
        "negative_prompt": "blurry, bad quality",
        "samples": 1,
        "scheduler": "DDIM",
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": int(time.time()),
        "img_width": 512,
        "img_height": 512,
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            save_path = IMAGE_DIR / f"{slugify(clean)}_{timestamp()}.png"
            save_path.write_bytes(resp.content)
            return {
                "success": True, "path": str(save_path),
                "prompt": clean, "size_kb": len(resp.content) / 1024,
                "engine": "Segmind ⚡",
            }
        return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)[:100]}


# ══════════════════════════════════════════════════════════
#  IMAGE ENGINE 2: Hugging Face (Reliable)
# ══════════════════════════════════════════════════════════

def generate_image_huggingface(prompt: str) -> dict:
    """Hugging Face Inference — FREE, no API key needed"""
    clean = prompt.strip()
    if not clean:
        return {"success": False, "error": "Empty prompt"}
    
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    payload = {"inputs": clean}
    
    try:
        resp = requests.post(API_URL, json=payload, timeout=90)
        if resp.status_code == 200:
            image_data = resp.content
            # Check if image (not error JSON)
            if image_data[:8] == b"\x89PNG\r\n\x1a\n" or image_data[:3] == b"\xff\xd8\xff":
                save_path = IMAGE_DIR / f"{slugify(clean)}_{timestamp()}.png"
                save_path.write_bytes(image_data)
                return {
                    "success": True, "path": str(save_path),
                    "prompt": clean, "size_kb": len(image_data) / 1024,
                    "engine": "Hugging Face ✅",
                }
            return {"success": False, "error": "Model loading, retry in 20s"}
        elif resp.status_code == 503:
            return {"success": False, "error": "Model loading, wait 20s"}
        return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)[:100]}


# ══════════════════════════════════════════════════════════
#  IMAGE ENGINE 3: Pollinations (Backup)
# ══════════════════════════════════════════════════════════

def generate_image_pollinations(prompt: str) -> dict:
    """Pollinations — backup option (slower, unreliable)"""
    clean = prompt.strip()
    if not clean:
        return {"success": False, "error": "Empty prompt"}
    
    encoded = quote(clean)
    url = f"https://image.pollinations.ai/prompt/{encoded}?model=flux&width=512&height=512&nologo=true&seed={int(time.time())}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "image/*"}
    
    try:
        time.sleep(2)
        resp = requests.get(url, headers=headers, timeout=60, verify=False)
        if resp.status_code == 200 and len(resp.content) > 2000:
            is_img = resp.content[:3] == b"\xff\xd8\xff" or resp.content[:8] == b"\x89PNG\r\n\x1a\n"
            if is_img:
                save_path = IMAGE_DIR / f"{slugify(clean)}_{timestamp()}.jpg"
                save_path.write_bytes(resp.content)
                return {
                    "success": True, "path": str(save_path),
                    "prompt": clean, "size_kb": len(resp.content) / 1024,
                    "engine": "Pollinations",
                }
        return {"success": False, "error": "Service busy/rate limited"}
    except Exception as e:
        return {"success": False, "error": str(e)[:100]}


# ══════════════════════════════════════════════════════════
#  MASTER IMAGE GENERATOR (Auto-fallback)
# ══════════════════════════════════════════════════════════

def generate_image(prompt: str, engine: str = "segmind") -> dict:
    """Try selected engine, auto-fallback if fails"""
    engines = {
        "segmind": generate_image_segmind,
        "huggingface": generate_image_huggingface,
        "pollinations": generate_image_pollinations,
    }
    
    # Try selected first
    if engine in engines:
        result = engines[engine](prompt)
        if result["success"]:
            return result
    
    # Auto-fallback
    for fallback in ["segmind", "huggingface", "pollinations"]:
        if fallback != engine:
            result = engines[fallback](prompt)
            if result["success"]:
                result["note"] = f"✨ Auto-fallback to {result['engine']}"
                return result
    
    return {"success": False, "error": "All engines failed"}


# ══════════════════════════════════════════════════════════
#  Chat
# ══════════════════════════════════════════════════════════

def chat_with_groq(client, messages, model, temperature, stream=True):
    try:
        return client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature, max_tokens=2048, stream=stream
        )
    except Exception as e:
        st.error(f"❌ Groq Error: {str(e)}")
        return None


# ══════════════════════════════════════════════════════════
#  Session State
# ══════════════════════════════════════════════════════════

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []


# ══════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="Super Fast AI Chatbot", page_icon="🚀",
        layout="wide", initial_sidebar_state="expanded"
    )
    
    load_css()
    init_session_state()
    
    # ── SIDEBAR ────────────────────────────────────────────
    with st.sidebar:
        st.title("🚀 Settings")
        st.markdown("---")
        
        # Chat model
        selected_model_name = st.selectbox("🤖 Model", list(MODELS.keys()), index=0)
        model = MODELS[selected_model_name]
        
        selected_prompt_name = st.selectbox("🎭 Personality", list(SYSTEM_PROMPTS.keys()), index=0)
        system_prompt = SYSTEM_PROMPTS[selected_prompt_name]
        
        temperature = st.slider("🌡️ Temperature", 0.0, 2.0, 0.7, 0.1)
        enable_streaming = st.checkbox("⚡ Streaming", value=True)
        
        st.markdown("---")
        st.subheader("🎨 Image Engine")
        
        selected_engine_name = st.selectbox(
            "Choose Engine", list(IMAGE_ENGINES.keys()), index=0,
            help="Segmind = Fastest & Most Reliable!"
        )
        image_engine = IMAGE_ENGINES[selected_engine_name]
        
        st.success("✅ **Segmind** works best!\n\n"
                   "• No API key needed\n"
                   "• 5-10 seconds\n"
                   "• 99% success rate")
        
        st.markdown("---")
        st.subheader("📊 Stats")
        col1, col2 = st.columns(2)
        col1.metric("💬", len(st.session_state.messages))
        col2.metric("🖼️", len(st.session_state.generated_images))
        
        st.markdown("---")
        st.subheader("📥 Export")
        col1, col2 = st.columns(2)
        
        if st.session_state.messages:
            with col1:
                txt = export_chat_history("txt")
                if txt:
                    st.download_button("📄 TXT", txt, f"chat_{timestamp()}.txt")
            with col2:
                json_data = export_chat_history("json")
                if json_data:
                    st.download_button("📋 JSON", json_data, f"chat_{timestamp()}.json")
        
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.generated_images = []
            st.rerun()
        
        st.markdown("---")
        st.caption("Made with ❤️")
    
    # ── MAIN AREA ──────────────────────────────────────────
    st.title("🚀 Super Fast AI Chatbot")
    st.caption("Groq + 3 Free Image APIs")
    
    # Chat history
    for msg in st.session_state.messages:
        css_class = "user-message" if msg["role"] == "user" else "assistant-message"
        icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="{css_class}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)
    
    # Image gallery
    if st.session_state.generated_images:
        st.markdown("---")
        st.subheader("🖼️ Generated Images")
        cols = st.columns(3)
        for idx, img in enumerate(st.session_state.generated_images):
            with cols[idx % 3]:
                st.image(img["path"], caption=img["prompt"], use_container_width=True)
                st.caption(f"{img.get('engine', '?')} • {img['size_kb']:.1f} KB")
    
    st.markdown("---")
    
    # Input
    user_input = st.chat_input("Type message or /image <prompt>...")
    
    if user_input:
        if user_input.lower().startswith("/image"):
            img_prompt = user_input[len("/image"):].strip()
            if img_prompt:
                with st.spinner(f"🎨 Generating with {selected_engine_name}..."):
                    result = generate_image(img_prompt, image_engine)
                
                if result["success"]:
                    st.success(f"✅ {result.get('engine', 'Engine')}: {result['prompt']}")
                    if "note" in result:
                        st.info(result["note"])
                    st.session_state.generated_images.append(result)
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")
                    st.info("💡 Try different engine or simpler prompt!")
            else:
                st.warning("⚠️ Add prompt after /image")
        
        else:
            # Chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
            client = get_groq_client()
            
            with st.chat_message("assistant"):
                if enable_streaming:
                    placeholder = st.empty()
                    full = ""
                    stream = chat_with_groq(client, messages, model, temperature, stream=True)
                    if stream:
                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full += chunk.choices[0].delta.content
                                placeholder.markdown(full + "▌")
                        placeholder.markdown(full)
                        st.session_state.messages.append({"role": "assistant", "content": full})
                else:
                    resp = chat_with_groq(client, messages, model, temperature, stream=False)
                    if resp:
                        reply = resp.choices[0].message.content
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()


if __name__ == "__main__":
    main()