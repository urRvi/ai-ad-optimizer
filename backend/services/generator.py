import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

AD_SYSTEM = "You are a senior performance marketer. Return strict JSON: {headlines:[], descriptions:[], ctas:[]}"
LP_SYSTEM = "Create LP sections. Return strict JSON with hero_headline, subheadline, bullets, social_proof, faq."

def generate_ads(payload):
    sys = f"{AD_SYSTEM}\nTone:{payload.tone}\nKeywords:{payload.keywords}\nAudience:{payload.audience}\nProduct:{payload.product}\nVariants:{payload.variants}"
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": sys}, {"role":"user","content":"Generate now."}],
        temperature=0.7,
    )
    return resp.choices[0].message.content

def generate_lp():
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": LP_SYSTEM}],
        temperature=0.6,
    )
    return resp.choices[0].message.content
