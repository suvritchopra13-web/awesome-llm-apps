from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import traceback

from competitor_agent_team import run_competitor_analysis

app = FastAPI(title="Competitor Intelligence API")

class AnalysisRequest(BaseModel):
company_url: str | None = None
description: str | None = None
search_engine: str = "Exa AI"
openai_api_key: str
firecrawl_api_key: str
exa_api_key: str | None = None
perplexity_api_key: str | None = None

@app.get("/")
def health():
return {"status": "ok"}

@app.post("/analyze")
async def analyze(req: AnalysisRequest):
try:
result = run_competitor_analysis(
company_url=req.company_url,
description=req.description,
search_engine_choice=req.search_engine,
openai_api_key=req.openai_api_key,
firecrawl_api_key=req.firecrawl_api_key,
exa_api_key=req.exa_api_key or "",
perplexity_api_key=req.perplexity_api_key or "",
)
return result

```
except Exception as e:
    traceback.print_exc()
    return {"error": str(e)}
```

if **name** == "**main**":
uvicorn.run(app, host="0.0.0.0", port=8000)
