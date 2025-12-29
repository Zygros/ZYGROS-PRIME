
import os
import shutil
import hashlib
from pathlib import Path

# === CONFIG ===
SOURCE_DIR = "/storage/emulated/0/Download/MyStuff"
DEST_DIR = "/storage/emulated/0/ZAAI_CORE"
DUPLICATES_DIR = os.path.join(DEST_DIR, "Duplicates")
CRASH_LOG = os.path.join(DEST_DIR, "crash_log.txt")

# === Create Folders ===
CATEGORIES = ["Audio", "Documents", "Images", "Executables", "Archives", "Logs", "Data"]
for cat in CATEGORIES + ["Duplicates"]:
    os.makedirs(os.path.join(DEST_DIR, cat), exist_ok=True)

# === File extensions map ===
EXT_MAP = {
    "Audio": [".mp3", ".wav", ".ogg", ".flac"],
    "Documents": [".pdf", ".docx", ".txt", ".md"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Executables": [".exe", ".sh", ".bin", ".apk"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Logs": [".log"],
    "Data": [".json", ".csv", ".xml"]
}

# === Helper Functions ===
hashes = set()

def get_hash(file_path):
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        log_crash(f"[HASH ERROR] {file_path} - {e}")
        return None

def log_crash(msg):
    with open(CRASH_LOG, "a") as f:
        f.write(msg + "\n")

def categorize_and_move(file_path):
    ext = file_path.suffix.lower()
    moved = False
    for cat, exts in EXT_MAP.items():
        if ext in exts:
            dest = os.path.join(DEST_DIR, cat, file_path.name)
            if not os.path.exists(dest):
                shutil.copy2(file_path, dest)
            moved = True
            break
    return moved

# === Main Sort Function ===
for root, dirs, files in os.walk(SOURCE_DIR):
    for name in files:
        full_path = Path(root) / name
        try:
            file_hash = get_hash(full_path)
            if not file_hash:
                continue
            if file_hash in hashes:
                shutil.copy2(full_path, os.path.join(DUPLICATES_DIR, name))
            else:
                hashes.add(file_hash)
                if not categorize_and_move(full_path):
                    # Unknown type — ignore or log
                    pass
        except Exception as e:
            log_crash(f"[SORT ERROR] {full_path} - {e}")

print("✅ Shielded sort complete. Check ZAAI_CORE and crash_log.txt.")
