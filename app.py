"""
Super Fast AI Chatbot - REAL AI Images!
AI Horde: Free Stable Diffusion (no API key)
"""

import os, sys, json, time, re
from pathlib import Path
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import requests

load_dotenv()
IMAGE_DIR = Path("generated_images")
IMAGE_DIR.mkdir(exist_ok=True)

MODELS = {
    "Llama 3.1 8B (Fast)": "llama-3.1-8b-instant",
    "Llama 3.3 70B (Smart)": "llama-3.3-70b-versatile",
}

SYSTEM_PROMPTS = {
    "Helpful Assistant": "You are helpful and friendly.",
    "Creative Writer": "You are a creative writer.",
    "Code Expert": "You are an expert programmer.",
}

def load_css():
    st.markdown("""<style>
    .stApp { max-width: 1200px; margin: 0 auto; }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 15px 20px; border-radius: 18px 18px 5px 18px;
        margin: 10px 0; max-width: 80%; margin-left: auto;
    }
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white; padding: 15px 20px; border-radius: 18px 18px 18px 5px;
        margin: 10px 0; max-width: 80%; margin-right: auto;
    }
    </style>""", unsafe_allow_html=True)

def slugify(text, max_len=40):
    return re.sub(r"\s+", "_", re.sub(r"[^\w\s-]", "", text.lower().strip()))[:max_len]

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_groq():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found!")
        st.stop()
    return Groq(api_key=api_key)

def generate_image_ai_horde(prompt, progress_cb=None):
    """AI Horde - Real Stable Diffusion images, 100% free!"""
    clean = prompt.strip()
    if not clean:
        return {"success": False, "error": "Empty"}
    
    url = "https://stablehorde.net/api/v2/generate/async"
    payload = {
        "prompt": clean,
        "params": {
            "sampler_name": "k_euler",
            "cfg_scale": 7,
            "steps": 20,
            "width": 512,
            "height": 512,
            "n": 1
        },
        "nsfw": False,
        "models": ["stable_diffusion"]
    }
    headers = {"Content-Type": "application/json", "apikey": "0000000000"}
    
    try:
        if progress_cb:
            progress_cb("📤 Submitting to AI Horde...")
        
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code != 200:
            return {"success": False, "error": f"Submit failed: {resp.status_code}"}
        
        gen_id = resp.json().get("id")
        if not gen_id:
            return {"success": False, "error": "No ID"}
        
        check_url = f"https://stablehorde.net/api/v2/generate/check/{gen_id}"
        status_url = f"https://stablehorde.net/api/v2/generate/status/{gen_id}"
        
        start = time.time()
        max_wait = 180
        
        while time.time() - start < max_wait:
            check = requests.get(check_url, timeout=10)
            if check.status_code == 200:
                data = check.json()
                done = data.get("done", False)
                queue = data.get("queue_position", 0)
                wait = data.get("wait_time", 0)
                
                if progress_cb:
                    if queue > 0:
                        progress_cb(f"⏳ Queue: {queue} | ETA: {wait}s")
                    else:
                        progress_cb(f"🎨 Generating... {int(time.time()-start)}s")
                
                if done:
                    status = requests.get(status_url, timeout=10)
                    if status.status_code == 200:
                        gens = status.json().get("generations", [])
                        if gens:
                            img_url = gens[0].get("img")
                            if img_url:
                                if progress_cb:
                                    progress_cb("📥 Downloading...")
                                img = requests.get(img_url, timeout=30)
                                if img.status_code == 200:
                                    save = IMAGE_DIR / f"{slugify(clean)}_{timestamp()}.webp"
                                    save.write_bytes(img.content)
                                    return {
                                        "success": True, "path": str(save),
                                        "prompt": clean, "size_kb": len(img.content)/1024,
                                        "engine": "AI Horde ✨",
                                        "generation_time": int(time.time()-start)
                                    }
                    return {"success": False, "error": "No image"}
            time.sleep(3)
        
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)[:80]}

def chat_groq(client, messages, model, temp, stream=True):
    try:
        return client.chat.completions.create(
            model=model, messages=messages,
            temperature=temp, max_tokens=2048, stream=stream
        )
    except Exception as e:
        st.error(f"Groq: {e}")
        return None

def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []

def main():
    st.set_page_config(page_title="AI Chatbot", page_icon="🚀", layout="wide")
    load_css()
    init_state()
    
    with st.sidebar:
        st.title("🚀 Settings")
        st.markdown("---")
        
        model_name = st.selectbox("🤖 Model", list(MODELS.keys()), 0)
        model = MODELS[model_name]
        
        prompt_name = st.selectbox("🎭 Personality", list(SYSTEM_PROMPTS.keys()), 0)
        sys_prompt = SYSTEM_PROMPTS[prompt_name]
        
        temp = st.slider("🌡️ Temperature", 0.0, 2.0, 0.7, 0.1)
        streaming = st.checkbox("⚡ Streaming", True)
        
        st.markdown("---")
        st.success("✨ **AI Horde**\n\n"
                   "• Real Stable Diffusion\n"
                   "• 100% Free\n"
                   "• No API key\n"
                   "• Takes 30-120s")
        
        st.warning("⏰ Be patient!\n\nReal AI takes 1-2 min")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        col1.metric("💬", len(st.session_state.messages))
        col2.metric("🖼️", len(st.session_state.generated_images))
        
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.generated_images = []
            st.rerun()
    
    st.title("🚀 AI Chatbot")
    st.caption("Groq + AI Horde")
    
    for msg in st.session_state.messages:
        css = "user-message" if msg["role"] == "user" else "assistant-message"
        icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="{css}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)
    
    if st.session_state.generated_images:
        st.markdown("---")
        st.subheader("🖼️ AI Images")
        cols = st.columns(3)
        for idx, img in enumerate(st.session_state.generated_images):
            with cols[idx % 3]:
                st.image(img["path"], caption=img["prompt"], use_container_width=True)
                st.caption(f"{img.get('engine','?')} • {img['size_kb']:.1f}KB • {img.get('generation_time','?')}s")
    
    st.markdown("---")
    
    user_input = st.chat_input("Type or /image <prompt> for REAL AI images...")
    
    if user_input:
        if user_input.lower().startswith("/image"):
            prompt = user_input[7:].strip()
            if prompt:
                status = st.empty()
                
                def update(msg):
                    status.info(msg)
                
                with st.spinner("🎨 Generating REAL AI image (1-2 min)..."):
                    result = generate_image_ai_horde(prompt, update)
                
                status.empty()
                
                if result["success"]:
                    t = result.get('generation_time','?')
                    st.success(f"✅ Done! ({t}s)")
                    st.session_state.generated_images.append(result)
                    st.rerun()
                else:
                    st.error(f"❌ {result.get('error')}")
            else:
                st.warning("Add prompt!")
        
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": sys_prompt}] + st.session_state.messages
            client = get_groq()
            
            with st.chat_message("assistant"):
                if streaming:
                    placeholder = st.empty()
                    full = ""
                    stream = chat_groq(client, messages, model, temp, True)
                    if stream:
                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full += chunk.choices[0].delta.content
                                placeholder.markdown(full + "▌")
                        placeholder.markdown(full)
                        st.session_state.messages.append({"role": "assistant", "content": full})
                else:
                    resp = chat_groq(client, messages, model, temp, False)
                    if resp:
                        reply = resp.choices[0].message.content
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

if __name__ == "__main__":
    main()