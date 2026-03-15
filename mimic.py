import requests
import time
import random

# لیست سایت‌های امن برای شبیه‌سازی ترافیک
safe_sites = ["https://www.google.com", "https://www.wikipedia.org", "https://www.bing.com"]

def mimic():
    print("Ghost-Mimic is active. Simulating normal traffic...")
    while True:
        try:
            url = random.choice(safe_sites)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            requests.get(url, headers=headers, timeout=10)
        except:
            pass
        # وقفه تصادفی بین ۳۰ تا ۱۸۰ ثانیه
        time.sleep(random.randint(30, 180))

if __name__ == "__main__":
    mimic()
