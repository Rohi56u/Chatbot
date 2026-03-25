"""
Central configuration for AI Chatbot
Used by both terminal and web versions
"""

from pathlib import Path

# ══════════════════════════════════════════════════════════
#  API & Model Settings
# ══════════════════════════════════════════════════════════

# Available Groq models
AVAILABLE_MODELS = {
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B (Fast)",
        "description": "Best for quick responses",
        "max_tokens": 2048,
        "speed": "⚡⚡⚡",
    },
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B (Smart)", 
        "description": "Best for complex tasks",
        "max_tokens": 4096,
        "speed": "⚡⚡",
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B",
        "description": "Google's balanced model",
        "max_tokens": 2048,
        "speed": "⚡⚡⚡",
    },
}

# Default model
DEFAULT_MODEL = "llama-3.1-8b-instant"

# Default temperature
DEFAULT_TEMPERATURE = 0.7

# ══════════════════════════════════════════════════════════
#  System Prompts
# ══════════════════════════════════════════════════════════

SYSTEM_PROMPTS = {
    "assistant": {
        "name": "Helpful Assistant",
        "prompt": "You are a helpful, concise, and friendly AI assistant. Answer clearly and keep responses focused.",
    },
    "writer": {
        "name": "Creative Writer",
        "prompt": "You are a creative writer who helps with storytelling, creative content, and imaginative ideas. Use vivid language and engaging narratives.",
    },
    "coder": {
        "name": "Code Expert",
        "prompt": "You are an expert programmer who explains code clearly, helps debug issues, and provides best practices. Use code examples when helpful.",
    },
    "teacher": {
        "name": "Patient Teacher",
        "prompt": "You are a patient teacher who explains complex topics in simple terms. Use analogies, examples, and break down concepts step-by-step.",
    },
    "analyst": {
        "name": "Data Analyst",
        "prompt": "You are a data analyst who helps interpret data, create insights, and explain statistics clearly. Be precise and analytical.",
    },
}

DEFAULT_SYSTEM_PROMPT = SYSTEM_PROMPTS["assistant"]["prompt"]

# ══════════════════════════════════════════════════════════
#  Image Generation Settings
# ══════════════════════════════════════════════════════════

# Pollinations.ai settings
POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"
POLLINATIONS_MODEL = "flux"  # Options: flux, flux-realism, flux-anime, turbo
POLLINATIONS_DEFAULT_WIDTH = 1024
POLLINATIONS_DEFAULT_HEIGHT = 1024
POLLINATIONS_RATE_LIMIT_SECONDS = 16  # Free tier limit

# Image storage
IMAGE_DIR = Path("generated_images")
IMAGE_FORMAT = "jpg"

# ══════════════════════════════════════════════════════════
#  UI Settings
# ══════════════════════════════════════════════════════════

# Terminal colors (for colorama)
TERMINAL_COLORS = {
    "user": "CYAN",
    "ai": "GREEN", 
    "system": "YELLOW",
    "error": "RED",
    "success": "GREEN",
}

# Web UI gradients
WEB_GRADIENTS = {
    "user_message": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "ai_message": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "sidebar": "linear-gradient(180deg, #667eea 0%, #764ba2 100%)",
    "header": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
}

# ══════════════════════════════════════════════════════════
#  Feature Flags
# ══════════════════════════════════════════════════════════

FEATURES = {
    "streaming": True,           # Enable streaming responses
    "image_generation": True,    # Enable image generation
    "export_chat": True,         # Enable chat export
    "session_persistence": True, # Save session state
    "show_statistics": True,     # Show usage stats
    "model_switching": True,     # Allow model changes
}

# ══════════════════════════════════════════════════════════
#  Limits & Constraints
# ══════════════════════════════════════════════════════════

MAX_CONVERSATION_LENGTH = 50  # Max messages in history
MAX_IMAGE_SIZE_MB = 10        # Max image file size
MAX_PROMPT_LENGTH = 500       # Max characters in prompt
REQUEST_TIMEOUT = 120         # Seconds for API requests

# ══════════════════════════════════════════════════════════
#  Error Messages
# ══════════════════════════════════════════════════════════

ERROR_MESSAGES = {
    "api_key_missing": "🔑 GROQ_API_KEY not found in .env file!",
    "rate_limit": "⚠️ Rate limit reached. Please wait a moment and try again.",
    "network_error": "🌐 Network error. Please check your internet connection.",
    "timeout": "⏱️ Request timed out. The service might be slow, try again.",
    "invalid_model": "❌ Invalid model selected. Please choose a valid model.",
    "image_failed": "🖼️ Image generation failed. Please try again.",
}

# ══════════════════════════════════════════════════════════
#  Help Text
# ══════════════════════════════════════════════════════════

COMMANDS_HELP = """
Available Commands:
  /image <prompt>  — Generate an AI image
  /history         — View conversation history
  /clear           — Clear conversation memory
  /help            — Show this help message
  exit / quit      — Exit the chatbot
"""

IMAGE_TIPS = """
Image Generation Tips:
  ✓ Be descriptive and specific
  ✓ Keep prompts under 50 words
  ✓ Wait 15+ seconds between requests
  ✓ Examples:
    - "a majestic lion in golden light"
    - "cyberpunk city at night with neon lights"
    - "peaceful sunset over mountains"
"""