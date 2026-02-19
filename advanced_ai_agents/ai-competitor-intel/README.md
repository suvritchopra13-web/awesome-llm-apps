# CompeteX - AI Competitor Intelligence Platform

A modern, AI-powered competitor analysis platform that uses multi-agent systems to discover, analyze, and deliver comprehensive competitor insights automatically.

![CompeteX Dashboard](https://img.shields.io/badge/Status-Beta-blue)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![Python](https://img.shields.io/badge/Python-3.10+-blue)

## ✨ Features

- 🤖 **Multi-Agent System**: 4 specialized AI agents working together
- 🔍 **Competitor Discovery**: Automatic competitor finding using Perplexity/Exa
- 📊 **Deep Analysis**: Pricing, features, tech stack, and marketing insights
- 💎 **Modern UI**: Beautiful, minimalistic design with smooth animations
- 📈 **Real-time Reports**: Comprehensive analysis in under 5 minutes
- 💰 **Credit-Based Pricing**: Pay only for what you use

## 🏗️ Architecture

```
CompeteX/
├── frontend/          # Next.js 16 + TailwindCSS
│   ├── app/          # App router pages
│   ├── components/   # Reusable UI components
│   └── lib/          # Utility functions
└── backend/          # Python + Agno (Phidata)
    ├── competitor_agent_team.py   # Main agent logic
    └── requirements.txt           # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- API Keys:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Firecrawl](https://www.firecrawl.dev/app/api-keys)
  - [Perplexity](https://www.perplexity.ai/settings/api) OR [Exa](https://dashboard.exa.ai/api-keys)

### Installation

#### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-competitor-intel
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

#### 3. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file (optional for local dev)
cp .env.example .env.local
```

#### 4. Run the Application

**Terminal 1 - Backend (Streamlit):**
```bash
cd backend
streamlit run competitor_agent_team.py
```

**Terminal 2 - Frontend (Next.js):**
```bash
cd frontend
npm run dev
```

Visit:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend (Streamlit): [http://localhost:8501](http://localhost:8501)

> **Note**: Currently, the frontend has a mock API. For production, you'll need to create API endpoints to connect the Next.js frontend with the Python backend.

## 📁 Project Structure

```
ai-competitor-intel/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                 # Landing page
│   │   ├── dashboard/
│   │   │   └── page.tsx            # Analysis dashboard
│   │   ├── layout.tsx              # Root layout
│   │   └── globals.css             # Global styles
│   ├── components/
│   │   └── ui/                     # Reusable components
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       ├── textarea.tsx
│   │       └── card.tsx
│   └── lib/
│       └── utils.ts                # Utility functions
├── backend/
│   ├── competitor_agent_team.py    # Main agent logic
│   └── requirements.txt            # Python dependencies
└── README.md
```

## 🎨 UI Features

### Landing Page
- Gradient hero section with animated elements
- Feature showcase with icon cards
- Pricing tiers
- Glassmorphism effects
- Fully responsive

### Dashboard
- Clean, minimalistic design
- URL or description-based analysis
- Real-time loading states with progress indicators
- Interactive competitor cards
- Export and share functionality

## 🔑 Environment Variables

### Backend (.env)

```bash
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=...
PERPLEXITY_API_KEY=...   # OR use EXA_API_KEY
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Styling**: TailwindCSS
- **UI Components**: Custom components with Radix UI primitives
- **Icons**: Lucide React
- **Fonts**: Inter (Google Fonts)

### Backend
- **Framework**: Streamlit (prototype), will migrate to FastAPI
- **AI Agents**: Agno (formerly Phidata)
- **LLM**: OpenAI GPT-4o
- **Web Scraping**: Firecrawl
- **Search**: Perplexity Sonar Pro or Exa AI

## 🚢 Deployment (Budget-Friendly)

### Frontend
- **Platform**: Vercel (Free tier)
- **Cost**: $0/month

### Backend
- **Platform**: Railway (Free tier or $5/mo)
- **Cost**: $0-5/month

### Database (Future)
- **Platform**: Supabase (Free tier)
- **Cost**: $0/month

### Total Monthly Cost: ~$5-10

## 📊 Pricing Strategy

| Plan | Credits | Price | Per Report |
|------|---------|-------|-----------|
| Starter | 10 | $29 | $2.90 |
| Professional | 50 | $99 | $1.98 |
| Enterprise | 200 | $299 | $1.49 |

**Cost per report**: ~$0.65-2.20 (API costs)
**Gross Margin**: 60-80%

## 🗺️ Roadmap

### ✅ Phase 1 - MVP (Completed)
- [x] Core agent system
- [x] Modern landing page
- [x] Interactive dashboard
- [x] Mock data integration

### 🔄 Phase 2 - Backend Integration (In Progress)
- [ ] FastAPI backend
- [ ] Database setup (PostgreSQL)
- [ ] User authentication
- [ ] Real API integration

### 📅 Phase 3 - Payment & Features
- [ ] Stripe payment integration
- [ ] Credit management system
- [ ] Report history
- [ ] PDF exports

### 🚀 Phase 4 - Launch
- [ ] Production deployment
- [ ] Domain setup
- [ ] Analytics integration
- [ ] Marketing site

## 🤝 Contributing

Contributions are wel come! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 🙏 Acknowledgments

- Based on the tutorial from [The Unwind AI](https://www.theunwindai.com/)
- Agent framework: [Agno (Phidata)](https://docs.agno.com/)
- Original repo: [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ using Next.js and Agno
