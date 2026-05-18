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
        content
        hints
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

def get_daily_challenge() -> Optional[Dict[str, Any]]:
    """Fetch the current daily challenge from LeetCode."""
    url = "https://leetcode.com/graphql"
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
          questionId
          questionFrontendId
          title
          titleSlug
          difficulty
          topicTags {
            name
          }
        }
      }
    }
    """
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }
    payload = {"query": query}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "errors" in data or not data.get("data", {}).get("activeDailyCodingChallengeQuestion"):
            return None
        return data["data"]["activeDailyCodingChallengeQuestion"]["question"]
    except requests.exceptions.RequestException:
        return None

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_problem_by_id(frontend_id: str) -> Optional[Dict[str, str]]:
    """Fetch problem title and slug by frontend ID."""
    url = "https://leetcode.com/api/problems/all/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Normalize the input ID (e.g., '0001' -> '1')
        clean_id = str(int(frontend_id)) if frontend_id.isdigit() else frontend_id
        
        for p in data.get("stat_status_pairs", []):
            api_id = str(p.get("stat", {}).get("frontend_question_id"))
            clean_api_id = str(int(api_id)) if api_id.isdigit() else api_id
            
            if clean_api_id == clean_id:
                return {
                    "title": p["stat"]["question__title"],
                    "slug": p["stat"]["question__title_slug"]
                }
    except requests.exceptions.RequestException:
        pass
    return None

def get_all_problems() -> Optional[Dict[str, Any]]:
    """Fetch the list of all problems from LeetCode."""
    url = "https://leetcode.com/api/problems/all/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_user_profile(username: str) -> Optional[Dict[str, Any]]:
    """Fetch user profile stats from LeetCode GraphQL API."""
    url = "https://leetcode.com/graphql"
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
          reputation
          starRating
        }
      }
    }
    """
    variables = {"username": username}
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }
    payload = {"query": query, "variables": variables}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "errors" in data or not data.get("data", {}).get("matchedUser"):
            return None
        return data["data"]["matchedUser"]
    except requests.exceptions.RequestException:
        return None
