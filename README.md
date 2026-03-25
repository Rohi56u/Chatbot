# 🚀 Super Fast AI Chatbot

A powerful AI chatbot with both **Terminal** and **Web** interfaces, powered by Groq (Llama 3.1) for lightning-fast text responses and Pollinations.ai for image generation.

---

## ✨ Features

### 🖥️ Terminal Version (`main.py`)
- ⚡ Instant text responses using Groq API
- 🎨 AI image generation with `/image` command
- 💾 Conversation memory/context
- 🎨 Colorful terminal UI
- 📜 View chat history
- 🗑️ Clear conversation

### 🌐 Web Version (`app.py`) — **NEW!**
- 🎯 Beautiful Streamlit web interface
- 💬 WhatsApp-style chat bubbles
- ⚡ Real-time streaming responses (typing effect)
- 🖼️ Image gallery with previews
- 🎛️ Sidebar controls:
  - Model selection (Llama 3.1 8B, 3.3 70B, Gemma 2 9B)
  - Personality presets (Assistant, Writer, Coder, Teacher)
  - Temperature slider
  - Streaming toggle
- 📊 Live statistics (message count, images generated)
- 📥 Export chat as TXT or JSON
- 🎨 Custom CSS with gradient themes
- 📱 Responsive design
- 🔄 Session persistence

---

## 📦 Installation

### 1. Clone or Download
```bash
# If you have git
git clone <your-repo-url>
cd chatbot

# Or just create a new folder and add the files
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Your FREE Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up (free)
3. Create an API key
4. Copy it

### 4. Create `.env` File
Create a file named `.env` in the same folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🚀 Usage

### Terminal Version
```bash
python main.py
```

**Commands:**
- Just type normally to chat
- `/image <prompt>` — Generate an image (e.g., `/image a cyberpunk city`)
- `/history` — View conversation history
- `/clear` — Clear memory
- `/help` — Show commands
- `exit` or `quit` — Exit

### Web Version (Streamlit)
```bash
streamlit run app.py
```

This will open your browser automatically at `http://localhost:8501`

**Features:**
- Type in the chat input to talk with AI
- Use `/image <prompt>` to generate images
- Click sidebar to change settings
- Export your chat using download buttons
- Clear chat with one click

---

## 🎨 Web Interface Preview

The Streamlit version includes:

1. **Sidebar Controls**
   - 🤖 Model Selection (3 models)
   - 🎭 Personality Selection (4 presets)
   - 🌡️ Temperature Slider (0.0 - 2.0)
   - ⚡ Streaming Toggle
   - 📊 Real-time Statistics
   - 📥 Export Buttons (TXT/JSON)
   - 🗑️ Clear Chat Button

2. **Main Chat Area**
   - 👤 User messages (purple gradient)
   - 🤖 AI messages (pink gradient)
   - Smooth animations
   - Copy-friendly text

3. **Image Gallery**
   - Grid layout (3 columns)
   - Hover effects
   - Image captions with prompts
   - File size display

---

## 🎯 Advanced Settings (Web Version)

### Model Selection
- **Llama 3.1 8B (Fast)** — Best for quick responses
- **Llama 3.3 70B (Smart)** — Best for complex tasks
- **Gemma 2 9B** — Google's model, balanced

### Personality Presets
- **Helpful Assistant** — General-purpose, friendly
- **Creative Writer** — For storytelling & creative content
- **Code Expert** — For programming help
- **Teacher** — For learning & explanations

### Temperature Control
- **0.0 - 0.3** — Very focused, deterministic
- **0.4 - 0.7** — Balanced (default: 0.7)
- **0.8 - 2.0** — More creative & random

---

## 🖼️ Image Generation

Both versions support AI image generation:

```
/image a majestic lion in golden light
/image cyberpunk city at night
/image sunset over mountains
```

**Notes:**
- ⏱️ Takes 30-60 seconds (free tier)
- 📁 Images saved to `generated_images/` folder
- ⚠️ Rate limit: 1 image per 15 seconds
- 🎨 Uses Pollinations.ai Flux model (best quality)

---

## 📂 Project Structure

```
chatbot/
├── main.py              # Terminal version
├── app.py               # Streamlit web version
├── requirements.txt     # Python dependencies
├── .env                 # API keys (create this)
├── generated_images/    # Auto-created for images
└── README.md           # This file
```

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Make sure `.env` file exists in the same folder
- Check that it contains: `GROQ_API_KEY=your_key_here`
- No spaces around the `=` sign

### "Image generation failed (530 error)"
- Wait 15-20 seconds between image requests
- Pollinations.ai free tier is rate-limited
- Try again after waiting

### "Module not found"
```bash
pip install -r requirements.txt
```

### Web app won't open
```bash
# Try specifying port
streamlit run app.py --server.port 8502
```

---

## 🎓 Tips for Best Results

### For Chat:
- Be specific with your questions
- Use follow-up questions to dive deeper
- Try different personalities for different tasks
- Adjust temperature for creativity vs. precision

### For Images:
- Be descriptive (e.g., "a photorealistic sunset over mountains with warm colors")
- Keep prompts under 50 words
- Wait for completion before requesting another
- Shorter prompts = faster generation

---

## 🚀 Deployment (Optional)

### Deploy Web Version to Streamlit Cloud (FREE)
1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Add `GROQ_API_KEY` to Secrets
5. Deploy!

**Note:** Don't commit your `.env` file to GitHub!

---

## 🆘 Support

If you encounter issues:
1. Check the error message carefully
2. Verify your API key is correct
3. Make sure all dependencies are installed
4. Try the terminal version first (simpler debugging)

---

## 📝 License

Free to use for personal and educational purposes.

---

## 🙏 Credits

- **Groq** — Lightning-fast LLM inference
- **Pollinations.ai** — Free AI image generation
- **Streamlit** — Beautiful web apps in Python
- **Made with ❤️**

---

## 🔮 Future Ideas

- [ ] Multiple language support
- [ ] Voice input/output
- [ ] PDF chat (upload & analyze)
- [ ] Image editing commands
- [ ] Multi-model comparison
- [ ] Chat templates
- [ ] API endpoint
- [ ] Mobile app version

---

**Enjoy your AI chatbot!** 🎉