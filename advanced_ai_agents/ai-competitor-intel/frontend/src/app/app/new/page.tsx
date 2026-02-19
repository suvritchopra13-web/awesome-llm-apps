"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { Loader2, Search, Target, Mail } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { register, analyze, AnalyzeRequest } from "@/lib/api";

export default function NewReportPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [url, setUrl] = useState("");
    const [description, setDescription] = useState("");
    const [engine, setEngine] = useState<"tavily" | "exa" | "duckduckgo">("exa");
    const [maxCompetitors, setMaxCompetitors] = useState("3");

    const analyzeMutation = useMutation({
        mutationFn: async () => {
            // 1. Get or create API key
            let apiKey = localStorage.getItem("compete_x_api_key");

            if (!apiKey) {
                if (!email) throw new Error("Email is required for first-time setup");
                const reg = await register(email);
                apiKey = reg.api_key;
                localStorage.setItem("compete_x_api_key", apiKey);
                localStorage.setItem("compete_x_email", email);
            }

            // 2. Run analysis
            const payload: AnalyzeRequest = {
                company_url: url || null,
                description: description || null,
                search_engine: engine,
                max_competitors: parseInt(maxCompetitors),
            };

            return await analyze(apiKey, payload);
        },
        onSuccess: (data) => {
            toast.success("Analysis complete!");
            // For now, save to local storage to simulate a database for the report view
            const reportId = crypto.randomUUID();
            const reports = JSON.parse(localStorage.getItem("compete_x_reports") || "{}");
            reports[reportId] = {
                ...data,
                timestamp: new Date().toISOString(),
                query: { url, description, engine }
            };
            localStorage.setItem("compete_x_reports", JSON.stringify(reports));

            router.push(`/app/reports/${reportId}`);
        },
        onError: (error: any) => {
            toast.error(error.message || "Failed to generate report");
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!url && !description) {
            toast.error("Please provide either a company URL or a description");
            return;
        }
        analyzeMutation.mutate();
    };

    const isFirstTime = typeof window !== "undefined" && !localStorage.getItem("compete_x_api_key");

    return (
        <div className="container max-w-2xl py-10">
            <Card className="border-2">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-2xl font-bold">
                        <Target className="h-6 w-6 text-primary" />
                        Generate New Analysis
                    </CardTitle>
                    <CardDescription>
                        Deep-dive into your competitors using AI-powered neural search.
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-6">
                        {isFirstTime && (
                            <div className="space-y-2">
                                <Label htmlFor="email" className="flex items-center gap-2">
                                    <Mail className="h-4 w-4" />
                                    Work Email
                                </Label>
                                <Input
                                    id="email"
                                    type="email"
                                    placeholder="suvrit@marmeto.com"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required={isFirstTime}
                                />
                                <p className="text-xs text-muted-foreground">
                                    We'll use this to create your account and manage your 3 free reports.
                                </p>
                            </div>
                        )}

                        <div className="space-y-2">
                            <Label htmlFor="url">Company Website (Optional)</Label>
                            <Input
                                id="url"
                                placeholder="https://example.com"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="description">Business Description</Label>
                            <Textarea
                                id="description"
                                placeholder="Describe the company and its primary products/services..."
                                className="min-h-[100px]"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="engine">Search Engine</Label>
                                <Select value={engine} onValueChange={(v: any) => setEngine(v)}>
                                    <SelectTrigger id="engine">
                                        <SelectValue placeholder="Select engine" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="exa">Exa (Neural)</SelectItem>
                                        <SelectItem value="tavily">Tavily (AI)</SelectItem>
                                        <SelectItem value="duckduckgo">DuckDuckGo (Privacy)</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="count">Max Competitors</Label>
                                <Input
                                    id="count"
                                    type="number"
                                    min="1"
                                    max="5"
                                    value={maxCompetitors}
                                    onChange={(e) => setMaxCompetitors(e.target.value)}
                                />
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter className="flex flex-col gap-4 border-t bg-muted/30 p-6">
                        <Button
                            type="submit"
                            className="w-full text-lg font-semibold"
                            size="lg"
                            disabled={analyzeMutation.isPending}
                        >
                            {analyzeMutation.isPending ? (
                                <>
                                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                    Analyzing Competitors...
                                </>
                            ) : (
                                <>
                                    <Search className="mr-2 h-5 w-5" />
                                    Generate Intel Report
                                </>
                            )}
                        </Button>
                        {analyzeMutation.isPending && (
                            <p className="text-center text-sm text-muted-foreground animate-pulse">
                                This usually takes 1-2 minutes. Please don't close this tab.
                            </p>
                        )}
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
