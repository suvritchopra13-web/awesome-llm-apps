from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from intelligence_engine import IntelligenceEngine

# Load API keys from .env
load_dotenv()

app = FastAPI(title="AI Competitor Intelligence API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Intelligence Engine using environment variables
engine = IntelligenceEngine(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY"),
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
    exa_api_key=os.getenv("EXA_API_KEY")
)

class AnalysisRequest(BaseModel):
    url: Optional[str] = None
    description: Optional[str] = None
    search_engine: Optional[str] = "🌟 Tavily AI (Free Tier - 1000/month)"

import asyncio

@app.post("/analyze")
async def analyze(req: AnalysisRequest):
    if not req.url and not req.description:
        raise HTTPException(status_code=400, detail="Either URL or Description must be provided")
    
    try:
        # 1. Get competitor URLs
        urls = engine.get_competitor_urls(req.search_engine, req.url, req.description)
        if not urls:
            return {"status": "error", "message": "No competitors found"}

        # 2. Extract competitor info IN PARALLEL
        tasks = [engine.extract_competitor_info(c_url) for c_url in urls]
        extracted_results = await asyncio.gather(*tasks)
        
        # Filter out failed extractions
        competitor_data = [info for info in extracted_results if info]

        if not competitor_data:
            return {"status": "error", "message": "Failed to extract data from competitors"}

        # 3. Generate final report
        report = engine.generate_analysis_report(competitor_data)

        return {
            "status": "success",
            "data": {
                "competitors": competitor_data,
                "report": report
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
