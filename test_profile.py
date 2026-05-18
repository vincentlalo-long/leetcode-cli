import requests
import json

def get_user_profile(username):
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
    payload = {"query": query, "variables": variables}
    
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    print(json.dumps(response.json(), indent=2))

get_user_profile("tourist")
