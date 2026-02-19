"use client"

import { useState, useEffect, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
    Sparkles,
    ArrowLeft,
    Loader2,
    Search,
    TrendingUp,
    Code,
    Target,
    Download,
    Share2,
    DollarSign,
    Box,
    Layers,
    Users,
    Zap,
    Scale,
    ShieldCheck,
    AlertTriangle,
    BarChart3
} from "lucide-react"
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell
} from 'recharts'

function DashboardContent() {
    const searchParams = useSearchParams()
    const [url, setUrl] = useState("")
    const [description, setDescription] = useState("")
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState<any>(null)
    const [searchEngine, setSearchEngine] = useState("🌟 Tavily AI (Free Tier - 1000/month)")
    const [credits, setCredits] = useState(10)

    useEffect(() => {
        const queryUrl = searchParams.get('url')
        if (queryUrl) {
            setUrl(queryUrl)
        }
    }, [searchParams])

    const handleAnalyze = async () => {
        if (!url && !description) {
            alert("Please provide either a URL or description")
            return
        }

        if (credits <= 0) {
            alert("Insufficient credits. Please top up your account.")
            return
        }

        setLoading(true)
        setResults(null)

        try {
            const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
            const response = await fetch(`${apiBase}/analyze`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url,
                    description,
                    search_engine: searchEngine
                }),
            })

            const result = await response.json()
            if (result.status === "success") {
                setResults(result.data)
                setCredits(prev => prev - 1)
            } else {
                alert(result.message || "Analysis failed")
            }
        } catch (error) {
            console.error("Analysis failed", error)
            alert("Connection error: Make sure the Python backend (main.py) is running on port 8000")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Navigation */}
            <nav className="fixed top-0 w-full glass z-50 border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <Link href="/" className="flex items-center gap-2">
                            <div className="w-10 h-10 rounded-xl gradient-blue-purple flex items-center justify-center shadow-lg shadow-blue-500/20">
                                <Sparkles className="w-6 h-6 text-white" />
                            </div>
                            <span className="text-2xl font-bold tracking-tight text-slate-900">
                                Compete<span className="text-blue-600">X</span>
                            </span>
                        </Link>
                        <div className="flex items-center gap-5">
                            <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-100 border border-slate-200 text-sm font-medium text-slate-700">
                                <Zap className="w-4 h-4 text-amber-500 fill-amber-500" />
                                <span>{credits} <span className="text-slate-400 font-normal">Credits</span></span>
                            </div>
                            <Button size="sm" className="rounded-full bg-slate-900 hover:bg-slate-800 px-6">Buy Credits</Button>
                        </div>
                    </div>
                </div>
            </nav>

            <div className="pt-24 pb-12 px-4">
                <div className="max-w-7xl mx-auto">
                    {/* Header */}
                    <div className="mb-8">
                        <Link href="/" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4">
                            <ArrowLeft className="w-4 h-4 mr-2" />
                            Back to Home
                        </Link>
                        <h1 className="text-3xl font-bold mb-2">Competitor Analysis</h1>
                        <p className="text-gray-600">Discover and analyze your competitors with AI-powered insights</p>
                    </div>

                    <div className="grid lg:grid-cols-3 gap-8">
                        {/* Input Panel */}
                        <div className="lg:col-span-1">
                            <Card className="sticky top-24">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <Search className="w-5 h-5" />
                                        Analysis Input
                                    </CardTitle>
                                    <CardDescription>
                                        Enter a competitor URL or describe your business
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div>
                                        <label className="text-sm font-medium mb-2 block">
                                            Competitor URL (optional)
                                        </label>
                                        <Input
                                            type="url"
                                            placeholder="https://competitor.com"
                                            value={url}
                                            onChange={(e) => setUrl(e.target.value)}
                                            disabled={loading}
                                        />
                                    </div>

                                    <div className="relative">
                                        <div className="absolute inset-0 flex items-center">
                                            <span className="w-full border-t" />
                                        </div>
                                        <div className="relative flex justify-center text-xs uppercase">
                                            <span className="bg-white px-2 text-gray-500">Or</span>
                                        </div>
                                    </div>

                                    <div>
                                        <label className="text-sm font-medium mb-2 block">
                                            Business Description
                                        </label>
                                        <Textarea
                                            placeholder="Describe your business or product..."
                                            value={description}
                                            onChange={(e) => setDescription(e.target.value)}
                                            disabled={loading}
                                            rows={4}
                                        />
                                    </div>

                                    <div>
                                        <label className="text-sm font-medium mb-2 block">
                                            Search Engine
                                        </label>
                                        <select
                                            value={searchEngine}
                                            onChange={(e) => setSearchEngine(e.target.value)}
                                            className="w-full h-11 rounded-lg border border-gray-200 bg-white px-4 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                            disabled={loading}
                                        >
                                            <option value="🌟 Tavily AI (Free Tier - 1000/month)">🌟 Tavily AI (Best Free Option)</option>
                                            <option value="🆓 DuckDuckGo (100% Free)">🆓 DuckDuckGo (Free)</option>
                                            <option value="Perplexity AI - Sonar Pro">Perplexity AI (Sonar Pro)</option>
                                            <option value="Exa AI">Exa AI (Semantic Search)</option>
                                        </select>
                                    </div>

                                    <Button
                                        onClick={handleAnalyze}
                                        disabled={loading || (!url && !description)}
                                        className="w-full"
                                        size="lg"
                                    >
                                        {loading ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Analyzing...
                                            </>
                                        ) : (
                                            <>
                                                <Sparkles className="w-4 h-4 mr-2" />
                                                Analyze Competitors
                                            </>
                                        )}
                                    </Button>

                                    {loading && (
                                        <div className="space-y-3 pt-4 border-t">
                                            <div className="flex items-center justify-between text-xs font-semibold text-blue-600 mb-1">
                                                <span>SPEED OPTIMIZED</span>
                                                <span>PARALLEL MODE ON</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm">
                                                <div className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
                                                <span className="text-gray-600">Discovering competitors (GPT-4o Mini)...</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm">
                                                <div className="w-2 h-2 rounded-full bg-blue-600 animate-pulse" />
                                                <span className="text-gray-600 font-medium">Extracting data in parallel (3x Faster)...</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm">
                                                <div className="w-2 h-2 rounded-full bg-gray-300" />
                                                <span className="text-gray-400">Synthesizing Market Intelligence...</span>
                                            </div>
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        </div>

                        {/* Results Panel */}
                        <div className="lg:col-span-2">
                            {!results && !loading && (
                                <Card className="border-2 border-dashed border-gray-300 bg-gray-50">
                                    <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                                        <div className="w-16 h-16 rounded-full bg-gray-200 flex items-center justify-center mb-4">
                                            <TrendingUp className="w-8 h-8 text-gray-400" />
                                        </div>
                                        <h3 className="text-lg font-semibold mb-2">No Analysis Yet</h3>
                                        <p className="text-gray-600 text-sm max-w-md">
                                            Enter a competitor URL or describe your business to get started with AI-powered competitive intelligence
                                        </p>
                                    </CardContent>
                                </Card>
                            )}

                            {results && (
                                <div className="space-y-8 animate-fade-in pb-20">
                                    {/* Market Landscape Visualizer */}
                                    <Card className="premium-card">
                                        <CardHeader>
                                            <div className="flex items-center justify-between">
                                                <div>
                                                    <CardTitle className="text-xl flex items-center gap-2">
                                                        <BarChart3 className="w-5 h-5 text-blue-600" />
                                                        Competitive Pricing Benchmarks
                                                    </CardTitle>
                                                    <CardDescription>
                                                        Comparison of entry-level pricing across discovered competitors
                                                    </CardDescription>
                                                </div>
                                            </div>
                                        </CardHeader>
                                        <CardContent>
                                            <div className="h-[300px] w-full mt-4">
                                                <ResponsiveContainer width="100%" height="100%">
                                                    <BarChart data={results.competitors.map((c: any) => ({
                                                        name: c.company_name.split(' ')[0],
                                                        cost: c.estimated_monthly_cost || 0,
                                                        fullName: c.company_name,
                                                        tier: c.market_tier
                                                    }))}>
                                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                                                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748B' }} dy={10} />
                                                        <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748B' }} tickFormatter={(v) => `$${v}`} />
                                                        <Tooltip
                                                            cursor={{ fill: '#F8FAFC' }}
                                                            content={({ active, payload }) => {
                                                                if (active && payload && payload.length) {
                                                                    return (
                                                                        <div className="glass p-3 rounded-xl border border-slate-200/50 shadow-xl">
                                                                            <p className="font-bold text-slate-800">{payload[0].payload.fullName}</p>
                                                                            <p className="text-blue-600 font-semibold">${payload[0].value} /mo</p>
                                                                            <p className="text-xs text-slate-500 mt-1">{payload[0].payload.tier}</p>
                                                                        </div>
                                                                    );
                                                                }
                                                                return null;
                                                            }}
                                                        />
                                                        <Bar dataKey="cost" radius={[6, 6, 0, 0]} barSize={45}>
                                                            {results.competitors.map((_: any, index: number) => (
                                                                <Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#4F46E5' : '#06B6D4'} fillOpacity={0.8} />
                                                            ))}
                                                        </Bar>
                                                    </BarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        </CardContent>
                                    </Card>

                                    {/* Executive Report */}
                                    <div className="grid md:grid-cols-3 gap-6">
                                        <Card className="md:col-span-2 premium-card">
                                            <CardHeader>
                                                <CardTitle className="flex items-center gap-2">
                                                    <Scale className="w-5 h-5 text-indigo-600" />
                                                    Strategic Intelligence Report
                                                </CardTitle>
                                            </CardHeader>
                                            <CardContent>
                                                <div className="prose prose-slate max-w-none text-sm leading-relaxed text-slate-600 whitespace-pre-wrap">
                                                    {results.report}
                                                </div>
                                            </CardContent>
                                        </Card>

                                        <div className="space-y-6">
                                            <Card className="premium-card bg-indigo-600 text-white border-none overflow-hidden relative">
                                                <div className="absolute top-0 right-0 p-4 opacity-10">
                                                    <Target className="w-24 h-24" />
                                                </div>
                                                <CardHeader>
                                                    <CardTitle className="text-lg">Market Sentiment</CardTitle>
                                                </CardHeader>
                                                <CardContent>
                                                    <div className="text-3xl font-bold mb-1">Strong</div>
                                                    <p className="text-indigo-100 text-xs text-balance">The competitive landscape shows high entry barriers but significant churn opportunity.</p>
                                                </CardContent>
                                            </Card>

                                            <Card className="premium-card">
                                                <CardHeader>
                                                    <CardTitle className="text-sm">Quick Action Items</CardTitle>
                                                </CardHeader>
                                                <CardContent className="space-y-3">
                                                    <div className="flex items-center gap-2 text-xs p-2 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-100">
                                                        <ShieldCheck className="w-4 h-4" />
                                                        Undercut "Leader" pricing
                                                    </div>
                                                    <div className="flex items-center gap-2 text-xs p-2 rounded-lg bg-blue-50 text-blue-700 border border-blue-100">
                                                        <Zap className="w-4 h-4" />
                                                        Focus on Tech integrations
                                                    </div>
                                                </CardContent>
                                            </Card>
                                        </div>
                                    </div>

                                    {/* Detailed Competitor SWOTS */}
                                    <div className="space-y-6">
                                        <h3 className="text-2xl font-bold text-slate-800 px-1">Tactical Analysis</h3>
                                        <div className="grid md:grid-cols-2 gap-6">
                                            {results.competitors.map((comp: any, idx: number) => (
                                                <Card key={idx} className="premium-card group hover:-translate-y-1">
                                                    <CardHeader className="pb-4">
                                                        <div className="flex justify-between items-start">
                                                            <div>
                                                                <div className="flex items-center gap-2 mb-1">
                                                                    <div className={`w-2 h-2 rounded-full ${comp.market_tier === 'Leader' ? 'bg-amber-500' : 'bg-blue-500'}`} />
                                                                    <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">{comp.market_tier}</span>
                                                                </div>
                                                                <CardTitle className="text-xl group-hover:text-blue-600 transition-colors">{comp.company_name}</CardTitle>
                                                                <CardDescription className="line-clamp-1">{comp.competitor_url}</CardDescription>
                                                            </div>
                                                            <div className="p-2 rounded-xl bg-slate-50 border border-slate-100 font-bold text-slate-700 px-3">
                                                                ${comp.estimated_monthly_cost || '??'}
                                                                <span className="text-[10px] text-slate-400 font-normal ml-1">/mo</span>
                                                            </div>
                                                        </div>
                                                    </CardHeader>
                                                    <CardContent className="space-y-6">
                                                        <div className="grid grid-cols-2 gap-4">
                                                            <div className="p-3 rounded-2xl bg-slate-50/50 border border-slate-100">
                                                                <div className="flex items-center gap-2 mb-2">
                                                                    <ShieldCheck className="w-4 h-4 text-emerald-500" />
                                                                    <span className="text-xs font-bold uppercase text-slate-500">Strengths</span>
                                                                </div>
                                                                <ul className="space-y-1.5">
                                                                    {comp.swot_strengths?.map((s: string, i: number) => (
                                                                        <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5 line-clamp-1">
                                                                            <span className="mt-1 w-1 h-1 rounded-full bg-emerald-300 shrink-0" />
                                                                            {s}
                                                                        </li>
                                                                    ))}
                                                                </ul>
                                                            </div>
                                                            <div className="p-3 rounded-2xl bg-slate-50/50 border border-slate-100">
                                                                <div className="flex items-center gap-2 mb-2">
                                                                    <AlertTriangle className="w-4 h-4 text-rose-400" />
                                                                    <span className="text-xs font-bold uppercase text-slate-500">Weaknesses</span>
                                                                </div>
                                                                <ul className="space-y-1.5">
                                                                    {comp.swot_weaknesses?.map((w: string, i: number) => (
                                                                        <li key={i} className="text-xs text-slate-600 flex items-start gap-1.5 line-clamp-1">
                                                                            <span className="mt-1 w-1 h-1 rounded-full bg-rose-300 shrink-0" />
                                                                            {w}
                                                                        </li>
                                                                    ))}
                                                                </ul>
                                                            </div>
                                                        </div>

                                                        <div className="space-y-2">
                                                            <div className="flex items-center gap-2">
                                                                <Code className="w-4 h-4 text-blue-500" />
                                                                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Technology Focus</span>
                                                            </div>
                                                            <div className="flex flex-wrap gap-1.5">
                                                                {comp.tech_stack?.map((t: string, i: number) => (
                                                                    <span key={i} className="px-2 py-0.5 bg-slate-100/80 rounded-md text-[10px] font-semibold text-slate-500 border border-slate-200/50">
                                                                        {t}
                                                                    </span>
                                                                ))}
                                                            </div>
                                                        </div>

                                                        <div className="pt-4 border-t border-slate-100">
                                                            <div className="flex items-center justify-between text-[11px] text-slate-400 italic">
                                                                <span>GTM Strategy: {comp.marketing_focus}</span>
                                                                <span className="flex items-center gap-1">
                                                                    <Users className="w-3 h-3" />
                                                                    Trust: {comp.social_proof}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </CardContent>
                                                </Card>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default function DashboardPage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
                    <p className="text-gray-600 font-medium">Loading Dashboard...</p>
                </div>
            </div>
        }>
            <DashboardContent />
        </Suspense>
    )
}
