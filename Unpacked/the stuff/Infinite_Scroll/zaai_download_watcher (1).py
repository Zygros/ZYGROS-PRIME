
import os
import shutil
import time
from datetime import datetime

DOWNLOAD_DIR = "/storage/emulated/0/Download"
ZAAI_CORE_DIR = "/storage/emulated/0/ZAAI_CORE"
LOG_FILE = os.path.join(ZAAI_CORE_DIR, "Logs", "watcher_log.txt")

EXTENSION_MAP = {
    '.pdf': 'PDFs',
    '.txt': 'Documents',
    '.docx': 'Documents',
    '.xlsx': 'Documents',
    '.csv': 'Documents',
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.mp4': 'Video',
    '.mkv': 'Video',
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.exe': 'Executables',
    '.py': 'Scripts'
}

def log(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def move_file(file_path):
    file_name = os.path.basename(file_path)
    _, ext = os.path.splitext(file_name)
    folder = EXTENSION_MAP.get(ext.lower(), "Other")
    dest_folder = os.path.join(ZAAI_CORE_DIR, folder)
    os.makedirs(dest_folder, exist_ok=True)

    target_path = os.path.join(dest_folder, file_name)
    if os.path.exists(target_path):
        dup_folder = os.path.join(ZAAI_CORE_DIR, "Duplicates")
        os.makedirs(dup_folder, exist_ok=True)
        target_path = os.path.join(dup_folder, file_name)

    shutil.move(file_path, target_path)
    log(f"Moved {file_path} to {target_path}")

def watch_download_folder():
    log("Watcher started.")
    seen_files = set(os.listdir(DOWNLOAD_DIR))
    try:
        while True:
            time.sleep(5)
            current_files = set(os.listdir(DOWNLOAD_DIR))
            new_files = current_files - seen_files
            for f in new_files:
                full_path = os.path.join(DOWNLOAD_DIR, f)
                if os.path.isfile(full_path):
                    move_file(full_path)
            seen_files = current_files
    except KeyboardInterrupt:
        log("Watcher stopped manually.")

if __name__ == "__main__":
    watch_download_folder()
