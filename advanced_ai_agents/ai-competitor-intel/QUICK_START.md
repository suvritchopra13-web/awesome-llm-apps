# 🚀 Quick Start Guide - FREE Setup (No Perplexity Needed!)

## ✅ Easiest Option: DuckDuckGo (100% Free)

Since you can't get Perplexity API key, use **DuckDuckGo** - it's completely FREE and requires NO API key!

### Steps:

#### 1. Setup Backend

```bash
cd backend

# Install Python dependencies
python -m pip install -r requirements.txt

# Create .env file
copy .env.example .env
notepad .env
```

#### 2. Add ONLY These API Keys to `.env`:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
FIRECRAWL_API_KEY=your-firecrawl-key-here
```

**That's it!** You don't need Perplexity, Exa, or Tavily.

#### 3. Run the App

```bash
streamlit run competitor_agent_team.py
```

#### 4. In Streamlit UI:
1. Select **"🆓 DuckDuckGo (100% Free)"** from dropdown
2. Enter your OpenAI and Firecrawl API keys in the sidebar
3. Enter a competitor URL or business description
4. Click "Analyze Competitors"

---

## 🌟 Better Option: Tavily AI (Free Tier)

For higher quality results, get Tavily's **free tier** (1,000 searches/month):

### Steps:

1. **Sign up for Tavily:**
   - Go to [https://tavily.com](https://tavily.com)
   - Sign up (completely free)
   - Get your API key (1,000 searches/month free)

2. **Install Tavily:**
   ```bash
   python -m pip install tavily-python
   ```

3. **Add to `.env`:**
   ```bash
   OPENAI_API_KEY=sk-your-key
   FIRECRAWL_API_KEY=your-key
   TAVILY_API_KEY=tvly-your-key-here
   ```

4. **In Streamlit:** Select **"🌟 Tavily AI (Free Tier - 1000/month)"**

---

## 📋 What You Need

### Always Required:
- ✅ **OpenAI API Key** - Get free credits at [platform.openai.com](https://platform.openai.com/api-keys)
- ✅ **Firecrawl API Key** - Free tier at [firecrawl.dev](https://www.firecrawl.dev/app/api-keys)

### Choose ONE Search Option:

| Option | Cost | Quality | API Key Needed? | Setup Time |
|--------|------|---------|-----------------|------------|
| **🆓 DuckDuckGo** | FREE | Good | ❌ NO | 0 min |
| **🌟 Tavily** | FREE | Very Good | ✅ Yes (free) | 2 min |
| Perplexity | $20/mo | Excellent | ✅ Yes (paid) | 5 min |
| Exa | $20/mo | Excellent | ✅ Yes (paid) | 5 min |

---

## 💡 Recommended Setup (Budget: $0)

1. **Use DuckDuckGo** (free, no signup)
2. **Get Tavily** as backup (free tier, quick signup)
3. Total monthly cost: **$0** (you only pay for OpenAI usage)

---

## 🎯 Full Installation

### 1. Clone or Navigate to Project
```bash
cd ai-competitor-intel/backend
```

### 2. Install Dependencies
```bash
# Windows
python -m pip install -r requirements.txt

# Mac/Linux
pip install -r requirements.txt
```

### 3. Create `.env` File
```bash
# Copy example
copy .env.example .env

# Edit with your API keys
notepad .env
```

### 4. Add Your API Keys

**Minimum (Free Setup):**
```
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=...
```

**Better (With Tavily Free):**
```
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=...
TAVILY_API_KEY=tvly-...
```

### 5. Run the App
```bash
streamlit run competitor_agent_team.py
```

### 6. Open Browser
- Streamlit will open automatically at `http://localhost:8501`
- If not, manually open that URL

---

## 🔧 Troubleshooting

### "pip is not recognized"
Use `python -m pip` instead:
```bash
python -m pip install -r requirements.txt
```

### "Module not found: tavily"
If using Tavily option:
```bash
python -m pip install tavily-python
```

### "No competitor URLs found"
- Try adding a more detailed description
- Or try a different search engine option
- DuckDuckGo works best with clear business descriptions

---

## ✨ Usage Tips

### For Best Results:

1. **Provide Both URL and Description:**
   - URL: `https://competitor.com`
   - Description: `AI-powered analytics platform for SaaS companies`

2. **Use Clear Descriptions:**
   - ✅ Good: "Project management tool for remote teams"
   - ❌ Bad: "Software company"

3. **Start with DuckDuckGo:**
   - It's free and works well for most cases
   - Upgrade to Tavily if you need better results

---

## 🚀 Next Steps

Once you have the backend running:

1. Test with a competitor URL
2. Review the generated analysis
3. Try different search engines to compare results
4. Integrate with the Next.js frontend (see main README)

---

## 💰 Cost Breakdown

**Monthly Costs:**

| Service | Cost | Notes |
|---------|------|-------|
| OpenAI GPT-4o | ~$5-10 | Pay per use |
| Firecrawl | $0 | Free tier (500 pages/mo) |
| DuckDuckGo | $0 | Completely free |
| Tavily (optional) | $0 | Free tier (1000/mo) |
| **Total** | **$5-10/mo** | 🎉 |

---

## 📞 Need Help?

- Check `FREE_ALTERNATIVES.md` for more details
- See main `README.md` for full documentation
- Review `implementation_plan.md` for architecture details

**You're all set!** 🎉 Start analyzing competitors for free with DuckDuckGo!
