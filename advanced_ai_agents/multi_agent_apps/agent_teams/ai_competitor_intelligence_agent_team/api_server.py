"""
============================================================
  Competitor Intelligence SaaS — FastAPI Server
  Drop this file into the same folder as competitor_intel_service.py
  and run: uvicorn api_server:app --reload --port 8000
============================================================
"""

import os
import time
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict
from collections import defaultdict

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
#  SIMPLE IN-MEMORY USER STORE  (replace with a real DB like Supabase later)
# ══════════════════════════════════════════════════════════════════════════════

# Structure: { api_key: { plan, reports_used, reports_limit, email, stripe_customer_id } }
USERS: Dict[str, dict] = {
    # One built-in dev user so you can test immediately
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
    "starter": 10,    # $29/mo
    "pro":     50,    # $79/mo
    "agency":  999999, # $199/mo — unlimited
}

# Simple rate limiter: max 5 requests per minute per API key
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
    allow_origins=["*"],  # Tighten this once you have a real frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ══════════════════════════════════════════════════════════════════════════════
#  AUTH & RATE LIMITING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_current_user(x_api_key: str = Header(..., description="Your API key")):
    """Validate API key and return user record."""
    user = USERS.get(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key. Get one at /register.")
    return {"api_key": x_api_key, **user}


def check_rate_limit(api_key: str):
    """Allow max 5 requests per 60 seconds per key."""
    now = time.time()
    window = 60
    max_requests = 5
    timestamps = rate_limit_store[api_key]
    # Drop timestamps older than the window
    rate_limit_store[api_key] = [t for t in timestamps if now - t < window]
    if len(rate_limit_store[api_key]) >= max_requests:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {max_requests} requests per minute."
        )
    rate_limit_store[api_key].append(now)


def check_quota(user: dict):
    """Ensure user hasn't exceeded their monthly report limit."""
    if user["reports_used"] >= user["reports_limit"]:
        raise HTTPException(
            status_code=402,
            detail=(
                f"Monthly report limit reached ({user['reports_limit']} reports on {user['plan']} plan). "
                "Upgrade at /upgrade."
            )
        )

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
    """Quick health check — confirms the server is running."""
    return {"status": "ok", "version": "1.0.0", "docs": "/docs"}


# ── AUTH ──────────────────────────────────────────────────────────────────────

@app.post("/register", response_model=RegisterResponse, tags=["Auth"])
def register(body: RegisterRequest):
    """
    Create a free account and get an API key.
    Free tier = 3 reports/month on the starter plan.
    Upgrade at /checkout to unlock more.
    """
    # Generate a deterministic but hard-to-guess API key from email + secret
    raw = f"{body.email}:{MASTER_API_KEY}:{time.time()}"
    api_key = "ci_" + hashlib.sha256(raw.encode()).hexdigest()[:32]

    USERS[api_key] = {
        "email":              body.email,
        "plan":               "starter",
        "reports_used":       0,
        "reports_limit":      3,      # Free trial: 3 reports
        "stripe_customer_id": None,
        "created_at":         datetime.utcnow().isoformat(),
    }

    return RegisterResponse(
        api_key=api_key,
        plan="starter",
        message=(
            "Welcome! You have 3 free reports. "
            "POST /analyze with header X-Api-Key to run your first analysis. "
            "Upgrade anytime at /checkout."
        )
    )


# ── CORE PRODUCT ──────────────────────────────────────────────────────────────

@app.post("/analyze", response_model=CompetitorIntelResult, tags=["Intelligence"])
def analyze(
    body: AnalyzeRequest,
    user: dict = Depends(get_current_user),
):
    """
    Run a full competitor intelligence analysis.

    Requires header:  X-Api-Key: your_key_here

    The AI will:
    1. Find up to `max_competitors` competitor URLs
    2. Scrape each competitor's website
    3. Extract pricing, features, tech stack, and more
    4. Generate a strategic analysis report
    """
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    # Increment usage counter
    USERS[user["api_key"]]["reports_used"] += 1

    return result


# ── USAGE ─────────────────────────────────────────────────────────────────────

@app.get("/usage", response_model=UsageResponse, tags=["Account"])
def get_usage(user: dict = Depends(get_current_user)):
    """Check how many reports you've used this month and what plan you're on."""
    return UsageResponse(
        email=user["email"],
        plan=user["plan"],
        reports_used=user["reports_used"],
        reports_limit=user["reports_limit"],
        reports_remaining=max(0, user["reports_limit"] - user["reports_used"]),
    )


# ── STRIPE PAYMENTS ───────────────────────────────────────────────────────────

@app.post("/checkout", tags=["Billing"])
def create_checkout(body: CheckoutRequest, user: dict = Depends(get_current_user)):
    """
    Create a Stripe Checkout session.
    Returns a `checkout_url` — redirect your user there to pay.

    Plans:
      starter  → $29/mo  → 10 reports
      pro      → $79/mo  → 50 reports
      agency   → $199/mo → unlimited
    """
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured. Set STRIPE_SECRET_KEY environment variable."
        )

    price_map = {
        "starter": STRIPE_PRICE_STARTER,
        "pro":     STRIPE_PRICE_PRO,
        "agency":  STRIPE_PRICE_AGENCY,
    }

    price_id = price_map.get(body.plan)
    if not price_id:
        raise HTTPException(status_code=400, detail=f"Unknown plan '{body.plan}'. Choose: starter, pro, agency")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=body.success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=body.cancel_url,
            customer_email=user["email"],
            metadata={"api_key": user["api_key"], "plan": body.plan},
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"checkout_url": session.url, "session_id": session.id}


@app.post("/webhooks/stripe", tags=["Billing"], include_in_schema=False)
async def stripe_webhook(request: Request):
    """
    Stripe sends events here when payments succeed or subscriptions change.
    Configure this URL in your Stripe dashboard → Webhooks.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if not STRIPE_WEBHOOK_SECRET:
        return JSONResponse({"status": "webhook secret not configured"}, status_code=200)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        session  = event["data"]["object"]
        api_key  = session.get("metadata", {}).get("api_key")
        plan     = session.get("metadata", {}).get("plan")

        if api_key and plan and api_key in USERS:
            USERS[api_key]["plan"]           = plan
            USERS[api_key]["reports_limit"]  = PLAN_LIMITS.get(plan, 10)
            USERS[api_key]["reports_used"]   = 0  # Reset on new subscription

    elif event["type"] == "customer.subscription.deleted":
        # Downgrade to free tier when subscription is cancelled
        customer_id = event["data"]["object"].get("customer")
        for key, user in USERS.items():
            if user.get("stripe_customer_id") == customer_id:
                USERS[key]["plan"]          = "starter"
                USERS[key]["reports_limit"] = 3
                break

    return JSONResponse({"status": "ok"})


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRYPOINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
