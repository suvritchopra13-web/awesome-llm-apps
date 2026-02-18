import os
import json
from pathlib import Path
from typing import List, Optional, Literal, Dict, Any

import requests
from pydantic import BaseModel, Field

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.exa import ExaTools
from agno.tools.firecrawl import FirecrawlTools
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from firecrawl import FirecrawlApp


def _load_dotenv_if_present() -> None:
    """
    Load key=value pairs from a local .env file into os.environ when they are
    not already set in the process environment.
    """
    candidate_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent / ".env",
    ]

    seen = set()
    for env_path in candidate_paths:
        resolved = env_path.resolve()
        if resolved in seen or not resolved.exists() or not resolved.is_file():
            continue
        seen.add(resolved)

        for raw_line in resolved.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key:
                continue

            cleaned_value = _normalize_env_value(value)
            if key not in os.environ or not _normalize_env_value(os.environ.get(key)):
                os.environ[key] = cleaned_value


class CompetitorDataSchema(BaseModel):
    company_name: str = Field(description="Name of the company")
    pricing: str = Field(description="Pricing details, tiers, and plans")
    key_features: List[str] = Field(description="Main features and capabilities of the product/service")
    tech_stack: List[str] = Field(description="Technologies, frameworks, and tools used")
    marketing_focus: str = Field(description="Main marketing angles and target audience")
    customer_feedback: str = Field(description="Customer testimonials, reviews, and feedback")


class CompetitorIntelRequest(BaseModel):
    company_url: Optional[str] = Field(None, description="URL of the company to analyze")
    description: Optional[str] = Field(
        None, description="Short description of the company if URL is not available"
    )
    search_engine: Literal["perplexity", "exa"] = Field(
        "exa",
        description="Which search engine to use for competitor discovery. "
        '"perplexity" uses Perplexity AI Sonar Pro, "exa" uses Exa AI.',
    )
    max_competitors: int = Field(
        3, ge=1, le=5, description="Maximum number of competitor URLs to analyze"
    )

    def validate_inputs(self) -> None:
        if not self.company_url and not self.description:
            raise ValueError("Please provide either a company_url or a description.")


class CompetitorIntelResult(BaseModel):
    competitor_urls: List[str]
    competitor_data: List[Dict[str, Any]]
    analysis_report: str


def _normalize_env_value(value: Optional[str]) -> str:
    if value is None:
        return ""
    return value.strip().strip('"').strip("'")


_load_dotenv_if_present()


def _load_required_env(*names: str) -> str:
    for name in names:
        value = _normalize_env_value(os.getenv(name))
        if value:
            return value

    expected = " or ".join(names)
    raise RuntimeError(
        f"Missing required environment variable: {expected}. "
        "Set it before running the service."
    )


def _build_agents(search_engine: str) -> Dict[str, Agent]:
    openai_api_key = _load_required_env("OPENAI_API_KEY")
    firecrawl_api_key = _load_required_env("FIRECRAWL_API_KEY", "FIRECRAWL_API")

    firecrawl_tools = FirecrawlTools(
        api_key=firecrawl_api_key,
        enable_scrape=False,
        enable_crawl=True,
        limit=5,
    )

    if search_engine == "exa":
        exa_api_key = _load_required_env("EXA_API_KEY")
        exa_tools = ExaTools(
            api_key=exa_api_key,
            category="company",
            num_results=3,
        )
        competitor_finder_agent = Agent(
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            tools=[exa_tools],
            debug_mode=False,
            markdown=False,
            instructions=[
                "You are a competitor finder agent. Use ExaTools to find competitor company URLs.",
                "When given a URL, find similar companies. When given a description, search for companies matching that description.",
                "Return ONLY the URLs, one per line, with no additional text.",
            ],
        )
    else:
        competitor_finder_agent = None

    firecrawl_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        tools=[firecrawl_tools, DuckDuckGoTools()],
        debug_mode=False,
        markdown=False,
    )

    analysis_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        debug_mode=False,
        markdown=True,
    )

    return {
        "competitor_finder_agent": competitor_finder_agent,
        "firecrawl_agent": firecrawl_agent,
        "analysis_agent": analysis_agent,
        "firecrawl_api_key": firecrawl_api_key,
    }


