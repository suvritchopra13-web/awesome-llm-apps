import asyncio
import os
import json
from dotenv import load_dotenv
from intelligence_engine import IntelligenceEngine

load_dotenv()

async def debug_llm():
    engine = IntelligenceEngine(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY"),
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )
    
    prompt = "Return a JSON object with a key 'test' and value 'success'. Return ONLY JSON."
    print("Testing LLM run...")
    try:
        response = engine.analysis_agent.run(prompt)
        print(f"LLM Response Content: '{response.content}'")
    except Exception as e:
        print(f"LLM Run Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_llm())
