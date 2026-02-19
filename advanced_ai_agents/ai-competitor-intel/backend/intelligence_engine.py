from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.exa import ExaTools
from agno.tools.firecrawl import FirecrawlTools
from agno.models.openai import OpenAIChat
import pandas as pd
import requests
from firecrawl import AsyncFirecrawlApp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field
from typing import List, Optional
import json

# Handle optional DuckDuckGoTools
try:
    from agno.tools.duckduckgo import DuckDuckGoTools
    DDG_AVAILABLE = True
except ImportError:
    DDG_AVAILABLE = False
    class DuckDuckGoTools:
        def __init__(self, *args, **kwargs):
            pass

class CompetitorDataSchema(BaseModel):
    company_name: str = Field(description="Name of the company")
    pricing: str = Field(description="Pricing details, tiers, and plans")
    estimated_monthly_cost: float = Field(description="Estimated entry-level monthly cost in USD (numeric only)")
    market_tier: str = Field(description="Market position: Leader, Challenger, or Niche Player")
    key_features: List[str] = Field(description="Main features and capabilities")
    tech_stack: List[str] = Field(description="Technologies and platforms used")
    marketing_focus: str = Field(description="Main marketing angles")
    target_audience: str = Field(description="Primary user segments")
    social_proof: str = Field(description="Trust signals: Customer logos, user counts, or ratings")
    swot_strengths: List[str] = Field(description="Top 3 tactical strengths")
    swot_weaknesses: List[str] = Field(description="Top 3 tactical weaknesses")

