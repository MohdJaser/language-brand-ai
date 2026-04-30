# ============================================
# app.py — Upgraded UI Version
# Professional Blue & White | Rich & Colorful
# ============================================

import streamlit as st
from language_detector import detect_language
from translator import translate_text, translate_to_multiple, get_supported_languages
from brand_generator import generate_brand_identity, adapt_slogan_culturally
from website_scraper import scrape_website
from report_generator import generate_localization_report
# from site_generator import generate_website_html
# import streamlit.components.v1 as components

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AI Language & Brand Tool",
    page_icon="🌍",
    layout="wide"
)

# ============================================
# RICH & COLORFUL CSS STYLING
# ============================================
st.markdown("""
    <style>

    /* ── Global Background ── */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 50%, #e8f0fe 100%);
    }

    /* ── Main Header ── */
    .main-header {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #1a73e8, #6c63ff, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.2rem 0 0.3rem 0;
        letter-spacing: -1px;
    }

    /* ── Subtitle ── */
    .sub-header {
        font-size: 1.1rem;
        color: #5f6368;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* ── Feature Cards ── */
    .feature-card {
        background: linear-gradient(135deg, #ffffff, #f0f4ff);
        border: 1.5px solid #d0e1ff;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.1);
    }

    /* ── Result Box (Blue) ── */
    .result-box {
        background: linear-gradient(135deg, #e8f0fe, #f0f4ff);
        border-left: 5px solid #1a73e8;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 12px rgba(26, 115, 232, 0.1);
    }

    /* ── Success Box (Green) ── */
    .success-box {
        background: linear-gradient(135deg, #e6f9f0, #f0fff8);
        border-left: 5px solid #34a853;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 0.8rem 0;
    }

    /* ── Language Badge ── */
    .lang-badge {
        display: inline-block;
        background: linear-gradient(90deg, #1a73e8, #6c63ff);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }

    /* ── Translation Row ── */
    .translation-row {
        background: white;
        border: 1px solid #d0e1ff;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.4rem 0;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 6px rgba(74,144,226,0.07);
    }

    /* ── Sidebar Styling ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    }

    [data-testid="stSidebar"] * {
        color: #e0e8ff !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem 0;
        transition: all 0.2s;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(74, 144, 226, 0.3);
    }

    /* ── Primary Button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #1a73e8, #6c63ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.35) !important;
        transition: all 0.3s !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.5) !important;
    }

    /* ── Metric Cards ── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a73e8, #6c63ff);
        border-radius: 14px;
        padding: 1rem;
        color: white !important;
        box-shadow: 0 4px 15px rgba(26,115,232,0.2);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: white !important;
    }

    /* ── Section Headers ── */
    h2, h3 {
        color: #1a1a2e !important;
        font-weight: 800 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: #d0e1ff !important;
    }

    </style>
""", unsafe_allow_html=True)


# ============================================
# APP HEADER
# ============================================
st.markdown('<p class="main-header">🌍 AI Language & Brand Development Tool</p>',
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Translate content & build global brand identity — powered by Claude AI</p>',
            unsafe_allow_html=True)
st.divider()


# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
# Professional Team Header
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #1a73e8, #6c63ff);
            border-radius: 14px;
            padding: 1.2rem;
            text-align: center;
            margin-bottom: 0.8rem;
        '>
            <div style='font-size: 2.8rem;'>🌐</div>
            <div style='
                color: white;
                font-size: 1.1rem;
                font-weight: 800;
                letter-spacing: 1px;
                margin-top: 0.3rem;
            '>TEAM 03</div>
            <div style='
                color: rgba(255,255,255,0.75);
                font-size: 0.75rem;
                font-weight: 500;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-top: 0.1rem;
            '>AI Project</div>
        </div>
        <div style='
            text-align: center;
            color: rgba(255,255,255,0.4);
            font-size: 0.75rem;
            margin-bottom: 0.8rem;
        '>── Navigation ──</div>
    """, unsafe_allow_html=True)

    feature = st.radio(
        "Select Feature",
        [
            "🔍 Language Detector",
            "🔄 Text Translator",
            "🌐 Batch Translator",
            "🎨 Brand Identity Generator",
            "🎯 Cultural Slogan Adapter",
            "📊 Website Localization Report"
            # "🚀 Instant Site Generator"
        ],
        label_visibility="collapsed"
    )

    # st.markdown("---")
    # st.markdown("**⚡ Powered by:**")
    # st.markdown("🐍 Python &nbsp;|&nbsp; 🤖 Claude AI")
    # st.markdown("🌐 Google Translate &nbsp;|&nbsp; ⚡ Streamlit")
    st.markdown("---")
    st.markdown("🎓 *AI Project Based Learning*")


# ============================================
# FEATURE 1: LANGUAGE DETECTOR
# ============================================
if feature == "🔍 Language Detector":

    st.markdown("## 🔍 Language Detector")
    st.markdown("Paste any text and AI will **instantly identify** its language.")

    # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    text_input = st.text_area(
        "Enter text to detect:",
        placeholder="Type or paste text in any language here...",
        height=150
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Detect Language", type="primary"):
        if text_input.strip():
            with st.spinner("🔍 Analyzing language patterns..."):
                lang_name, lang_code = detect_language(text_input)

            if lang_code == "unknown":
                st.warning(f"⚠️ {lang_name}")
            else:
                st.success("✅ Language Detected!")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    st.metric("🌍 Language", lang_name)
                with col2:
                    st.metric("🔤 Code", lang_code.upper())
                with col3:
                    st.metric("📊 Confidence", "High")
        else:
            st.warning("⚠️ Please enter some text first.")


# ============================================
# FEATURE 2: TEXT TRANSLATOR
# ============================================
elif feature == "🔄 Text Translator":

    st.markdown("## 🔄 Text Translator")
    st.markdown("Translate brand content into any language **instantly.**")

    # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        translate_input = st.text_area(
            "✏️ Text to translate:",
            placeholder="Enter your slogan, tagline, product description...",
            height=150
        )
    with col2:
        target_lang = st.selectbox("🌍 Translate to:", get_supported_languages())
        if translate_input.strip():
            detected, _ = detect_language(translate_input)
            st.info(f"📌 Source: **{detected}**")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 Translate Now", type="primary"):
        if translate_input.strip():
            with st.spinner(f"Translating to {target_lang}..."):
                result = translate_text(translate_input, target_lang)

            st.success("✅ Translation Complete!")
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f"**📝 Original:**\n\n{translate_input}")
            st.markdown(f"**🌍 {target_lang}:**\n\n{result}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter text to translate.")


# ============================================
# FEATURE 3: BATCH TRANSLATOR
# ============================================
elif feature == "🌐 Batch Translator":

    st.markdown("## 🌐 Batch Translator")
    st.markdown("Translate your message into **multiple languages simultaneously.**")

    # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    batch_input = st.text_area(
        "📢 Your brand message:",
        placeholder="E.g: Quality products, delivered with care.",
        height=120
    )

    selected_langs = st.multiselect(
        "🌍 Select target languages:",
        get_supported_languages(),
        default=["French", "Spanish", "Hindi", "German", "Arabic"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🌐 Translate to All Languages", type="primary"):
        if batch_input.strip() and selected_langs:
            with st.spinner(f"🌍 Translating into {len(selected_langs)} languages..."):
                results = translate_to_multiple(batch_input, selected_langs)

            st.success(f"✅ Translated into {len(results)} languages!")
            st.markdown("---")

            for lang, translation in results.items():
                st.markdown('<div class="translation-row">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f'<span class="lang-badge">🌍 {lang}</span>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{translation}**")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter text and select languages.")


# ============================================
# FEATURE 4: BRAND IDENTITY GENERATOR
# ============================================
elif feature == "🎨 Brand Identity Generator":

    st.markdown("## 🎨 Brand Identity Generator")
    st.markdown("Describe your company and Claude AI generates a **complete brand package.**")

    # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        company_desc = st.text_area("🏢 Company Description:", placeholder="What does your company do?", height=100)
        industry = st.text_input("🏭 Industry:", placeholder="E.g: Healthcare, EdTech, E-commerce...")
        target_audience = st.text_input("👥 Target Audience:", placeholder="E.g: Young professionals aged 22-35...")

    with col2:
        brand_values = st.text_input("💎 Brand Values:", placeholder="E.g: Innovation, Trust, Sustainability...")
        target_markets = st.text_input("🌍 Target Markets:", placeholder="E.g: India, USA, Germany, Brazil...")
        # st.markdown("<br>", unsafe_allow_html=True)
        # st.info("💡 Requires Anthropic API credits")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🎨 Generate Brand Identity", type="primary"):
        if all([company_desc, industry, target_audience, brand_values, target_markets]):
            with st.spinner("🤖 Claude AI is crafting your brand identity..."):
                result = generate_brand_identity(
                    company_desc, industry,
                    target_audience, brand_values, target_markets
                )
            st.success("✅ Brand Identity Generated!")
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please fill in all fields.")


# ============================================
# FEATURE 5: CULTURAL SLOGAN ADAPTER
# ============================================
elif feature == "🎯 Cultural Slogan Adapter":

    st.markdown("## 🎯 Cultural Slogan Adapter")
    st.markdown("Go beyond translation — **culturally adapt** your slogan for each market.")

    # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    slogan_input = st.text_input("💬 Your brand slogan:", placeholder="E.g: Innovating the future, today.")

    col1, col2 = st.columns(2)
    with col1:
        adapt_language = st.selectbox("🌍 Target Language:", get_supported_languages())
    with col2:
        adapt_culture = st.text_input("🗺️ Target Culture/Market:", placeholder="E.g: Japan, Brazil...")

    # st.info("💡 Requires Anthropic API credits")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🎯 Adapt Culturally", type="primary"):
        if slogan_input and adapt_culture:
            with st.spinner("🤖 Analyzing cultural context..."):
                result = adapt_slogan_culturally(slogan_input, adapt_language, adapt_culture)
            st.success("✅ Cultural Adaptation Complete!")
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please fill in all fields.")
# ============================================
# FEATURE 6: WEBSITE LOCALIZATION REPORT
# ============================================
elif feature == "📊 Website Localization Report":

    st.markdown("## 📊 Website Localization Report")
    st.markdown("Paste any website URL and get a **complete localization report** for your target market.")

    # st.markdown('<div class="feature-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        website_url = st.text_input(
            "🌐 Website URL:",
            placeholder="E.g: https://www.amazon.com"
        )
    with col2:
        report_lang = st.selectbox(
            "🌍 Target Language:",
            get_supported_languages()
        )
        report_culture = st.text_input(
            "🗺️ Target Market:",
            placeholder="E.g: Saudi Arabia, Japan..."
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📊 Generate Report", type="primary"):
        if website_url and report_culture:
            # STEP 1: Scrape website
            with st.spinner("🔍 Scanning website content..."):
                content, error = scrape_website(website_url)

            if error:
                st.error(error)
            else:
                st.success("✅ Website scanned successfully!")

                # STEP 2: Generate report
                with st.spinner("🤖 Translating & analyzing content..."):
                    report = generate_localization_report(
                        website_url, content,
                        report_lang, report_culture
                    )

                st.success("✅ Report Generated!")
                st.divider()

                # ── REPORT DISPLAY ──

                # Header
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1a73e8, #6c63ff);
                padding: 1.5rem; border-radius: 16px; color: white; margin-bottom: 1rem;'>
                <h2 style='color:white; margin:0;'>🌍 Website Localization Report</h2>
                <p style='margin:0.3rem 0 0 0; opacity:0.85;'>
                {report['url']} → {report['target_language']} 
                ({report['target_culture']})</p>
                <p style='margin:0.3rem 0 0 0; opacity:0.7; font-size:0.85rem;'>
                Generated: {report['generated_at']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Section 1: Page Title
                st.markdown("### 📌 Page Title")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original:**")
                    st.info(content["title"] or "Not found")
                with col2:
                    st.markdown(f"**{report_lang}:**")
                    st.success(
                        report["translated"].get(
                            "title", "N/A"
                        )
                    )

                st.divider()

                # Section 2: Headings
                if report["translated"].get("headings"):
                    st.markdown("### 📝 Headings & Key Messages")
                    for item in report["translated"]["headings"]:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"🔹 {item['original']}")
                        with col2:
                            st.markdown(f"✅ {item['translated']}")
                    st.divider()

                # Section 3: Navigation
                if report["translated"].get("nav_items"):
                    st.markdown("### 🧭 Navigation Menu")
                    cols = st.columns(2)
                    for i, item in enumerate(
                        report["translated"]["nav_items"]
                    ):
                        with cols[i % 2]:
                            st.markdown(
                                f"**{item['original']}** → "
                                f"{item['translated']}"
                            )
                    st.divider()

                # Section 4: Buttons/CTAs
                if report["translated"].get("buttons"):
                    st.markdown("### 🖱️ Buttons & Call-to-Actions")
                    cols = st.columns(3)
                    for i, item in enumerate(
                        report["translated"]["buttons"][:9]
                    ):
                        with cols[i % 3]:
                            st.markdown(
                                f'<div class="result-box">'
                                f'<small>{item["original"]}</small>'
                                f'<br><strong>{item["translated"]}'
                                f'</strong></div>',
                                unsafe_allow_html=True
                            )
                    st.divider()

                # Section 5: Content Paragraphs
                if report["translated"].get("paragraphs"):
                    st.markdown("### 📄 Key Content")
                    for item in report["translated"]["paragraphs"]:
                        with st.expander(
                            f"📌 {item['original'][:60]}..."
                        ):
                            st.markdown(f"**Original:** {item['original']}")
                            st.markdown("---")
                            st.markdown(f"**{report_lang}:** {item['translated']}")
                    st.divider()

                # Section 6: AI Analysis
                st.markdown("### 🤖 AI Cultural Analysis")
                st.markdown(
                    '<div class="result-box">',
                    unsafe_allow_html=True
                )
                st.markdown(report["ai_analysis"])
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("⚠️ Please enter a website URL and target market.")
# ============================================
# FEATURE 7: INSTANT SITE GENERATOR
# ============================================
# elif feature == "🚀 Instant Site Generator":
#     st.markdown("## 🚀 Instant Site Generator")
#     st.markdown("Generate a **culturally-tailored** landing page in seconds.")

#     col1, col2 = st.columns(2)
#     with col1:
#         site_name = st.text_input("🏢 Company Name:")
#         site_industry = st.text_input("🏭 Industry:")
#     with col2:
#         site_lang = st.selectbox("🌍 Site Language:", get_supported_languages())
#         site_culture = st.text_input("🗺️ Target Culture:", placeholder="e.g., Japan, UAE...")
    
#     site_desc = st.text_area("📝 Brief Description:")

#     if st.button("🚀 Generate Website", type="primary"):
#         if site_name and site_culture and site_desc:
#             with st.spinner("🎨 AI is designing your localized website..."):
#                 generated_code = generate_website_html(
#                     site_name, site_industry, site_lang, site_culture, site_desc
#                 )
            
#             st.success("✅ Website Generated Successfully!")
            
#             # --- LIVE PREVIEW ---
#             st.markdown("### 🖥️ Live Preview")
#             components.html(generated_code, height=1200, scrolling=True)
            
#             # --- DOWNLOAD & CODE VIEW ---
#             st.markdown("### 📥 Get the Code")
#             st.download_button(
#                 label="Download index.html",
#                 data=generated_code,
#                 file_name="index.html",
#                 mime="text/html"
#             )
#             with st.expander("View Source Code"):
#                 st.code(generated_code, language="html")
#         else:
#             st.warning("⚠️ Please fill in all fields to generate the site.")
