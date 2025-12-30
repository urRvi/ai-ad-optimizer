import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

st.set_page_config(page_title="AI Ad & LP Optimizer", layout="wide")
st.title("AI‑Driven Ad Copy & Landing Page Optimizer")

with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Creativity", 0.0, 1.0, 0.6, 0.1)
    num_variants = st.selectbox("# Variants", [3, 5, 7], index=1)
    include_lp = st.checkbox("Generate Landing Page Sections", value=True)

col1, col2 = st.columns(2)
with col1:
    product = st.text_input("Product / Offer", placeholder="Premium car‑care kit")
    audience = st.text_input("Target Audience", placeholder="First‑time car buyers in Tier‑1 cities")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Luxury", "Playful", "Urgent"])
    keywords = st.text_input("Keywords (comma‑sep)", placeholder="fast delivery, warranty, EMI")

with col2:
    pain = st.text_area("Customer Pain Points", placeholder="Confused about add‑ons, fear of overpaying, busy schedules")
    usp = st.text_area("Your Unique Value Proposition", placeholder="Transparent pricing, doorstep service, 24x7 support")
    cta = st.text_input("Primary CTA", placeholder="Book a free inspection")

if st.button("Generate"):
    if not product or not audience:
        st.error("Please fill Product and Audience.")
        st.stop()

    sys_prompt = f"""        You are a senior performance marketer. Create high‑converting ad copy variants for Meta/Google Ads.
    Constraints: 30‑character headlines max (where applicable), punchy CTAs, avoid clickbait, keep brand‑safe language.
    Return JSON with keys: headlines, descriptions, ctas. Each should be an array of strings. 
    Style: {tone}. Keywords to weave in: {keywords}.
    Context:\nAudience: {audience}\nProduct: {product}\nPain: {pain}\nUSP: {usp}\nPrimary CTA: {cta}
    Variants: {num_variants}
    """

    start = time.time()
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": "Generate variants now as *strict JSON without markdown formatting, code blocks or triple backticks.*"}

        ],
    )
    content = resp.choices[0].message.content

    # Very light JSON guard – fallback to text table if parsing fails
    import json
    try:
        data = json.loads(content)
    except Exception:
        st.warning("Model did not return strict JSON; rendering raw output below.")
        st.code(content)
        st.stop()

    st.subheader("Ad Variants")
    df_rows = []
    for i in range(min(num_variants, len(data.get("headlines", [])))):
        df_rows.append({
            "variant": i+1,
            "headline": data.get("headlines", [""])[i],
            "description": data.get("descriptions", [""])[i] if i < len(data.get("descriptions", [])) else "",
            "cta": data.get("ctas", [cta])[i] if i < len(data.get("ctas", [])) else cta,
        })
    df = pd.DataFrame(df_rows)
    st.dataframe(df, width='stretch')

    if include_lp:
        lp_prompt = f"""            Create landing page sections for the same campaign.
        Return JSON with keys: hero_headline, subheadline, bullets (3‑5), social_proof (1‑2 lines), faq (2‑3 Q&A).
        Keep copy concise and conversion‑oriented.
        """
        lp_resp = client.chat.completions.create(
            model=MODEL,
            temperature=temperature,
            messages=[{"role": "system", "content": lp_prompt}],
        )
        try:
            lp = json.loads(lp_resp.choices[0].message.content)
        except Exception:
            lp = {"raw": lp_resp.choices[0].message.content}
        st.subheader("Landing Page Sections")
        st.json(lp)

    st.caption(f"Generated in {time.time() - start:.2f}s | Model: {MODEL}")

    # Export
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), file_name="ad_variants.csv")
