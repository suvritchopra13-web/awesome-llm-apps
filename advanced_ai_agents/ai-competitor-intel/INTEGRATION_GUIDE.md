# 🔗 Bolt Frontend ↔ Python Backend Integration Guide

I have already created the necessary files (`main.py` and `intelligence_engine.py`) to expose your backend as a REST API. Follow these steps to complete the integration.

## Step 1: Install API dependencies
Run this in your `backend` directory:
```bash
python -m pip install -r requirements.txt
```

---

## Step 2: Start the API Server
In a new terminal, run:
```bash
cd backend
python main.py
```
Your API will be live at `http://localhost:8000`. You can verify it by visiting `http://localhost:8000/health`.

---

## Step 3: Configure Bolt Frontend
In your Next.js project (created by Bolt), update your environment variables.

1. Create or edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

2. Locate the "Analyze" function in your frontend and update the fetch call:
```typescript
const handleAnalyze = async () => {
  setIsLoading(true);
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, description })
    });
    
    const result = await response.json();
    
    if (result.status === "success") {
      // result.data.report contains the markdown analysis
      // result.data.competitors contains the extracted cards
      setAnalysisData(result.data);
    }
  } catch (error) {
    console.error("API Error:", error);
  } finally {
    setIsLoading(false);
  }
};
```

---

## Deployment Strategy 🚀
When you are ready to deploy to production:

### 1. Backend (Python API)
- Deploy to **Railway** or **Render**.
- Add your `.env` variables (OPENAI_API_KEY, etc.) in their dashboard.

### 2. Frontend (Next.js)
- Deploy to **Vercel**.
- Add `NEXT_PUBLIC_API_URL` pointing to your Railway/Render URL.

---

### Tips for Success:
- **CORS**: I have enabled "Allow All" (`*`) in `main.py` for easy testing. For production, restrict this to your actual frontend domain.
- **Loading States**: The analysis takes 30-60 seconds (it's crawling sites!). Ensure your Bolt UI has a nice spinner or progress bar.
