import os
import json
import urllib.request
import urllib.error
from datetime import datetime

# Configuration
BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
BUFFER_CHANNEL_ID = os.getenv("BUFFER_CHANNEL_ID")
BUFFER_ENDPOINT = "https://api.buffer.com"

def get_keys():
    global BUFFER_ACCESS_TOKEN, BUFFER_CHANNEL_ID
    if not BUFFER_ACCESS_TOKEN or not BUFFER_CHANNEL_ID:
        try:
            with open("/home/ilham/botthreads/.env", "r") as f:
                for line in f:
                    if line.startswith("BUFFER_ACCESS_TOKEN="):
                        BUFFER_ACCESS_TOKEN = line.split("=", 1)[1].strip()
                    if line.startswith("BUFFER_CHANNEL_ID="):
                        BUFFER_CHANNEL_ID = line.split("=", 1)[1].strip()
        except Exception:
            pass

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "/home/ilham/botthreads/posting.log"
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def get_it_tip():
    """Fetch a natural, SEO-friendly IT tip from Groq (groq.com) in Bahasa Malaysia."""
    key = None
    try:
        with open("/home/ilham/botthreads/.env", "r") as f:
            for line in f:
                if line.startswith("GROQ_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    except Exception:
        pass
        
    if not key:
        log_message("Warning: GROQ_API_KEY not set. Using fallback tip.")
        return "Tips IT: Pastikan anda sentiasa mengemaskini perisian peranti untuk keselamatan yang lebih baik. Langkah mudah ini membantu melindungi data peribadi anda daripada ancaman siber."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}',
        'User-Agent': 'Mozilla/5.0'
    }
    
    # Prompt for natural, SEO-friendly content without hashtags
    prompt = """
    Anda adalah pakar strategi kandungan untuk MIJ Digital di Malaysia.
    Tugas anda adalah mencipta postingan Threads yang sangat natural, profesional, dan mesra SEO.
    
    Kriteria:
    1. Kandungan IT dalam Bahasa Malaysia (Bahasa Melayu moden).
    2. JANGAN gunakan sebarang hashtag (#).
    3. HAD PANJANG: Tulis dalam 1 atau 2 ayat sahaja (Maksimum 300 aksara). 
    4. Gaya bahasa: Natural, seperti manusia berkongsi ilmu di media sosial.
    5. Berikan teks postingan SAHAJA.
    """
    
    data = {
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Sediakan satu postingan IT yang natural dan berimpak untuk hari ini."}
        ],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.7
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    
    try:
        log_message("Menjana kandungan AI natural via Groq...")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            tip = result['choices'][0]['message']['content'].strip()
            if tip.startswith('"') and tip.endswith('"'):
                tip = tip[1:-1]
            return tip
    except Exception as e:
        log_message(f"Error fetching tip from Groq: {e}")
        return "Tips IT: Keselamatan siber bermula dengan kesedaran kita. Sentiasa berhati-hati dengan pautan yang mencurigakan dalam e-mel anda."

def post_to_threads(content):
    """Post natural content to Threads via Buffer GraphQL API."""
    get_keys()
    if not BUFFER_ACCESS_TOKEN or not BUFFER_CHANNEL_ID:
        log_message("Error: Buffer Access Token atau Channel ID tidak dijumpai.")
        return False

    headers = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    # Strict character limit safety net
    if len(content) > 500:
        log_message(f"Warning: Teks terlalu panjang ({len(content)}). Memotong secara paksa...")
        content = content[:497] + "..."

    query = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post { id }
        }
        ... on MutationError { message }
      }
    }
    """
    
    variables = {
        "input": {
            "text": content,
            "channelId": BUFFER_CHANNEL_ID,
            "schedulingType": "automatic",
            "mode": "shareNow"
        }
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    req = urllib.request.Request(BUFFER_ENDPOINT, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        log_message(f"Memposting ke Threads (Panjang: {len(content)} aksara)...")
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            
            if "errors" in response_data:
                log_message(f"GraphQL Error: {response_data['errors']}")
                return False
                
            create_post_result = response_data.get("data", {}).get("createPost", {})
            if "post" in create_post_result:
                log_message(f"BERHASIL: Post ID {create_post_result['post']['id']}")
                return True
            elif "message" in create_post_result:
                log_message(f"GAGAL: {create_post_result['message']}")
                return False
            else:
                log_message(f"Respons tidak dikenali: {response_data}")
                return False
    except Exception as e:
        log_message(f"Error posting to Buffer: {e}")
        return False

def run_job():
    content = get_it_tip()
    if content:
        return post_to_threads(content)
    return False

if __name__ == "__main__":
    run_job()
