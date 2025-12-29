#!/usr/bin/env python3
import os, sys, hashlib, zipfile, json, csv, datetime, io

TEXT_EXTS = {".md", ".txt", ".json", ".csv", ".py", ".yml", ".yaml", ".ini", ".toml", ".cfg", ".rst"}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_read_text(zf, zi, max_bytes=2_000_000):
    try:
        with zf.open(zi, "r") as f:
            data = f.read(max_bytes)
        try:
            return data.decode("utf-8", errors="replace")
        except:
            return data.decode("latin-1", errors="replace")
    except Exception as e:
        return f"<<ERROR READING {zi.filename}: {e}>>"

def main():
    if len(sys.argv) < 2:
        print("Usage: scan_local_zips.py <folder> [report_prefix]")
        sys.exit(2)
    root = os.path.abspath(sys.argv[1])
    prefix = sys.argv[2] if len(sys.argv) > 2 else "dropbox_zip_scan"
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    report_json = f"{prefix}_{ts}.json"
    report_csv  = f"{prefix}_{ts}.csv"

    results = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith(".zip"):
                p = os.path.join(dirpath, fn)
                entry = {
                    "zip_path": p,
                    "zip_sha256": sha256_file(p),
                    "size_bytes": os.path.getsize(p),
                    "files": []
                }
                try:
                    with zipfile.ZipFile(p, "r") as zf:
                        for zi in zf.infolist():
                            info = {
                                "name": zi.filename,
                                "size": zi.file_size,
                                "compressed_size": zi.compress_size,
                            }
                            ext = os.path.splitext(zi.filename)[1].lower()
                            if ext in TEXT_EXTS and zi.file_size <= 2_000_000:
                                info["preview"] = safe_read_text(zf, zi, 200_000)
                            entry["files"].append(info)
                except Exception as e:
                    entry["error"] = f"Failed to open zip: {e}"
                results.append(entry)

    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # CSV summary
    with open(report_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["zip_path","zip_sha256","size_bytes","internal_name","internal_size","internal_compressed_size"])
        for r in results:
            if "files" in r:
                for fi in r["files"]:
                    w.writerow([r["zip_path"], r["zip_sha256"], r["size_bytes"], fi.get("name",""), fi.get("size",""), fi.get("compressed_size","")])
            else:
                w.writerow([r["zip_path"], r["zip_sha256"], r["size_bytes"], "<<NO FILES OR ERROR>>", "", ""])

    print(f"Wrote {report_json}")
    print(f"Wrote {report_csv}")

if __name__ == "__main__":
    main()
