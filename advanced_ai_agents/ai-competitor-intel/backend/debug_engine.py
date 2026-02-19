import asyncio
import os
from dotenv import load_dotenv
from intelligence_engine import IntelligenceEngine

load_dotenv()

async def debug_engine():
    engine = IntelligenceEngine(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY"),
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )
    
    print("Finding URLs...")
    urls = engine.get_competitor_urls("tavily", url="https://www.firecrawl.dev")
    print(f"Found URLs: {urls}")
    
    if urls:
        print(f"Extracting info for {urls[0]}...")
        data = await engine.extract_competitor_info(urls[0])
        print(f"Result: {data}")
    else:
        print("No URLs found by Tavily.")

if __name__ == "__main__":
    asyncio.run(debug_engine())
