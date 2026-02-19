# Step-by-Step Tavily Setup Guide

## 1️⃣ Get Your Free Tavily API Key

### Visit Tavily Website
1. Open your browser and go to: **https://tavily.com**
2. Click "Get Started" or "Sign Up"
3. Create a free account (using Google/GitHub or email)
4. Once logged in, navigate to your **Dashboard**
5. Copy your **API Key** (starts with `tvly-`)

**Free Tier Benefits:**
- ✅ 1,000 searches per month
- ✅ No credit card required
- ✅ Full API access

---

## 2️⃣ Install Tavily Python Package

Open your terminal in the backend folder:

```bash
cd C:\Users\suvri\Downloads\ai-competitor-intel\backend
python -m pip install tavily-python
```

---

## 3️⃣ Configure Your Environment

### Create `.env` file (if you haven't already):

```bash
copy .env.example .env
notepad .env
```

### Add Your API Keys to `.env`:

```bash
# Required APIs
OPENAI_API_KEY=sk-your-actual-openai-key-here
FIRECRAWL_API_KEY=your-actual-firecrawl-key-here

# Tavily AI (Free tier)
TAVILY_API_KEY=tvly-your-actual-tavily-key-here
```

**Replace the placeholder values with your actual API keys!**

---

## 4️⃣ Run the Application

```bash
streamlit run competitor_agent_team.py
```

---

## 5️⃣ Use Tavily in the App

1. **Browser should open automatically** to `http://localhost:8501`
2. **In the sidebar:**
   - Select **"🌟 Tavily AI (Free Tier - 1000/month)"** from dropdown
   - Enter your API keys (OpenAI, Firecrawl, Tavily)
3. **In the main area:**
   - Enter a competitor URL OR business description
   - Click **"Analyze Competitors"**
4. **Wait for results** (usually 2-3 minutes)

---

## 6️⃣ Test Example

**Try this:**
- **URL**: `https://asana.com`
- **Description**: `Project management and team collaboration tool`
- **Search Engine**: 🌟 Tavily AI

**Expected Results:**
- Find 3 competitors (e.g., Monday.com, Trello, ClickUp)
- Extract pricing, features, tech stack
- Generate competitive insights

---

## ✅ Verification Checklist

- [ ] Tavily account created at tavily.com
- [ ] API key copied (starts with `tvly-`)
- [ ] `tavily-python` package installed
- [ ] `.env` file created with all 3 API keys
- [ ] Streamlit app running on localhost:8501
- [ ] Tavily selected in dropdown
- [ ] Successfully analyzed at least one competitor

---

## 🔧 Troubleshooting

### "Module 'tavily' not found"
```bash
python -m pip install tavily-python --upgrade
```

### "Invalid API key"
- Check your Tavily dashboard for the correct key
- Make sure there are no extra spaces in `.env`
- Restart Streamlit after updating `.env`

### "Rate limit exceeded"
- You've used 1,000 free searches
- Wait until next month or upgrade to paid plan
- Switch to DuckDuckGo temporarily

### "No competitors found"
- Try adding a more detailed description
- Check if the URL is accessible
- Verify API keys are correct

---

## 💡 Tips for Best Results

1. **Provide both URL and description** for better accuracy
2. **Use specific descriptions**: "AI-powered project management for remote teams" vs "software company"
3. **Start with well-known companies** to test: Asana, Notion, Airtable
4. **Monitor your usage** at tavily.com dashboard

---

## 📊 What to Expect

**Analysis Time:** 2-5 minutes per analysis
**Competitors Found:** 3 companies per search
**Data Extracted:**
- Company name
- Pricing models
- Key features
- Tech stack
- Marketing focus
- Customer feedback

**AI Insights:**
- Market gaps
- Competitive advantages
- Pricing strategies
- Growth opportunities

---

## 🎯 Next Steps After Setup

1. ✅ Test with 1-2 competitor analyses
2. ✅ Review the generated reports
3. ✅ Connect frontend (Next.js app on port 3000)
4. ✅ Add payment gateway (Stripe)
5. ✅ Deploy to production

---

## 📞 Get Help

If you encounter issues:
1. Check `FREE_ALTERNATIVES.md` for alternative options
2. Review error messages in Streamlit
3. Verify all API keys are valid
4. Try DuckDuckGo option if Tavily fails

**You're ready to analyze competitors with Tavily AI! 🚀**
