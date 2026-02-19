# AI Competitor Intelligence Platform - Lovable/Bolt Prompt

## Project Overview

Build a modern, minimalistic AI competitor intelligence platform called "CompeteX" that allows users to analyze competitors using AI agents. The platform should have a stunning landing page and an interactive analysis dashboard with a premium, polished feel.

---

## Tech Stack

**Frontend:**
- Next.js 14+ (App Router, TypeScript)
- TailwindCSS for styling
- Lucide React for icons
- shadcn/ui components (or similar) for base UI
- Google Fonts: Inter

**Design Style:**
- Modern, minimalistic aesthetic
- Gradient-heavy (blue-to-purple, purple-to-pink)
- Glassmorphism effects
- Smooth animations (fade-in, slide-up, scale on hover)
- Clean, spacious layouts
- Interactive hover states on all clickable elements

---

## Color Palette

**Primary:**
- Blue: `#3b82f6`
- Purple: `#8b5cf6`
- Gradient: `from-blue-600 to-purple-600`

**Accent:**
- Deep Purple: `#667eea`
- Pink: `#764ba2`

**Neutral:**
- Gray 50: `#f9fafb` (backgrounds)
- Gray 100: `#f3f4f6`
- Gray 600: `#4b5563` (text)
- Gray 900: `#111827` (headings)

**Success:** Green `#10b981`

---

## Pages to Build

### 1. Landing Page (`/`)

#### Navigation Bar (Fixed, Glassmorphic)
- Logo: Purple-blue gradient circle with sparkle icon + "CompeteX" text
- Right side: "Dashboard" link (ghost button) + "Get Started" button (gradient)
- Smooth scroll on navigation

#### Hero Section
**Background:** Gradient mesh (multiple radial gradients creating abstract pattern)

**Content:**
- Small badge: "AI-Powered Competitor Intelligence" with lightning icon
- Headline (extra large, bold):
  ```
  Analyze Your Competitors
  In Minutes, Not Days
  ```
  (Second line in gradient text)
- Subheadline: "Our AI agents work together to discover, analyze, and deliver comprehensive competitor insights automatically"
- Two CTA buttons:
  - Primary: "Start Free Analysis" (gradient with shadow)
  - Secondary: "Watch Demo" (outline)
- Stats row (4 columns):
  - "98%" - Accuracy
  - "<5min" - Analysis Time
  - "50+" - Data Points
  - "24/7" - Auto-Monitor

#### How It Works Section
**Title:** "How It Works"
**Subtitle:** "Four specialized AI agents work together to deliver comprehensive insights"

**Grid of 4 cards** (responsive: 2 cols mobile, 4 cols desktop):

1. **Research Agent**
   - Icon: Users (blue-to-cyan gradient background)
   - Description: "Discovers relevant competitors using neural search"

2. **Data Extraction**
   - Icon: FileText (purple-to-pink gradient)
   - Description: "Deep-crawls websites for pricing, features, and tech stack"

3. **Market Analyst**
   - Icon: LineChart (orange-to-red gradient)
   - Description: "Identifies gaps, opportunities, and positioning"

4. **Team Coordinator**
   - Icon: Shield (green-to-emerald gradient)
   - Description: "Orchestrates agents and delivers structured reports"

**Card style:**
- White background
- Border with hover shadow lift effect
- Icon in gradient circle (12x12, rounded-lg)
- Title: semi-bold
- Description: gray text

#### Benefits Section
**Two-column layout** (image on right, content on left on desktop)

**Left Column:**
- Title: "Everything You Need to Stay Ahead"
- Checklist with green checkmarks:
  - Comprehensive competitor analysis in minutes
  - Real-time data extraction from live websites
  - Strategic insights and recommendations
  - Beautiful, exportable reports (PDF, CSV)
  - Track changes with automated monitoring
  - Compliant and ethical data collection

**Right Column:**
- Glassmorphic card mockup showing:
  - Gradient progress bar
  - Gray placeholder bars
  - 2x2 grid of stat cards showing "87% Market Share" and "$49 Avg. Pricing"

#### Pricing Section
**Title:** "Simple, Credit-Based Pricing"
**Subtitle:** "Pay only for what you use. No subscriptions."

**3 pricing cards** (grid layout):

**Starter ($29):**
- 10 credits
- Basic analysis
- Email support
- PDF exports

**Professional ($99) - HIGHLIGHTED:**
- Badge: "Most Popular" (gradient, positioned absolutely above card)
- 50 credits
- Advanced insights
- Priority support
- All export formats
- API access
- Elevated with scale and blue border

**Enterprise ($299):**
- 200 credits
- Custom analysis
- 24/7 support
- White-label reports
- Team collaboration

**Card style:**
- Clean, minimal
- Feature list with checkmarks
- "Get Started" button at bottom

