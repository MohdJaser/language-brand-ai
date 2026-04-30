# ============================================
# language_detector.py
# PURPOSE: Detect the language of any input text
# ============================================

# WHAT: We're importing the tools we need
# WHY: langdetect gives us language detection
#      detect() → returns language code (e.g., 'en', 'fr', 'hi')
#      LangDetectException → handles errors gracefully
from langdetect import detect, LangDetectException


# This is a dictionary — like a lookup table
# WHAT: Maps short language codes to full names
# WHY: "en" is not user-friendly, "English" is!
LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "hi": "Hindi",
    "zh-cn": "Chinese (Simplified)",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "it": "Italian",
    "te": "Telugu",
    "ta": "Tamil",
    "bn": "Bengali"
}


# WHAT: This is our main function
# WHY: A function packages logic so we can reuse it
#      anywhere in the project just by calling it
# HOW: It takes text as input, returns language name
def detect_language(text):

    if not text or text.strip() == "":
        return "Unknown", "unknown"

    # ADD THIS ↓ — warn user if text is too short
    if len(text.strip()) < 20:
        return "Text too short to detect accurately — please type more", "unknown"

    try:
        lang_code = detect(text)
        lang_name = LANGUAGE_NAMES.get(lang_code, f"Unknown ({lang_code})")
        return lang_name, lang_code

    except LangDetectException:
        return "Could not detect", "unknown"


    # WHAT: Catches any detection errors
    # WHY: If text is too short or gibberish, langdetect can fail
    #      We catch the error instead of crashing the whole app
    except LangDetectException:
        return "Could not detect", "unknown"


# ============================================
# TESTING BLOCK
# WHAT: This only runs when YOU run this file directly
# WHY: It lets us test just this module without running
#      the whole app — very useful for debugging!
# HOW: __name__ == "__main__" is True only when file
#      is run directly, not when imported elsewhere
# ============================================
if __name__ == "__main__":

    # Test samples in different languages
    test_texts = [
        "Hello, how are you?",           # English
        "Bonjour, comment ça va?",        # French
        "नमस्ते, आप कैसे हैं?",           # Hindi
        "Hola, ¿cómo estás?",             # Spanish
        "مرحبا كيف حالك",                 # Arabic
    ]

    print("=" * 45)
    print("   LANGUAGE DETECTOR - TEST RESULTS")
    print("=" * 45)

    for text in test_texts:
        name, code = detect_language(text)
        print(f"Text    : {text}")
        print(f"Detected: {name} (code: {code})")
        print("-" * 45)