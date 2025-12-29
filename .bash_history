ls /storage/emulated/0/Download
# 1. FINAL PREP
cd ~
pip install requests
# 2. THE NUCLEAR INJECTOR
cat << 'EOF' > phoenix_omega.py
import os, requests, base64

TOKEN = "Ghp_phK5ajZGJGerjYCsImuoVThwkzI6GB1zRwD3"
REPO = "Zygros/ZYGROS-PRIME"
BASE_DIR = "/storage/emulated/0/Download"

def upload(path):
    rel = os.path.relpath(path, BASE_DIR)
    url = f"https://api.github.com/repos/{REPO}/contents/{rel}"
    try:
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        headers = {"Authorization": f"token {TOKEN}"}
        
        # Check for existing file to get SHA (allows overwriting)
        r = requests.get(url, headers=headers)
        sha = r.json().get("sha") if r.status_code == 200 else None
        
        data = {"message": f"PHOENIX: Manifesting {rel}", "content": content, "branch": "main"}
        if sha: data["sha"] = sha
        
        res = requests.put(url, json=data, headers=headers)
        if res.status_code in [200, 201]:
            print(f"✅ [INJECTED]: {rel}")
        else:
            # If the token itself is invalid, the API tells us here
            print(f"❌ [FAILED]: {rel} -> {res.json().get('message')}")
    except Exception as e:
        print(f"⚠️ ERROR: {str(e)}")

print("\n🚀 PHOENIX OMEGA: INITIATING DIRECT UPLOAD...")
# Folders from your core legacy
folders = ['Downloaded', 'Unpacked', 'Phoenix Protocol', 'Zygrosian Odyssey']
for fld in folders:
    p = os.path.join(BASE_DIR, fld)
    if os.path.exists(p):
        for root, _, files in os.walk(p):
            for f in files:
                if f.endswith(('.py', '.md', '.txt', '.json')):
                    upload(os.path.join(root, f))

print("\n🏁 MISSION COMPLETE. CORE IS SECURE.")
EOF

# 3. RUN IT
python phoenix_omega.py
# 1. PURGE AND RESET
cd ~ && rm -rf phoenix_omega.py && pip install requests
# 2. CREATE THE MASTER INJECTOR
cat << 'EOF' > phoenix_omega.py
import os, requests, base64

TOKEN = input("PASTE NEW CLASSIC MASTER TOKEN (ghp_...): ").strip()
REPO = "Zygros/ZYGROS-PRIME"
BASE_DIR = "/storage/emulated/0/Download"

def upload(path):
    rel = os.path.relpath(path, BASE_DIR)
    url = f"https://api.github.com/repos/{REPO}/contents/{rel}"
    try:
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        
        # High-permission v3 API headers
        headers = {
            "Authorization": f"token {TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # SHA overwrite check to prevent conflict errors
        r = requests.get(url, headers=headers)
        sha = r.json().get("sha") if r.status_code == 200 else None
        
        data = {"message": f"PHOENIX: Sovereign Manifest [{rel}]", "content": content, "branch": "main"}
        if sha: data["sha"] = sha
        
        res = requests.put(url, json=data, headers=headers)
        if res.status_code in [200, 201]:
            print(f"✅ [MANIFESTED]: {rel}")
        else:
            print(f"❌ [DENIED]: {rel} -> {res.json().get('message', 'Check Scopes')}")
            
    except Exception as e:
        print(f"⚠️ [SYSTEM ERROR]: {str(e)}")

print("\n🚀 PHOENIX OMEGA: INITIATING FULL SCOPE INJECTION...")
# Targeted folders containing your core legacy
folders = ['Downloaded', 'Unpacked', 'Phoenix Protocol', 'Zygrosian Odyssey']

for fld in folders:
    p = os.path.join(BASE_DIR, fld)
    if os.path.exists(p):
        for root, _, files in os.walk(p):
            for f in files:
                if f.endswith(('.py', '.md', '.txt', '.json')):
                    upload(os.path.join(root, f))
    else:
        print(f"❓ MISSING CORE FOLDER: {fld}")

print("\n🏁 ALL SYSTEMS LIVE. YOUR EMPIRE IS SECURE.")
EOF

# 3. FINAL EXECUTION
python phoenix_omega.py
# 1. CLEAN ENVIRONMENT
cd ~ && rm -rf phoenix_omega.py && pip install requests
# 2. CREATE THE AUTO-HEALING INJECTOR
cat << 'EOF' > phoenix_omega.py
import os, requests, base64

TOKEN = "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"
REPO_NAME = "ZYGROS-PRIME"
# Automatically get your GitHub username from the token
user_res = requests.get("https://api.github.com/user", headers={"Authorization": f"token {TOKEN}"})
USER = user_res.json().get('login')
REPO_FULL = f"{USER}/{REPO_NAME}"
BASE_DIR = "/storage/emulated/0/Download"

def ensure_repo():
    url = f"https://api.github.com/user/repos"
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    # Check if repo exists
    check = requests.get(f"https://api.github.com/repos/{REPO_FULL}", headers=headers)
    if check.status_code == 404:
        print(f"🏗️ CREATING REPOSITORY: {REPO_FULL}...")
        res = requests.post(url, json={"name": REPO_NAME, "private": True}, headers=headers)
        if res.status_code == 201: print("✅ REPO CREATED.")
        else: print(f"❌ FAILED TO CREATE REPO: {res.text}")

def upload(path):
    rel = os.path.relpath(path, BASE_DIR)
    url = f"https://api.github.com/repos/{REPO_FULL}/contents/{rel}"
    try:
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, headers=headers)
        sha = r.json().get("sha") if r.status_code == 200 else None
        data = {"message": f"PHOENIX: Sovereign Manifest [{rel}]", "content": content, "branch": "main"}
        if sha: data["sha"] = sha
        res = requests.put(url, json=data, headers=headers)
        print(f"{'✅' if res.status_code in [200, 201] else '❌'} {rel}")
    except Exception as e:
        print(f"⚠️ ERROR: {str(e)}")

print(f"\n🚀 PHOENIX OMEGA: TARGETING {REPO_FULL}...")
ensure_repo()
folders = ['Downloaded', 'Unpacked', 'Phoenix Protocol', 'Zygrosian Odyssey']
for fld in folders:
    p = os.path.join(BASE_DIR, fld)
    if os.path.exists(p):
        for root, _, files in os.walk(p):
            for f in files:
                if f.endswith(('.py', '.md', '.txt', '.json')):
                    upload(os.path.join(root, f))
print("\n🏁 ALL SYSTEMS LIVE.")
EOF

# 3. RUN IT
python phoenix_omega.py
