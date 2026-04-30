# ============================================
# translator.py
# PURPOSE: Translate text into any target language
# ============================================

# WHAT: Importing our translation engine
# WHY: GoogleTranslator is free, supports 100+ languages
#      and doesn't need an API key — perfect for our project
# HOW: deep-translator wraps Google Translate in clean Python
from deep_translator import GoogleTranslator, exceptions


# WHAT: A comprehensive dictionary of supported languages
# WHY: We show users friendly names ("French") but the
#      library needs language codes ("fr") internally
# HOW: We'll use this to validate user choices and
#      convert names → codes before translating
SUPPORTED_LANGUAGES = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Dutch": "nl",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Russian": "ru",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
}


# ============================================
# CORE TRANSLATION FUNCTION
# ============================================

# WHAT: Main function that does the translation
# WHY: We wrap the library call in our own function so
#      we can add validation, error handling & formatting
# HOW: Takes text + target language name as input,
#      returns translated text as output
def translate_text(text, target_language, source_language="auto"):

    # STEP 1: Validate input
    # WHY: Never trust raw input — always check it first
    if not text or text.strip() == "":
        return "⚠️ No text provided for translation."

    # STEP 2: Convert language name → language code
    # WHY: User selects "French" but library needs "fr"
    # HOW: Look it up in our dictionary above
    if target_language not in SUPPORTED_LANGUAGES:
        return f"⚠️ '{target_language}' is not a supported language."

    target_code = SUPPORTED_LANGUAGES[target_language]

    # STEP 3: Perform the actual translation
    # WHY: This is where the magic happens!
    # HOW: GoogleTranslator(source, target) sets up the translator
    #      .translate(text) sends the text and gets back translation
    #      source="auto" means it auto-detects the input language
    try:
        translator = GoogleTranslator(
            source=source_language,
            target=target_code
        )
        translated = translator.translate(text)
        return translated

    # STEP 4: Handle specific errors
    # WHY: Network issues, unsupported text, or API limits
    #      can cause failures — we catch them cleanly
    except exceptions.NotValidPayload:
        return "⚠️ Text is too short or invalid to translate."

    except exceptions.RequestError:
        return "⚠️ Network error. Please check your internet connection."

    except Exception as e:
        return f"⚠️ Translation failed: {str(e)}"


# ============================================
# BATCH TRANSLATION FUNCTION
# ============================================

# WHAT: Translates text into MULTIPLE languages at once
# WHY: A company expanding globally needs their content
#      in many languages simultaneously — not one by one
# HOW: We loop through a list of target languages and
#      call translate_text() for each one
def translate_to_multiple(text, target_languages):

    # WHAT: A dictionary to store all results
    # WHY: We want to return all translations together
    #      in one neat package — {language: translation}
    results = {}

    for language in target_languages:
        translation = translate_text(text, language)
        results[language] = translation

    return results


# ============================================
# HELPER FUNCTION
# ============================================

# WHAT: Returns the list of all supported language names
# WHY: Our UI (app.py) will need this list to show
#      a dropdown menu of language choices
def get_supported_languages():
    return list(SUPPORTED_LANGUAGES.keys())


# ============================================
# TESTING BLOCK
# ============================================
if __name__ == "__main__":

    print("=" * 50)
    print("   TRANSLATION ENGINE - TEST RESULTS")
    print("=" * 50)

    # TEST 1: Single translation
    # A typical brand slogan being translated
    sample_text = "Quality you can trust, delivered to your door."

    print("\n📝 Original Text:")
    print(f"   {sample_text}")
    print("\n🌍 Single Translation Test:")
    print("-" * 50)

    single_langs = ["French", "German", "Hindi", "Japanese"]
    for lang in single_langs:
        result = translate_text(sample_text, lang)
        print(f"  {lang:20} → {result}")

    # TEST 2: Batch translation
    # Simulating a company translating their tagline globally
    print("\n\n🌐 Batch Translation Test (Global Expansion):")
    print("-" * 50)

    tagline = "Innovating the future, today."
    global_languages = ["Spanish", "Arabic", "Chinese (Simplified)", "Telugu", "Russian"]

    batch_results = translate_to_multiple(tagline, global_languages)

    print(f"\n📝 Tagline: '{tagline}'")
    print(f"🌍 Translated into {len(batch_results)} languages:\n")
    for lang, translation in batch_results.items():
        print(f"  {lang:25} → {translation}")

    print("\n" + "=" * 50)
    print("✅ Translation Engine Test Complete!")
    print("=" * 50)