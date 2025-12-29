# Facebook Page posting via Graph API
import os, requests
from dotenv import load_dotenv
load_dotenv()

PAGE_ID = os.getenv("FB_PAGE_ID")
TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAYMENT_URL = os.getenv("PAYMENT_URL")

def post_to_page(message: str):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    r = requests.post(url, data={"message": message, "access_token": TOKEN}, timeout=20)
    r.raise_for_status()
    print("Posted to Facebook Page.")

if __name__ == "__main__":
    print("Fill PAGE_ID and TOKEN in .env, then call post_to_page(...)")
