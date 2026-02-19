# Test Script for AI Competitor Intelligence API

$baseUrl = "http://127.0.0.1:8000"
$testEmail = "test_user_$(Get-Date -Format "yyyyMMdd_HHmmss")@example.com"

Write-Host "--- 1. Registering New User ---" -ForegroundColor Cyan
$regResponse = Invoke-RestMethod -Uri "$baseUrl/register" -Method Post -ContentType "application/json" -Body "{`"email`": `"$testEmail`"}"
$apiKey = $regResponse.api_key
Write-Host "New API Key: $apiKey" -ForegroundColor Green

Write-Host "`n--- 2. Checking Usage ---" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$baseUrl/usage" -Method Get -Headers @{"X-Api-Key" = $apiKey } | ConvertTo-Json

Write-Host "`n--- 3. Running Competitor Analysis (Marmeto) ---" -ForegroundColor Cyan
Write-Host "This may take 30-60 seconds (using free scraper)..." -ForegroundColor Yellow
$analyzeBody = @{
    company_url     = "https://marmeto.com"
    max_competitors = 1
    search_engine   = "tavily"
} | ConvertTo-Json

$analysis = Invoke-RestMethod -Uri "$baseUrl/analyze" -Method Post -Headers @{"X-Api-Key" = $apiKey } -ContentType "application/json" -Body $analyzeBody
Write-Host "`n--- Analysis Result ---" -ForegroundColor Green
$analysis | ConvertTo-Json