class IntelligenceEngine:
    def __init__(self, openai_api_key: str, firecrawl_api_key: str, 
                 tavily_api_key: Optional[str] = None, 
                 perplexity_api_key: Optional[str] = None,
                 exa_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.firecrawl_api_key = firecrawl_api_key
        self.tavily_api_key = tavily_api_key
        self.perplexity_api_key = perplexity_api_key
        self.exa_api_key = exa_api_key
        
        # Primary model for complex analysis
        self.model = OpenAIChat(id="gpt-4o", api_key=openai_api_key)
        # Fast model for search and initial data processing
        self.fast_model = OpenAIChat(id="gpt-4o-mini", api_key=openai_api_key)
        
        self.firecrawl_tools = FirecrawlTools(
            api_key=firecrawl_api_key,
            enable_scrape=False,
            enable_crawl=True,
            limit=5
        )

        # Initialize agents
        self.firecrawl_tools_list = [self.firecrawl_tools]
        if DDG_AVAILABLE:
            self.firecrawl_tools_list.append(DuckDuckGoTools())

        self.firecrawl_agent = Agent(
            model=self.model,
            tools=self.firecrawl_tools_list,
            debug_mode=True,
            markdown=True
        )

        self.analysis_agent = Agent(
            model=self.model,
            debug_mode=True,
            markdown=True
        )

        # Aggressive Domain blacklist to filter out directories/profiles/review sites
        self.blacklist = [
            "g2.com", "capterra.com", "crunchbase.com", "linkedin.com", 
            "trustradius.com", "topdesignfirms.com", "clutch.co", 
            "upcity.com", "sortlist.com", "themanifest.com", "builtwith.com",
            "facebook.com", "twitter.com", "instagram.com", "youtube.com",
            "zoominfo.com", "tracxn.com", "pitchbook.com", "apollo.io",
            "owler.com", "glassdoor.com", "indeed.com", "yelp.com",
            "getlatka.com", "myalice.ai", "theorg.com", "similarweb.com",
            "semrush.com", "ahrefs.com", "crozdesk.com", "softwareadvice.com",
            "getapp.com", "financesonline.com", "goodfirms.co", "quora.com",
            "reddit.com", "tracxn.com", "zoominfo.com"
        ]

    def filter_competitor_urls(self, urls: list[str]) -> list[str]:
        """Filters out non-company websites like directories or social media."""
        filtered = []
        for url in urls:
            clean_url = url.lower().strip()
            if not clean_url.startswith("http"):
                continue
            
            # Simple domain check
            domain = clean_url.split("//")[-1].split("/")[0]
            if any(black_domain in domain for black_domain in self.blacklist):
                continue
                
            # Filter out search-specific pages, profiles, or lists
            path_blacklist = [
                "/company/", "/products/", "/reviews/", "/alternatives/", 
                "/vs/", "/competitors/", "/top-", "/best-", "/agencies/",
                "/software/", "/platform/", "/category/"
            ]
            if any(path in clean_url for path in path_blacklist):
                 # Skip deep paths in directory-like structures
                 if clean_url.count("/") > 3:
                    continue

            filtered.append(url)
        return filtered

    def get_competitor_urls(self, search_engine: str, url: str = None, description: str = None) -> list[str]:
        if not url and not description:
            raise ValueError("Please provide either a URL or a description.")

        search_engine = search_engine.lower()
        instructions = [
            "You are a market research expert.",
            "Find 3 direct competitor company homepages (e.g., 'https://competitor.com').",
            "ABSOLUTELY AVOID directory sites, social media, or review pages.",
            "If you find a directory list (like 'Top 10 Agencies'), extract the actual company website URLs from that list.",
            "Return ONLY the direct official website homepages.",
            "Return one URL per line, strictly NO other text."
        ]

        if "duckduckgo" in search_engine:
            if not DDG_AVAILABLE:
                return []
            try:
                content = f"Find 3 direct competitor company websites for: URL: {url}, Description: {description}."
                search_agent = Agent(
                    model=self.fast_model,
                    tools=[DuckDuckGoTools()],
                    instructions=instructions,
                    show_tool_calls=True,
                    markdown=True
                )
                response: RunOutput = search_agent.run(content)
                urls = [line.strip() for line in response.content.strip().split('\n') 
                       if line.strip() and line.strip().startswith('http')]
                return self.filter_competitor_urls(urls)[:3]
            except Exception:
                return []
        
        elif "tavily" in search_engine:
            try:
                from tavily import TavilyClient
                tavily_client = TavilyClient(api_key=self.tavily_api_key)
                # Advanced search to get snippets for the agent to analyze
                query = f"top direct competitors of {url or description} official websites -site:g2.com -site:clutch.co"
                search_results = tavily_client.search(query=query, search_depth="advanced", max_results=10)
                
                # Use Agent to process Tavily results and find homepages
                context = json.dumps(search_results.get('results', []), indent=2)
                processing_agent = Agent(
                    model=self.fast_model,
                    instructions=instructions,
                    markdown=True
                )
                analyze_prompt = f"Based on these search results, identify the official homepages of the top 3 direct competitors:\n{context}"
                response: RunOutput = processing_agent.run(analyze_prompt)
                
                urls = [line.strip() for line in response.content.strip().split('\n') 
                       if line.strip() and line.strip().startswith('http')]
                return self.filter_competitor_urls(urls)[:3]
            except Exception as e:
                print(f"Tavily Agent Discovery failed: {e}")
                return []
        
        elif "exa" in search_engine:
            try:
                if not self.exa_api_key:
                    return []
                
                query = f"Official websites of direct competitors to {url or description}"
                exa_agent = Agent(
                    model=self.model,
                    tools=[ExaTools(api_key=self.exa_api_key)],
                    instructions=instructions
                )
                response = exa_agent.run(query)
                urls = [line.strip() for line in response.content.strip().split('\n') 
                       if line.strip() and line.strip().startswith('http')]
                return self.filter_competitor_urls(urls)[:3]
            except Exception:
                return []
        
        # Add other search engines as needed...
        return []

    async def free_scrape(self, url: str) -> Optional[str]:
        """
        Scrapes a URL for free using Jina Reader (API-less) or local BeautifulSoup.
        Returns cleaned markdown-like text.
        """
        # Method 1: Jina Reader (Best for LLMs, Free)
        try:
            jina_url = f"https://r.jina.ai/{url}"
            headers = {"X-Return-Format": "markdown"}
            # Jina is very generous and works without a key
            response = requests.get(jina_url, headers=headers, timeout=15)
            if response.status_code == 200 and len(response.text) > 200:
                print(f"Jina Reader success for {url}")
                return response.text
        except Exception as e:
            print(f"Jina Reader failed: {e}")

        # Method 2: Local Requests + BeautifulSoup (100% Free/Local)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                import html2text
                
                soup = BeautifulSoup(response.text, 'html.parser')
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Convert to markdown
                h = html2text.HTML2Text()
                h.ignore_links = True
                markdown = h.handle(str(soup))
                print(f"Local BeautifulSoup success for {url}")
                return markdown
        except Exception as e:
            print(f"Local scrape failed for {url}: {e}")
            
        return None

    async def extract_competitor_info(self, competitor_url: str) -> Optional[dict]:
        """
        Extracts structured data using a multi-stage approach (Free -> Paid Fallback).
        """
        context = ""
        
        # 1. Try Free Scrape first (Jina/BS4)
        print(f"Attempting free scrape for {competitor_url}...")
        context = await self.free_scrape(competitor_url)
        
        # 2. If free scrape failed, try Firecrawl (if key exists)
        if not context and self.firecrawl_api_key:
            try:
                print(f"Free scrape limited. Trying Firecrawl for {competitor_url}...")
                app = AsyncFirecrawlApp(api_key=self.firecrawl_api_key)
                response = await app.extract(
                    [f"{competitor_url}/*"],
                    prompt="Extract company details, pricing, features, and SWOT.",
                    schema=CompetitorDataSchema.model_json_schema()
                )
                if response.success and response.data:
                    # Map Firecrawl response to our format
                    data = response.data
                    return self._map_to_standard_format(competitor_url, data)
            except Exception as e:
                print(f"Firecrawl failed: {e}")

        # 3. Last Resort: Tavily Search Context (Always works, uses search snippets)
        if not context:
            print(f"Scraping blocked. Falling back to Tavily search context for {competitor_url}...")
            try:
                from tavily import TavilyClient
                tavily_client = TavilyClient(api_key=self.tavily_api_key)
                domain = competitor_url.replace("https://", "").replace("http://", "").split("/")[0]
                search_query = f"{competitor_url} {domain} company details pricing features tech stack"
                tav_response = tavily_client.search(query=search_query, search_depth="advanced")
                context = "\n".join([f"Source: {r.get('url')}\nContent: {r.get('content')}" for r in tav_response.get('results', [])])
            except Exception as e:
                print(f"Tavily fallback failed: {e}")

        # 4. If we have context (either from Free Scrape or Tavily), use LLM to extract
        if context:
            try:
                analysis_prompt = f"""
                Extract structured information from this context about {competitor_url}.
                Context:
                {context[:10000]}  # Cap at 10k chars for efficiency
                
                Return a JSON object with: company_name, pricing, estimated_monthly_cost, 
                market_tier, key_features (list), tech_stack (list), marketing_focus, 
                target_audience, social_proof, swot_strengths (3 max), swot_weaknesses (3 max).
                
                Return ONLY raw JSON.
                """
                llm_response: RunOutput = self.analysis_agent.run(analysis_prompt)
                content = llm_response.content.strip()
                
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                data = json.loads(content)
                return self._map_to_standard_format(competitor_url, data)
            except Exception as e:
                print(f"LLM Extraction failed for {competitor_url}: {e}")

        return None

    def _map_to_standard_format(self, url: str, data: dict) -> dict:
        """Helper to ensure consistent data structure."""
        return {
            "competitor_url": url,
            "company_name": data.get('company_name', 'N/A'),
            "pricing": data.get('pricing', 'N/A'),
            "estimated_monthly_cost": data.get('estimated_monthly_cost', 0.0),
            "market_tier": data.get('market_tier', 'Niche Player'),
            "key_features": data.get('key_features', [])[:5],
            "tech_stack": data.get('tech_stack', [])[:5],
            "marketing_focus": data.get('marketing_focus', 'N/A'),
            "target_audience": data.get('target_audience', 'General'),
            "social_proof": data.get('social_proof', 'N/A'),
            "swot_strengths": data.get('swot_strengths', [])[:3],
            "swot_weaknesses": data.get('swot_weaknesses', [])[:3]
        }

    def generate_analysis_report(self, competitor_data: list) -> str:
        formatted_data = json.dumps(competitor_data, indent=2)
        report: RunOutput = self.analysis_agent.run(
            f"""Analyze the following competitor data and identify market opportunities:
            {formatted_data}
            1. Identify market gaps
            2. Analyze weaknesses
            3. Recommend features
            4. Suggest pricing/positioning
            """
        )
        return report.content
