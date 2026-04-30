# ============================================
# report_generator.py
# PURPOSE: Generate localization report
# using AI translation + cultural adaptation
# ============================================

import os
from groq import Groq
from dotenv import load_dotenv
from translator import translate_text
from datetime import datetime

load_dotenv()


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found!")
    return Groq(api_key=api_key)


def generate_cultural_analysis(
    content, target_language, target_culture
):
    """
    WHAT: Uses Groq AI to analyze content
          and provide cultural recommendations
    WHY: Pure translation isn't enough —
         we need cultural intelligence too
    """
    client = get_groq_client()

    # Build a summary of scraped content
    headings_text = "\n".join(
        content["headings"][:5]
    ) or "Not found"
    paragraphs_text = "\n".join(
        content["paragraphs"][:3]
    ) or "Not found"

    prompt = f"""
You are an expert in global brand localization 
and cultural adaptation.

A company wants to expand to {target_culture} 
and needs their website localized into {target_language}.

WEBSITE DETAILS:
- Title: {content['title']}
- Main Headings: {headings_text}
- Key Content: {paragraphs_text}

Please provide a localization analysis with:

1. CULTURAL FIT SCORE (out of 10)
   - How well does the current content suit {target_culture}?
   - Brief explanation

2. TOP 3 CULTURAL RECOMMENDATIONS
   - Specific actionable advice for {target_culture} market

3. ADAPTED TAGLINE
   - Take the website title/heading and create a 
     culturally adapted version in {target_language}
   - Explain your adaptation

4. TONE GUIDELINES FOR {target_culture.upper()}
   - What communication style works best?
   - Words/phrases to use and avoid

5. MARKET ENTRY TIPS
   - 3 specific tips for entering {target_culture} market

Keep response clear, specific and actionable.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            messages=[
                {
                    "role": "system",
                    "content": "You are a global brand localization expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"


def generate_localization_report(
    url, content, target_language,
    target_culture
):
    """
    WHAT: Builds the complete localization report
    WHY: Combines translation + AI analysis
         into one comprehensive document
    HOW: Translates each content section,
         gets AI recommendations, structures
         everything into a clean report dict
    """

    report = {
        "url": url,
        "target_language": target_language,
        "target_culture": target_culture,
        "generated_at": datetime.now().strftime(
            "%B %d, %Y at %I:%M %p"
        ),
        "original": content,
        "translated": {},
        "ai_analysis": ""
    }

    # TRANSLATE each content section
    translated = {}

    # Translate title
    if content["title"]:
        translated["title"] = translate_text(
            content["title"], target_language
        )

    # Translate headings
    translated["headings"] = []
    for h in content["headings"]:
        translated["headings"].append({
            "original": h,
            "translated": translate_text(h, target_language)
        })

    # Translate paragraphs
    translated["paragraphs"] = []
    for p in content["paragraphs"]:
        translated["paragraphs"].append({
            "original": p,
            "translated": translate_text(p, target_language)
        })

    # Translate buttons/CTAs
    translated["buttons"] = []
    for b in content["buttons"]:
        translated["buttons"].append({
            "original": b,
            "translated": translate_text(b, target_language)
        })

    # Translate nav items
    translated["nav_items"] = []
    for n in content["nav_items"]:
        translated["nav_items"].append({
            "original": n,
            "translated": translate_text(n, target_language)
        })

    report["translated"] = translated

    # GET AI CULTURAL ANALYSIS
    report["ai_analysis"] = generate_cultural_analysis(
        content, target_language, target_culture
    )

    return report

