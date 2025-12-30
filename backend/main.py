import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import init, get_session
from models import Generation
from schemas import GenerateIn, GenerateOut, Variant
from services.generator import generate_ads, generate_lp

app = FastAPI(title="AI Ad Optimizer API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init()

@app.post("/generate", response_model=GenerateOut)
def generate(payload: GenerateIn):
    # generate ads
    ads_json = generate_ads(payload)
    try:
        ads = json.loads(ads_json)
    except Exception:
        raise HTTPException(500, "Model did not return JSON")

    variants = []
    for i in range(min(payload.variants, len(ads.get("headlines", [])))):
        variants.append(Variant(
            headline=ads["headlines"][i],
            description=ads.get("descriptions", [""])[i] if i < len(ads.get("descriptions", [])) else "",
            cta=ads.get("ctas", ["Learn More"])[i] if i < len(ads.get("ctas", [])) else "Learn More",
        ))

    landing = None
    if payload.include_lp:
        try:
            landing = json.loads(generate_lp())
        except Exception:
            landing = None

    # persist
    from db import get_session
    with get_session() as s:
        gen = Generation(
            product=payload.product, audience=payload.audience, tone=payload.tone,
            keywords=payload.keywords, prompt="", output_json=json.dumps({"variants":[v.model_dump() for v in variants], "landing": landing}),
            model="openai",
        )
        s.add(gen); s.commit(); s.refresh(gen)
        gid = gen.id

    return GenerateOut(variants=variants, landing=landing, id=gid)