#### CTA Section
**Background:** Purple-blue gradient
**Content (centered, white text):**
- Title: "Ready to Outpace Your Competition?"
- Subtitle: "Get your first competitor analysis report in under 5 minutes"
- Button: "Start Free Analysis" (white background, blue text)

#### Footer
**Background:** Dark gray (gray-900)
**Content (centered):**
- Logo + "CompeteX" branding
- Description: "AI-powered competitor intelligence for modern businesses"
- Links: Privacy | Terms | Contact
- Copyright: "© 2026 CompeteX. All rights reserved."

---

### 2. Dashboard Page (`/dashboard`)

#### Navigation Bar (Same as landing page)
**Right side changes:**
- Credits display: "Credits: 10" (bold number)
- "Buy Credits" button (outline, small)

#### Page Header
- Back arrow link: "← Back to Home"
- Title: "Competitor Analysis"
- Subtitle: "Discover and analyze your competitors with AI-powered insights"

#### Two-Column Layout

##### Left Column (Sticky, 1/3 width)
**Card: "Analysis Input"**

**Form fields:**
1. **Competitor URL** (optional)
   - Label: "Competitor URL (optional)"
   - Input: `https://competitor.com`
   - Type: url

2. **Divider** with "Or" text in center

3. **Business Description**
   - Label: "Business Description"
   - Textarea: "Describe your business or product..."
   - Rows: 4

4. **Search Engine Selector**
   - Label: "Search Engine"
   - Dropdown:
     - Perplexity AI - Sonar Pro
     - Exa AI

5. **Analyze Button**
   - Full width, large
   - Text: "Analyze Competitors" with sparkle icon
   - Gradient style
   - Disabled when no input or loading

**Loading States:**
When analyzing, show progress checklist:
- ✓ Discovering competitors... (blue dot, pulsing)
- ○ Extracting data... (gray dot)
- ○ Analyzing insights... (gray dot)

##### Right Column (2/3 width)

**Empty State** (before analysis):
- Dashed border card
- Centered content:
  - Large icon (TrendingUp in gray circle)
  - Title: "No Analysis Yet"
  - Description: "Enter a competitor URL or describe your business to get started with AI-powered competitive intelligence"

**Results State** (after analysis):

**1. Key Insights Card**
- Header: "Key Insights" with Target icon
- Actions: "Share" and "Export" buttons (small, outline)
- Content: Numbered insight boxes (blue background, blue border):
  ```
  1. 67% of competitors use credit-based pricing models
  2. Average entry-level price point is $39/month
  3. Most competitors focus on SaaS companies
  4. API access is a premium feature (83% paywall)
  ```

**2. Competitors Found Section**
- Title: "Competitors Found (2)"
- List of competitor cards:

**Competitor Card Structure:**
- Header: Company name + Pricing (right aligned)
- Description: Marketing focus
- 3-column grid:
  1. **Pricing** (DollarSign icon, green)
     - Display pricing tiers
  2. **Key Features** (Sparkles icon, purple)
     - Bullet list of features
  3. **Tech Stack** (Code icon, blue)
     - Badge pills for each technology

**Card style:**
- White background
- Border with hover shadow
- Hover: lift effect

---

## Component Requirements

### UI Components to Create

1. **Button** (with variants)
   - `default`: Gradient with shadow
   - `outline`: Border with hover fill
   - `ghost`: Transparent with hover background
   - `secondary`: Gray background
   - Sizes: sm, default, lg

2. **Input**
   - Clean border
   - Blue ring on focus
   - Placeholder styling

3. **Textarea**
   - Same styling as Input
   - Min height: 120px

4. **Card**
   - Card, CardHeader, CardTitle, CardDescription, CardContent
   - Rounded corners
   - Subtle shadow
   - Hover shadow increase

5. **Badge**
   - Small pill-shaped elements
   - Gray background for tech stack

### Utilities

