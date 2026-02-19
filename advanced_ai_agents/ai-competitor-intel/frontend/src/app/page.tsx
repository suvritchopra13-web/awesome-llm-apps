import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  Bot,
  CheckCircle2,
  Cpu,
  Zap,
  Globe,
  Search,
  ShieldCheck
} from "lucide-react";

import { Button } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Navigation */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold tracking-tight">CompeteX</span>
          </div>
          <nav className="hidden gap-6 md:flex">
            <Link href="#features" className="text-sm font-medium hover:text-primary">Features</Link>
            <Link href="#how-it-works" className="text-sm font-medium hover:text-primary">How it Works</Link>
            <Link href="#pricing" className="text-sm font-medium hover:text-primary">Pricing</Link>
          </nav>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" asChild>
              <Link href="/app/new">Login</Link>
            </Button>
            <Button size="sm" asChild>
              <Link href="/app/new">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden py-24 lg:py-32">
          <div className="container relative z-10 flex flex-col items-center text-center">
            <div className="animate-fade-in mb-6 inline-flex items-center rounded-full border bg-primary/5 px-3 py-1 text-sm font-medium text-primary shadow-sm">
              <Bot className="mr-2 h-4 w-4" />
              <span>Next-Gen Competitor Discovery is Here</span>
            </div>
            <h1 className="animate-slide-up bg-gradient-to-br from-foreground to-foreground/70 bg-clip-text text-5xl font-extrabold tracking-tight text-transparent sm:text-6xl md:text-7xl lg:text-8xl">
              Outsmart your <br />
              <span className="text-primary italic">Competitors</span> with AI.
            </h1>
            <p className="animate-slide-up mt-8 max-w-2xl text-lg text-muted-foreground md:text-xl">
              Instantly identify competitors, analyze their strategies, and uncover market gaps using our advanced Neural Search engine and AI Agents.
            </p>
            <div className="animate-slide-up mt-10 flex flex-col gap-4 sm:flex-row">
              <Button size="lg" className="h-12 px-8 text-lg" asChild>
                <Link href="/app/new">
                  Launch Free Analysis <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="h-12 px-8 text-lg">
                View Live Demo
              </Button>
            </div>

            {/* Social Proof */}
            <div className="mt-16 flex flex-col items-center gap-8 opacity-60">
              <p className="text-sm font-semibold uppercase tracking-widest text-muted-foreground">Trusted by top growth teams</p>
              <div className="flex flex-wrap justify-center gap-8 md:gap-16">
                <div className="text-2xl font-bold">MARMETO</div>
                <div className="text-2xl font-bold">NOGIN</div>
                <div className="text-2xl font-bold">VAIMO</div>
                <div className="text-2xl font-bold">ECOMNOVA</div>
              </div>
            </div>
          </div>

          {/* Background Decorative Elements */}
          <div className="absolute left-1/2 top-1/2 -z-10 h-[600px] w-[800px] -translate-x-1/2 -translate-y-1/2 bg-primary/10 blur-[120px] rounded-full" />
        </section>

        {/* Value Propositions */}
        <section id="features" className="bg-muted/30 py-24">
          <div className="container">
            <div className="mb-16 text-center">
              <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Everything you need to lead your market</h2>
              <p className="mt-4 text-lg text-muted-foreground">Built for high-growth startups and strategic researchers.</p>
            </div>
            <div className="grid gap-8 md:grid-cols-3">
              {[
                {
                  title: "Neural Search Discovery",
                  description: "Leverage Exa's brain-like search to find direct competitors that normal search engines miss.",
                  icon: Search
                },
                {
                  title: "AI Agent Analysis",
                  description: "Our agents crawl official websites in real-time to extract features, offerings, and positioning.",
                  icon: Cpu
                },
                {
                  title: "Data Visualization",
                  description: "Turn raw intelligence into beautiful, actionable reports that keep your team aligned.",
                  icon: BarChart3
                }
              ].map((feature, i) => (
                <div key={i} className="premium-card flex flex-col p-8">
                  <div className="mb-6 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <h3 className="mb-3 text-xl font-bold">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How it Works */}
        <section id="how-it-works" className="py-24">
          <div className="container grid gap-12 lg:grid-cols-2 lg:items-center">
            <div className="space-y-6">
              <div className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
                Step-by-Step
              </div>
              <h2 className="text-4xl font-bold tracking-tight">Zero to Intelligence in 60 seconds.</h2>
              <div className="space-y-4">
                {[
                  { step: "01", text: "Enter your company URL or business description." },
                  { step: "02", text: "Choose your search engine (Exa, Tavily, or DuckDuckGo)." },
                  { step: "03", text: "Let our AI Agents map out your competitive landscape." },
                  { step: "04", text: "Get a strategic report with homepages and core offerings." }
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-4">
                    <span className="text-2xl font-black text-primary/20">{item.step}</span>
                    <p className="text-lg font-medium">{item.text}</p>
                  </div>
                ))}
              </div>
              <Button size="lg" className="mt-4 shadow-lg shadow-primary/20" asChild>
                <Link href="/app/new">Identify Competitors Now</Link>
              </Button>
            </div>
            <div className="relative rounded-3xl border-4 border-muted p-8 shadow-2xl bg-white lg:aspect-square">
              {/* Mock UI Element */}
              <div className="h-full w-full rounded-2xl bg-slate-50 p-6 flex flex-col gap-6">
                <div className="h-10 w-48 rounded bg-slate-200 animate-pulse" />
                <div className="grid grid-cols-3 gap-4">
                  <div className="h-32 rounded-xl bg-slate-200 animate-pulse" />
                  <div className="h-32 rounded-xl bg-slate-200 animate-pulse" />
                  <div className="h-32 rounded-xl bg-white border border-primary/30 p-4 shadow-sm">
                    <div className="h-4 w-4 rounded-full bg-primary mb-2" />
                    <div className="h-2 w-full rounded bg-slate-200 mb-2" />
                    <div className="h-2 w-2/3 rounded bg-slate-200" />
                  </div>
                </div>
                <div className="flex-1 rounded-xl bg-white border-2 border-dashed flex flex-col p-6 items-center justify-center text-center">
                  <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mb-2">
                    <Zap className="h-6 w-6 text-primary" />
                  </div>
                  <p className="text-sm font-bold">Analysis in Progress...</p>
                  <p className="text-xs text-muted-foreground mt-1">Extracting features from 3 websites</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t py-12">
        <div className="container flex flex-col items-center justify-between gap-6 md:flex-row">
          <div className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-primary" />
            <span className="font-bold">CompeteX</span>
          </div>
          <p className="text-sm text-muted-foreground">© 2026 CompeteX AI. Part of the Marmeto Labs collective.</p>
          <div className="flex gap-4">
            <Link href="#" className="text-muted-foreground hover:text-primary"><Globe className="h-5 w-5" /></Link>
            <Link href="#" className="text-muted-foreground hover:text-primary"><ShieldCheck className="h-5 w-5" /></Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
