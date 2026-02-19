"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
    ArrowLeft,
    Download,
    ExternalLink,
    FileText,
    Globe,
    Info,
    LayoutDashboard,
    Share2,
    TrendingUp
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";

export default function ReportViewPage() {
    const { runId } = useParams();
    const router = useRouter();
    const [report, setReport] = useState<any>(null);

    useEffect(() => {
        if (runId) {
            const reports = JSON.parse(localStorage.getItem("compete_x_reports") || "{}");
            const foundReport = reports[runId as string];
            if (foundReport) {
                setReport(foundReport);
            }
        }
    }, [runId]);

    if (!report) {
        return (
            <div className="container flex min-h-[60vh] flex-col items-center justify-center space-y-4 py-10">
                <div className="h-12 w-12 animate-pulse rounded-full bg-muted" />
                <h2 className="text-xl font-semibold">Loading your intelligence report...</h2>
                <p className="text-muted-foreground">This normally takes just a second.</p>
                <Button variant="outline" onClick={() => router.push("/app/new")}>
                    <ArrowLeft className="mr-2 h-4 w-4" /> Go back
                </Button>
            </div>
        );
    }

    return (
        <div className="container max-w-5xl space-y-8 py-10">
            {/* Header */}
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
                <div>
                    <div className="mb-2 flex items-center gap-2">
                        <Button variant="ghost" size="sm" className="-ml-2 h-8 px-2" onClick={() => router.push("/app/new")}>
                            <ArrowLeft className="mr-1 h-4 w-4" /> Back to Dashboard
                        </Button>
                        <Separator orientation="vertical" className="h-4" />
                        <span className="text-xs font-medium text-muted-foreground">
                            Generated on {new Date(report.timestamp).toLocaleDateString()}
                        </span>
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
                        {report.query.url ? new URL(report.query.url).hostname : "Market Analysis"}
                    </h1>
                    <p className="mt-2 text-lg text-muted-foreground">
                        Competitor Intelligence & Strategic Analysis Report
                    </p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                        <Share2 className="mr-2 h-4 w-4" /> Share
                    </Button>
                    <Button size="sm">
                        <Download className="mr-2 h-4 w-4" /> Export PDF
                    </Button>
                </div>
            </div>

            <Separator />

            {/* Main Content */}
            <Tabs defaultValue="competitors" className="space-y-6">
                <TabsList className="grid w-full grid-cols-2 lg:w-[400px]">
                    <TabsTrigger value="competitors">
                        <TrendingUp className="mr-2 h-4 w-4" /> Competitors
                    </TabsTrigger>
                    <TabsTrigger value="report">
                        <FileText className="mr-2 h-4 w-4" /> Full Analysis
                    </TabsTrigger>
                </TabsList>

                <TabsContent value="competitors" className="space-y-6">
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                        {report.competitors.map((comp: any, index: number) => (
                            <Card key={index} className="flex flex-col border-2 transition-colors hover:border-primary/50">
                                <CardHeader className="pb-4">
                                    <div className="mb-2 flex items-center justify-between">
                                        <Badge variant="outline">#{index + 1} Direct Competitor</Badge>
                                        <a
                                            href={comp.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-muted-foreground hover:text-primary"
                                        >
                                            <ExternalLink className="h-4 w-4" />
                                        </a>
                                    </div>
                                    <CardTitle className="line-clamp-1">{comp.name || new URL(comp.url).hostname}</CardTitle>
                                    <CardDescription className="flex items-center gap-1">
                                        <Globe className="h-3 w-3" />
                                        {new URL(comp.url).hostname}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="flex-1 space-y-4">
                                    <div className="space-y-2">
                                        <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-muted-foreground">
                                            <LayoutDashboard className="mr-1 h-3 w-3" /> Core Offering
                                        </h4>
                                        <p className="text-sm leading-relaxed text-foreground/90">
                                            {comp.offering || "Software solutions and strategic services tailored for enterprise clients."}
                                        </p>
                                    </div>
                                    <div className="space-y-2">
                                        <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-muted-foreground">
                                            <Info className="mr-1 h-3 w-3" /> Key Features
                                        </h4>
                                        <div className="flex flex-wrap gap-1">
                                            {(comp.features || ["Cloud Platform", "Analytics", "Automation"]).map((f: string) => (
                                                <Badge key={f} variant="secondary" className="bg-primary/5 text-[10px] font-semibold text-primary/80">
                                                    {f}
                                                </Badge>
                                            ))}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                <TabsContent value="report" className="space-y-6">
                    <Card className="border-2 shadow-sm">
                        <CardHeader className="bg-muted/30 pb-4">
                            <CardTitle className="text-xl">Strategic Analysis Deep-Dive</CardTitle>
                            <CardDescription>
                                Comprehensive breakdown of market positioning, strengths, and weaknesses.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="prose prose-sm dark:prose-invert max-w-none py-8">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {report.analysis_report}
                            </ReactMarkdown>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
