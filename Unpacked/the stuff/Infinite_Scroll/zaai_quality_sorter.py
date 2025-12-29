
import os
import shutil
from pathlib import Path
from hashlib import md5
from datetime import datetime

# === CONFIG ===
source_dir = "/storage/emulated/0"
target_base = Path("/storage/emulated/0/ZAAI_CORE")
log_path = target_base / "Logs" / "zaai_sort_log.txt"

# === FILE CATEGORIES ===
categories = {
    "Audio": [".mp3", ".wav", ".m4a"],
    "Documents": [".pdf", ".docx", ".txt", ".md", ".pptx", ".xls", ".xlsx"],
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".sh", ".apk", ".exe", ".py"],
    "Data": [".csv", ".json", ".xml", ".db"]
}

# === PREP FOLDERS ===
for folder in categories.keys():
    (target_base / folder).mkdir(parents=True, exist_ok=True)
(target_base / "Duplicates").mkdir(parents=True, exist_ok=True)
(target_base / "Logs").mkdir(parents=True, exist_ok=True)

# === HASHING FOR DUPES ===
hashes = {}
log_entries = []

def get_file_hash(path):
    try:
        with open(path, "rb") as f:
            return md5(f.read()).hexdigest()
    except:
        return None

def categorize_file(ext):
    for folder, extensions in categories.items():
        if ext.lower() in extensions:
            return folder
    return "Other"

# === RECURSIVE SORT + LOG ===
for root, dirs, files in os.walk(source_dir):
    for filename in files:
        file_path = Path(root) / filename
        ext = file_path.suffix
        category = categorize_file(ext)
        target_folder = target_base / category
        target_file = target_folder / filename
        hash_val = get_file_hash(file_path)

        try:
            if hash_val in hashes:
                # === DUPLICATE ===
                dup_path = target_base / "Duplicates" / filename
                shutil.copy2(file_path, dup_path)
                print(f"♻️  DUPLICATE: {filename} → Duplicates/")
                log_entries.append(f"DUPLICATE: {file_path} → Duplicates/")
            else:
                shutil.copy2(file_path, target_file)
                print(f"✅ {filename} → {category}/")
                log_entries.append(f"MOVED: {file_path} → {category}/")
                hashes[hash_val] = file_path
        except Exception as e:
            print(f"❌ ERROR with {filename}: {e}")
            log_entries.append(f"ERROR: {filename} → {e}")

# === WRITE LOG ===
with open(log_path, "a", encoding="utf-8") as log:
    log.write(f"\n\n=== SORT LOG {datetime.now()} ===\n")
    for entry in log_entries:
        log.write(entry + "\n")

print("✅ All files processed. Check ZAAI_CORE/Logs/ for detailed results.")