def _get_competitor_urls(
    request: CompetitorIntelRequest, competitor_finder_agent: Optional[Agent]
) -> List[str]:
    request.validate_inputs()

    if request.search_engine == "perplexity":
        perplexity_api_key = _load_required_env("PERPLEXITY_API_KEY")
        perplexity_url = "https://api.perplexity.ai/chat/completions"

        content = "Find me competitor company URLs similar to the company with "
        if request.company_url and request.description:
            content += f"URL: {request.company_url} and description: {request.description}"
        elif request.company_url:
            content += f"URL: {request.company_url}"
        else:
            content += f"description: {request.description}"
        content += f". ONLY RESPOND WITH THE URLS, NO OTHER TEXT. Return up to {request.max_competitors} URLs."

        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and only return company URLs ONLY.",
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            "max_tokens": 200,
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {perplexity_api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(perplexity_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        urls_raw = response.json()["choices"][0]["message"]["content"].strip().split("\n")
        urls = [u.strip() for u in urls_raw if u.strip()]
        return urls[: request.max_competitors]

    # Exa AI branch using agno Agent
    if not competitor_finder_agent:
        raise RuntimeError("competitor_finder_agent is not configured for search_engine 'exa'.")

    if request.company_url:
        prompt = (
            "Find competitor company URLs similar to: "
            f"{request.company_url}. Return ONLY the URLs, one per line."
        )
    else:
        prompt = (
            "Find competitor company URLs matching this description: "
            f"{request.description}. Return ONLY the URLs, one per line."
        )

    response: RunOutput = competitor_finder_agent.run(prompt)
    urls = [
        line.strip()
        for line in response.content.strip().split("\n")
        if line.strip() and line.strip().startswith("http")
    ]
    return urls[: request.max_competitors]


def _extract_competitor_info(
    competitor_url: str,
    firecrawl_api_key: str,
) -> Optional[Dict[str, Any]]:
    try:
        app = FirecrawlApp(api_key=firecrawl_api_key)
        url_pattern = f"{competitor_url}/*"

        extraction_prompt = """
        Extract detailed information about the company's offerings, including:
        - Company name and basic information
        - Pricing details, plans, and tiers
        - Key features and main capabilities
        - Technology stack and technical details
        - Marketing focus and target audience
        - Customer feedback and testimonials

        Analyze the entire website content to provide comprehensive information for each field.
        """

        schema = CompetitorDataSchema.model_json_schema()
        response = app.extract(
            [url_pattern],
            prompt=extraction_prompt,
            schema=schema,
        )

        if not getattr(response, "success", False) or not getattr(response, "data", None):
            return None

        extracted_info = response.data

        # Handle both dict and object-like responses defensively
        def _get(field: str, default):
            if isinstance(extracted_info, dict):
                return extracted_info.get(field, default)
            return getattr(extracted_info, field, default)

        competitor_json: Dict[str, Any] = {
            "competitor_url": competitor_url,
            "company_name": _get("company_name", "N/A"),
            "pricing": _get("pricing", "N/A"),
            "key_features": (_get("key_features", []) or [])[:5] or ["N/A"],
            "tech_stack": (_get("tech_stack", []) or [])[:5] or ["N/A"],
            "marketing_focus": _get("marketing_focus", "N/A"),
            "customer_feedback": _get("customer_feedback", "N/A"),
        }

        return competitor_json
    except Exception as exc:
        message = str(exc).lower()
        if "firecrawl" in message and (
            "401" in message
            or "403" in message
            or "unauthorized" in message
            or "forbidden" in message
            or "api key" in message
        ):
            raise RuntimeError(
                "Firecrawl authentication failed. Set FIRECRAWL_API_KEY "
                "(or FIRECRAWL_API) to a valid key."
            ) from exc
        return None


def _generate_analysis_report(
    competitor_data: List[Dict[str, Any]],
    analysis_agent: Agent,
) -> str:
    formatted_data = json.dumps(competitor_data, indent=2)

    report: RunOutput = analysis_agent.run(
        f"""Analyze the following competitor data in JSON format and identify market opportunities to improve my own company:

{formatted_data}

Tasks:
1. Identify market gaps and opportunities based on competitor offerings
2. Analyze competitor weaknesses that we can capitalize on
3. Recommend unique features or capabilities we should develop
4. Suggest pricing and positioning strategies to gain competitive advantage
5. Outline specific growth opportunities in underserved market segments
6. Provide actionable recommendations for product development and go-to-market strategy

Focus on finding opportunities where we can differentiate and do better than competitors.
Highlight any unmet customer needs or pain points we can address.
"""
    )

    return report.content


def run_competitor_intel(request: CompetitorIntelRequest) -> CompetitorIntelResult:
    """
    High-level service function to run the competitor intelligence workflow.

    This function is framework-agnostic and can be called from a FastAPI endpoint,
    a CLI, or any other Python environment. It relies on environment variables
    for API keys.
    """

    agents = _build_agents(request.search_engine)
    competitor_finder_agent: Optional[Agent] = agents["competitor_finder_agent"]
    analysis_agent: Agent = agents["analysis_agent"]
    firecrawl_api_key: str = agents["firecrawl_api_key"]

    competitor_urls = _get_competitor_urls(request, competitor_finder_agent)
    if not competitor_urls:
        raise RuntimeError("No competitor URLs could be discovered for the given inputs.")

    competitor_data: List[Dict[str, Any]] = []
    for url in competitor_urls:
        info = _extract_competitor_info(url, firecrawl_api_key)
        if info is not None:
            competitor_data.append(info)

    if not competitor_data:
        raise RuntimeError(
            "Could not extract data from any discovered competitor URLs. "
            "This may be due to rate limits or site access restrictions."
        )

    analysis_report = _generate_analysis_report(competitor_data, analysis_agent)

    return CompetitorIntelResult(
        competitor_urls=competitor_urls,
        competitor_data=competitor_data,
        analysis_report=analysis_report,
    )


