import requests
import re
from typing import Optional, Dict, Any

def get_problem_details(title_slug: str) -> Optional[Dict[str, Any]]:
    """Fetch problem details from LeetCode GraphQL API."""
    url = "https://leetcode.com/graphql"
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        difficulty
        topicTags {
          name
        }
      }
    }
    """
    variables = {"titleSlug": title_slug}
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }
    payload = {"query": query, "variables": variables}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "errors" in data or not data.get("data", {}).get("question"):
            return None
        return data["data"]["question"]
    except requests.exceptions.RequestException:
        return None

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')
