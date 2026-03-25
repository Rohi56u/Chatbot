"""
Setup Verification Script
Run this to check if everything is configured correctly
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_dependencies():
    """Check if all required packages are installed."""
    print_header("Checking Dependencies")
    
    # Map package names to import names (some are different!)
    required = {
        "groq": ("groq", "Groq API client"),
        "python-dotenv": ("dotenv", "Environment variables"),
        "requests": ("requests", "HTTP client"),
        "colorama": ("colorama", "Terminal colors (optional)"),
        "streamlit": ("streamlit", "Web interface (optional)"),
    }
    
    missing = []
    
    for package, (import_name, description) in required.items():
        try:
            __import__(import_name)
            print(f"✅ {package:20} — {description}")
        except ImportError:
            print(f"❌ {package:20} — {description} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("📦 Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def check_env_file():
    """Check if .env file exists and has API key."""
    print_header("Checking Environment Setup")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("\n📝 Create a file named '.env' with:")
        print("   GROQ_API_KEY=your_key_here")
        print("\n🔑 Get free API key at: https://console.groq.com/keys")
        return False
    
    print("✅ .env file exists")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        print("\n📝 Add this line to .env:")
        print("   GROQ_API_KEY=your_key_here")
        return False
    
    if api_key == "your_groq_api_key_here" or api_key == "your_key_here":
        print("⚠️  You need to replace the placeholder with your actual API key")
        print("🔑 Get it at: https://console.groq.com/keys")
        return False
    
    print(f"✅ GROQ_API_KEY is set (length: {len(api_key)} chars)")
    return True

def check_file_structure():
    """Check if all required files exist."""
    print_header("Checking File Structure")
    
    required_files = {
        "main.py": "Terminal version",
        "app.py": "Web version (Streamlit)",
        "requirements.txt": "Dependencies list",
        ".env": "API keys",
    }
    
    all_exist = True
    
    for file, description in required_files.items():
        path = Path(file)
        if path.exists():
            print(f"✅ {file:20} — {description}")
        else:
            print(f"❌ {file:20} — {description} (MISSING)")
            all_exist = False
    
    # Check image directory
    img_dir = Path("generated_images")
    if img_dir.exists():
        print(f"✅ {'generated_images/':20} — Image storage folder")
    else:
        print(f"ℹ️  {'generated_images/':20} — Will be created automatically")
    
    return all_exist

def test_groq_connection():
    """Try to connect to Groq API."""
    print_header("Testing Groq API Connection")
    
    try:
        from groq import Groq
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print("❌ Cannot test — API key not found")
            return False
        
        print("⏳ Attempting to connect to Groq API...")
        
        client = Groq(api_key=api_key)
        
        # Try a simple request
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=10,
        )
        
        print("✅ Successfully connected to Groq API!")
        print(f"📡 Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)[:100]}")
        print("\n💡 Common issues:")
        print("   • Invalid API key")
        print("   • No internet connection")
        print("   • API service down")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║        🚀  SUPER FAST AI CHATBOT - Setup Check         ║
╚══════════════════════════════════════════════════════════╝
""")
    
    checks = {
        "Dependencies": check_dependencies(),
        "Environment": check_env_file(),
        "Files": check_file_structure(),
        "API Connection": test_groq_connection(),
    }
    
    print_header("Summary")
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("""
🎉 Everything is ready!

You can now run:
  • Terminal version: python main.py
  • Web version:      streamlit run app.py

Or use the shortcuts:
  • Windows: run_terminal.bat or run_web.bat
""")
    else:
        print("""
⚠️  Some checks failed. Please fix the issues above.

Need help? Check README.md for detailed instructions.
""")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()