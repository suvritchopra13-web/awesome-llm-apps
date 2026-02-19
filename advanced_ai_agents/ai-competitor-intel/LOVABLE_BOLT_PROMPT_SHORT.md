# CompeteX - Quick Prompt for Lovable/Bolt

Build "CompeteX" - an AI competitor intelligence platform with Next.js 14, TypeScript, and TailwindCSS.

## Design
- Modern, minimalistic, gradient-heavy (blue-purple)
- Glassmorphism effects, smooth animations
- Font: Inter, Colors: Blue (#3b82f6) to Purple (#8b5cf6)

## Pages

### Landing Page (/)
1. **Hero**: Gradient mesh bg, headline "Analyze Your Competitors / In Minutes, Not Days", stats row (98% accuracy, <5min, 50+ data points, 24/7)
2. **How It Works**: 4 agent cards (Research, Data Extraction, Market Analyst, Coordinator) with gradient icons
3. **Benefits**: 2-col layout, checklist + mockup card
4. **Pricing**: 3 tiers (Starter $29/10 credits, Professional $99/50 credits - highlighted, Enterprise $299/200 credits)
5. **CTA**: Gradient bg, "Ready to Outpace Your Competition?"
6. **Footer**: Dark, centered

### Dashboard (/dashboard)
**Left panel (sticky, 1/3)**: Analysis form
- URL input (optional)
- OR business description textarea
- Search engine dropdown (Perplexity/Exa)
- "Analyze Competitors" button (gradient)
- Loading: 3-step progress indicator

**Right panel (2/3)**: Results
- Empty state: dashed card with TrendingUp icon
- Results: 
  - Key Insights card (numbered blue boxes)
  - Competitor cards (name, pricing, 3-col grid: pricing/features/tech stack)

## Mock Data
```typescript
const results = {
  competitors: [
    { name: "Competitor A", pricing: "$29-99/mo", 
      features: ["AI Analysis", "Real-time Data", "API Access"],
      tech: ["React", "Python", "PostgreSQL"],
      marketingFocus: "SMB-focused" },
    { name: "Competitor B", pricing: "$49-299/mo", 
      features: ["Advanced Analytics", "Custom Reports"],
      tech: ["Next.js", "FastAPI", "MongoDB"],
      marketingFocus: "Enterprise-grade" }
  ],
  insights: [
    "67% use credit-based pricing",
    "Average entry price is $39/month",
    "Most focus on SaaS companies",
    "API access is premium (83% paywall)"
  ]
}
```

## Components
- Button (gradient default, outline, ghost variants)
- Input, Textarea (blue focus ring)
- Card (shadow, hover lift)
- Badge (gray pills for tech)

## Animations
- Fade-in on scroll
- Slide-up hero elements
- Hover: scale on buttons, shadow lift on cards
- Loading: spinner + pulsing dots

## Icons (Lucide)
Sparkles, Users, FileText, LineChart, Shield, TrendingUp, Check, ArrowRight, DollarSign, Code, Target, Search, Share2, Download

## Key Features
✨ Premium, polished aesthetic
✨ Fully responsive
✨ Smooth transitions (200-300ms)
✨ Clear visual hierarchy
✨ Interactive hover states everywhere

Use this for a stunning, production-ready SaaS UI!