Create `lib/utils.ts` with:
```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Styling Details

### Global CSS (`globals.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .glass {
    @apply bg-white/80 backdrop-blur-lg border border-gray-200/50 shadow-xl;
  }
  
  .gradient-purple-blue {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .gradient-mesh {
    background: 
      radial-gradient(at 40% 20%, hsla(240, 80%, 70%, 0.3) 0px, transparent 50%),
      radial-gradient(at 80% 0%, hsla(280, 80%, 70%, 0.3) 0px, transparent 50%),
      radial-gradient(at 0% 50%, hsla(220, 80%, 70%, 0.3) 0px, transparent 50%),
      radial-gradient(at 80% 50%, hsla(260, 80%, 70%, 0.3) 0px, transparent 50%);
  }
  
  .animate-fade-in {
    animation: fadeIn 0.5s ease-in;
  }
  
  .animate-slide-up {
    animation: slideUp 0.5s ease-out;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Tailwind Config

Extend with:
- Font family: Inter
- Custom animations
- Custom colors matching the palette above

---

## Functionality Requirements

### Landing Page
- Smooth scroll navigation
- Animate elements on scroll (fade-in)
- All "Get Started" buttons link to `/dashboard`
- Responsive: mobile-first design

### Dashboard Page

**State Management:**
```typescript
const [url, setUrl] = useState("")
const [description, setDescription] = useState("")
const [loading, setLoading] = useState(false)
const [results, setResults] = useState(null)
const [searchEngine, setSearchEngine] = useState("perplexity")
```

**Analysis Function (Mock for now):**
```typescript
const handleAnalyze = async () => {
  if (!url && !description) {
    alert("Please provide either a URL or description")
    return
  }

  setLoading(true)
  
  // Simulate API call
  setTimeout(() => {
    setResults({
      competitors: [
        { 
          name: "Competitor A", 
          pricing: "$29-99/mo", 
          features: ["AI Analysis", "Real-time Data", "API Access"],
          tech: ["React", "Python", "PostgreSQL"],
          marketingFocus: "SMB-focused, self-service platform"
        },
        { 
          name: "Competitor B", 
          pricing: "$49-299/mo", 
          features: ["Advanced Analytics", "Custom Reports", "Team Collaboration"],
          tech: ["Next.js", "FastAPI", "MongoDB"],
          marketingFocus: "Enterprise-grade, white-label solutions"
        },
      ],
      insights: [
        "67% of competitors use credit-based pricing models",
        "Average entry-level price point is $39/month",
        "Most competitors focus on SaaS companies",
        "API access is a premium feature (83% paywall)",
      ]
    })
    setLoading(false)
  }, 3000)
}
```

**Validation:**
- Disable analyze button when no input provided
- Disable all inputs during loading
- Show loading spinner in button

**Loading States:**
- Progress indicator updates during analysis
- Smooth transition from empty to results state

---

## Design Principles

1. **Minimalism First**
   - Clean, spacious layouts
   - Plenty of whitespace
   - Simple, clear typography

2. **Interactive & Modern**
   - Hover effects on all clickable elements
   - Smooth transitions (200-300ms)
   - Scale transforms on buttons
   - Shadow lift on cards

3. **Visual Hierarchy**
   - Large, bold headings
   - Clear section separation
   - Gradient text for emphasis
   - Icon usage for quick recognition

4. **Responsive Design**
   - Mobile-first approach
   - Breakpoints: sm (640px), md (768px), lg (1024px)
   - Grid layouts that stack on mobile
   - Readable font sizes on all devices

5. **Accessibility**
   - Proper heading hierarchy
   - Alt text for icons
   - Keyboard navigation support
   - Focus states visible

---

## Icons to Use (Lucide React)

- Sparkles (logo, features)
- Zap (badge, speed)
- Shield (security, coordinator)
- TrendingUp (analytics, empty state)
- Users (research agent)
- ArrowRight (CTAs)
- Check (checklists, pricing)
- LineChart (analyst)
- FileText (extraction)
- Clock (timing)
- Download (export)
- Share2 (sharing)
- DollarSign (pricing)
- Code (tech stack)
- Target (insights)
- Loader2 (loading spinner)
- Search (search)
- ArrowLeft (back button)

---

## API Integration Points (For Future)

The dashboard should be ready to connect to a backend API:

**Endpoint:** `POST /api/analyze`

**Request:**
```json
{
  "url": "https://competitor.com",
  "description": "AI-powered analytics platform",
  "searchEngine": "perplexity"
}
```

**Response:**
```json
{
  "competitors": [
    {
      "name": "string",
      "pricing": "string",
      "features": ["string"],
      "tech": ["string"],
      "marketingFocus": "string"
    }
  ],
  "insights": ["string"]
}
```

---

## Final Touches

1. **Favicon:** Create a simple gradient icon
2. **Meta tags:** Add proper title and description
3. **Loading states:** Skeleton loaders or spinners
4. **Error handling:** Toast notifications for errors
5. **Mobile menu:** Hamburger menu for mobile navigation

---

## Success Criteria

The final application should:
✅ Look premium and modern (like a $99/mo SaaS product)
✅ Be fully responsive on all devices
✅ Have smooth, delightful animations
✅ Feel interactive with clear visual feedback
✅ Have a clean, minimalistic aesthetic
✅ Use gradients tastefully (not overwhelming)
✅ Work perfectly with mock data
✅ Be ready for API integration

---

## Deployment Notes

- Build command: `npm run build`
- Deploy to Vercel (auto-detected Next.js)
- Environment variables: None needed for frontend-only version

---

**IMPORTANT:** Focus on creating a visually stunning, modern UI that feels premium and polished. Every interaction should feel smooth and intentional. The design should inspire confidence that this is a professional, high-quality product worth paying for.
