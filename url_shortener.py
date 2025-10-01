import sys
import hashlib
import json
import os

DATA_FILE = "url_data.json"

def load_urls():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_urls(urls):
    with open(DATA_FILE, "w") as f:
        json.dump(urls, f, indent=2)

def generate_short_code(url, urls):
    base_code = hashlib.md5(url.encode()).hexdigest()[:6]
    code = base_code
    counter = 1
    # Avoid duplicates for different URLs, simple linear probing
    while code in urls and urls[code] != url:
        code = base_code + str(counter)
        counter += 1
    return code

def shorten_url(url):
    urls = load_urls()
    code = generate_short_code(url, urls)
    urls[code] = url
    save_urls(urls)
    return code

def expand_url(code):
    urls = load_urls()
    if code in urls:
        return urls[code]
    else:
        return "Error: Code not found."

def delete_url(code):
    urls = load_urls()
    if code in urls:
        del urls[code]
        save_urls(urls)
        return "Deleted successfully."
    else:
        return "Error: Code not found."

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 url_shortener.py [shorten|expand|delete] [URL|code]")
        return
    cmd = sys.argv[1]
    if cmd == "shorten":
        url = sys.argv[2]
        code = shorten_url(url)
        print(f"Shortened URL code: {code}")
    elif cmd == "expand":
        code = sys.argv[2]
        result = expand_url(code)
        print(f"Original URL: {result}")
    elif cmd == "delete":
        code = sys.argv[2]
        result = delete_url(code)
        print(result)
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()
