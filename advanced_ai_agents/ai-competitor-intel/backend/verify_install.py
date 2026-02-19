try:
    from agno.tools.firecrawl import FirecrawlTools
    print("Successfully imported FirecrawlTools")
except ImportError as e:
    print(f"Failed to import FirecrawlTools: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    import firecrawl
    print(f"Successfully imported firecrawl: {firecrawl.__file__}")
except ImportError as e:
    print(f"Failed to import firecrawl: {e}")
