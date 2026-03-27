from tavily import TavilyClient
from config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query: str) -> str:
    results = tavily.search(query=query, max_results=3)
    output = ""
    for result in results["results"]:
        output += f"Title: {result['title']}\n"
        output += f"Content: {result['content']}\n\n"
    return output


def needs_web_search(query: str, client) -> bool:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{
            "role": "user",
            "parts": [{"text": f"Does this question require current/real-time information from the web to answer accurately? Reply with only YES or NO.\n\nQuestion: {query}"}]
        }]
    )
    return response.text.strip().upper() == "YES"