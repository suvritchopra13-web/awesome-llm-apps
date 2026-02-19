"""
============================================================
  Competitor Intelligence SaaS — FastAPI Server
  Run: uvicorn api_server:app --reload --port 8000
============================================================
"""

import os
import time
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import stripe
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ── Import your existing service ──────────────────────────────────────────────
from competitor_intel_service import (
    CompetitorIntelRequest,
    CompetitorIntelResult,
    run_competitor_intel,
)

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG  —  set these as environment variables before running
# ══════════════════════════════════════════════════════════════════════════════

STRIPE_SECRET_KEY        = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET    = os.getenv("STRIPE_WEBHOOK_SECRET", "")
MASTER_API_KEY           = os.getenv("MASTER_API_KEY", "dev-master-key-change-me")

# Stripe Price IDs — create these in your Stripe dashboard
STRIPE_PRICE_STARTER     = os.getenv("STRIPE_PRICE_STARTER", "price_starter_id_here")
STRIPE_PRICE_PRO         = os.getenv("STRIPE_PRICE_PRO", "price_pro_id_here")
STRIPE_PRICE_AGENCY      = os.getenv("STRIPE_PRICE_AGENCY", "price_agency_id_here")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# ══════════════════════════════════════════════════════════════════════════════
#  SIMPLE IN-MEMORY USER STORE
# ══════════════════════════════════════════════════════════════════════════════

USERS: Dict[str, dict] = {
    "dev-master-key-change-me": {
        "email":               "dev@localhost",
        "plan":                "agency",
        "reports_used":        0,
        "reports_limit":       999999,
        "stripe_customer_id":  None,
        "created_at":          datetime.utcnow().isoformat(),
    }
}

PLAN_LIMITS = {
    "starter": 10,
    "pro":     50,
    "agency":  999999,
}

rate_limit_store: Dict[str, list] = defaultdict(list)

# ══════════════════════════════════════════════════════════════════════════════
#  APP SETUP
# ══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Competitor Intelligence API",
    description="AI-powered competitor research. Find competitors, scrape their sites, and generate strategic insights.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ══════════════════════════════════════════════════════════════════════════════
#  AUTH & RATE LIMITING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_current_user(x_api_key: str = Header(..., description="Your API key")):
    user = USERS.get(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key. Get one at /register.")
    return {"api_key": x_api_key, **user}


def check_rate_limit(api_key: str):
    now = time.time()
    window = 60
    max_requests = 5
    timestamps = rate_limit_store[api_key]
    rate_limit_store[api_key] = [t for t in timestamps if now - t < window]
    if len(rate_limit_store[api_key]) >= max_requests:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {max_requests} requests per minute."
        )
    rate_limit_store[api_key].append(now)


def check_quota(user: dict):
    if user["reports_used"] >= user["reports_limit"]:
        raise HTTPException(
            status_code=402,
            detail=(
                f"Monthly report limit reached ({user['reports_limit']} reports on {user['plan']} plan). "
                "Upgrade at /upgrade."
            )
        )
    user["reports_used"] += 1

# ══════════════════════════════════════════════════════════════════════════════
#  REQUEST / RESPONSE MODELS
# ══════════════════════════════════════════════════════════════════════════════

class RegisterRequest(BaseModel):
    email: str = Field(..., description="Your email address")

class RegisterResponse(BaseModel):
    api_key: str
    plan:    str
    message: str

class AnalyzeRequest(BaseModel):
    company_url:     Optional[str] = Field(None,  description="URL of the company to analyze")
    description:     Optional[str] = Field(None,  description="Short description if URL is unavailable")
    search_engine:   str           = Field("exa", description="'exa' or 'perplexity'")
    max_competitors: int           = Field(3, ge=1, le=5)

class UsageResponse(BaseModel):
    email:          str
    plan:           str
    reports_used:   int
    reports_limit:  int
    reports_remaining: int

class CheckoutRequest(BaseModel):
    plan:         str = Field(..., description="starter | pro | agency")
    success_url:  str = Field(..., description="Redirect URL after successful payment")
    cancel_url:   str = Field(..., description="Redirect URL if user cancels")

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "version": "1.0.0", "docs": "/docs"}

@app.post("/register", response_model=RegisterResponse, tags=["Auth"])
def register(body: RegisterRequest):
    raw = f"{body.email}:{MASTER_API_KEY}:{time.time()}"
    api_key = "ci_" + hashlib.sha256(raw.encode()).hexdigest()[:32]

    USERS[api_key] = {
        "email":              body.email,
        "plan":               "starter",
        "reports_used":       0,
        "reports_limit":      3,
        "stripe_customer_id": None,
        "created_at":         datetime.utcnow().isoformat(),
    }

    return RegisterResponse(
        api_key=api_key,
        plan="starter",
        message="Welcome! You have 3 free reports. POST /analyze with header X-Api-Key."
    )

@app.post("/analyze", response_model=CompetitorIntelResult, tags=["Intelligence"])
def analyze(
    body: AnalyzeRequest,
    user: dict = Depends(get_current_user),
):
    check_rate_limit(user["api_key"])
    check_quota(user)

    request = CompetitorIntelRequest(
        company_url=body.company_url,
        description=body.description,
        search_engine=body.search_engine,
        max_competitors=body.max_competitors,
    )

    try:
        result = run_competitor_intel(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/usage", response_model=UsageResponse, tags=["Account"])
def get_usage(user: dict = Depends(get_current_user)):
    return UsageResponse(
        email=user["email"],
        plan=user["plan"],
        reports_used=user["reports_used"],
        reports_limit=user["reports_limit"],
        reports_remaining=max(0, user["reports_limit"] - user["reports_used"]),
    )

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
