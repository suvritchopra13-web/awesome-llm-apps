import os
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from intelligence_engine import IntelligenceEngine

class CompetitorIntelRequest(BaseModel):
    company_url: Optional[str] = None
    description: Optional[str] = None
    search_engine: str = "exa"
    max_competitors: int = 3

class CompetitorIntelResult(BaseModel):
    competitors: List[dict]
    analysis_report: str

def run_competitor_intel(request: CompetitorIntelRequest) -> CompetitorIntelResult:
    """
    Synchronous wrapper for the intelligence engine to match api_server expectations.
    """
    # Initialize engine with environment variables
    engine = IntelligenceEngine(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY"),
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
        exa_api_key=os.getenv("EXA_API_KEY")
    )

    # 1. Get competitor URLs
    urls = engine.get_competitor_urls(request.search_engine, request.company_url, request.description)
    if not urls:
        return CompetitorIntelResult(competitors=[], analysis_report="No competitors found.")

    # 2. Extract competitor info (Async)
    async def get_data():
        tasks = [engine.extract_competitor_info(url) for url in urls[:request.max_competitors]]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]

    # Create a wrapper to run async in sync
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    competitor_data = loop.run_until_complete(get_data())

    if not competitor_data:
        return CompetitorIntelResult(competitors=[], analysis_report="Failed to extract data from competitors.")

    # 3. Generate Report
    report = engine.generate_analysis_report(competitor_data)

    return CompetitorIntelResult(
        competitors=competitor_data,
        analysis_report=report
    )
