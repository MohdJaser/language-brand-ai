# ============================================
# brand_generator.py
# PURPOSE: Generate brand identity using Groq AI
# 100% FREE — Perfect for college projects!
# ============================================

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


# ============================================
# SETUP GROQ CLIENT
# ============================================
def get_groq_client():
    # Try Streamlit Cloud secrets first
    # Then fall back to local .env file
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found!")

    return Groq(api_key=api_key)


# ============================================
# CORE BRAND GENERATION FUNCTION
# ============================================
def generate_brand_identity(
    company_description,
    industry,
    target_audience,
    brand_values,
    target_markets
):
    client = get_groq_client()

    prompt = f"""
You are a world-class brand strategist and creative director.
A company needs a complete brand identity package.

Here are the company details:
- Description: {company_description}
- Industry: {industry}
- Target Audience: {target_audience}
- Core Brand Values: {brand_values}
- Target Markets (countries/regions): {target_markets}

Please generate a complete brand identity package with the following:

1. BRAND NAME SUGGESTIONS (give 3 options)
   - Each name should be memorable, global-friendly, and meaningful
   - Explain the meaning/reasoning behind each name

2. PRIMARY TAGLINE
   - One powerful, concise tagline (under 10 words)
   - Should work globally and be easy to translate

3. BRAND SLOGANS (give 3 variations)
   - Short, punchy, and emotionally resonant
   - Different tones: professional, emotional, bold

4. BRAND VOICE & TONE GUIDELINES
   - How should this brand communicate?
   - What words/phrases to use and avoid?

5. KEY BRAND MESSAGES (3 core messages)
   - The fundamental ideas the brand should always communicate

6. CULTURAL ADAPTATION NOTES
   - Specific tips for the target markets mentioned
   - Any cultural sensitivities to be aware of

Format your response clearly with each section labeled.
Be creative, strategic, and globally minded.
"""

    try:
        # WHAT: Groq API call using Llama 3
        # WHY: llama-3.3-70b is free, fast and very capable
        # HOW: Same structure as OpenAI — Groq is
        #      intentionally OpenAI-compatible!
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=2000,
            messages=[
                {
                    "role": "system",
                    "content": "You are a world-class brand strategist \
and creative director with expertise in global markets."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Brand generation failed: {str(e)}"


# ============================================
# CULTURAL SLOGAN ADAPTER
# ============================================
def adapt_slogan_culturally(slogan, target_language, target_culture):

    client = get_groq_client()

    prompt = f"""
You are a cultural brand adaptation expert.

Original slogan: "{slogan}"
Target language: {target_language}
Target culture/market: {target_culture}

Please provide:
1. DIRECT TRANSLATION - Word for word translation
2. CULTURAL ADAPTATION - A version adapted for this culture
   (may change words but keeps the emotional intent)
3. EXPLANATION - Why you made these adaptation choices
4. CULTURAL NOTES - Any important cultural context to know

Be specific and culturally sensitive.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=800,
            messages=[
                {
                    "role": "system",
                    "content": "You are a cultural brand adaptation \
expert with deep knowledge of global markets."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Cultural adaptation failed: {str(e)}"


# ============================================
# TESTING BLOCK
# ============================================
if __name__ == "__main__":

    print("=" * 55)
    print("   BRAND GENERATOR (Groq/Llama3) - TEST RESULTS")
    print("=" * 55)

    print("\n🏢 TEST 1: Generating Brand Identity...")
    print("-" * 55)

    brand_result = generate_brand_identity(
        company_description="An AI-powered healthcare app that connects \
patients in rural areas with specialist doctors via telemedicine",
        industry="Healthcare Technology",
        target_audience="Rural patients aged 25-60, caregivers, \
and rural healthcare workers",
        brand_values="Accessibility, Trust, Compassion, Innovation",
        target_markets="India, Nigeria, Brazil, Indonesia"
    )
    print(brand_result)

    print("\n\n🌍 TEST 2: Cultural Slogan Adaptation...")
    print("-" * 55)

    adaptation = adapt_slogan_culturally(
        slogan="Healthcare for everyone, everywhere.",
        target_language="Japanese",
        target_culture="Japan"
    )
    print(adaptation)

    print("\n" + "=" * 55)
    print("✅ Brand Generator Test Complete!")
    print("=" * 55)
