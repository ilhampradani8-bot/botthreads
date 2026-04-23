import json
import urllib.request
import urllib.error

ACCESS_TOKEN = "K0b0PvmVoY1WavmBEhifaAjXvJaEyfer94D2ZLO6LV5"
CHANNEL_ID = "69e9e10b031bfa423c3437ba"
ENDPOINT = "https://api.buffer.com"

def test_thread():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    query = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            text
          }
        }
        ... on MutationError {
          message
        }
      }
    }
    """
    
    variables = {
        "input": {
            "text": "Post Utama: Testing Fitur Thread (Post 1)",
            "channelId": CHANNEL_ID,
            "schedulingType": "automatic",
            "mode": "shareNow",
            "metadata": {
                "threads": {
                    "thread": [
                        {"text": "Balasan Otomatis: Ini adalah isi balasan (Post 2)"}
                    ]
                }
            }
        }
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        print("Mencuba posting thread manual...")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Ralat: {e}")

if __name__ == "__main__":
    test_thread()
