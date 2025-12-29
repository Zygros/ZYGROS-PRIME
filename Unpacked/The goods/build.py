#!/usr/bin/env python3
import os, json, zipfile, datetime, pathlib, shutil

BASE = "/mnt/data"
DIST = f"{BASE}/dist"
INPUT = f"{BASE}/input"
CATALOG_PATH = f"{DIST}/catalog.json"

def zipdir(zf, path, arcbase=""):
    for root, _, files in os.walk(path):
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, path)
            zf.write(full, os.path.join(arcbase, rel))

def main():
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)
    assets_total = 0

    # Build per-pack archives if assets or manifests exist
    for p in catalog["packs"]:
        pack_id = p["id"]
        pack_dir = os.path.join(INPUT, pack_id)
        if not os.path.isdir(pack_dir):
            continue
        out_zip = os.path.join(DIST, f"{pack_id}.zip")
        with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
            # include manifest
            man_path = os.path.join(pack_dir, "pack.manifest.json")
            if os.path.exists(man_path):
                z.write(man_path, f"{pack_id}/pack.manifest.json")
            # include assets dir (may be empty)
            assets_dir = os.path.join(pack_dir, "assets")
            if os.path.isdir(assets_dir):
                zipdir(z, assets_dir, f"{pack_id}/assets")
                # count assets
                for _, _, files in os.walk(assets_dir):
                    assets_total += len(files)

    # Make ultimate bundle (all per-pack zips)
    bundle_zip = os.path.join(DIST, "ultimate-pack-v1.zip")
    with zipfile.ZipFile(bundle_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for fname in os.listdir(DIST):
            if fname.endswith(".zip") and fname not in ["ultimate-pack-v1.zip", "ultimate-pack-lite.zip"]:
                z.write(os.path.join(DIST, fname), f"packs/{fname}")
        # include docs
        z.write(os.path.join(BASE, "docs", "README.md"), "docs/README.md")
        z.write(os.path.join(BASE, "docs", "LICENSE-standard.md"), "docs/LICENSE-standard.md")
        z.write(os.path.join(BASE, "docs", "CHANGELOG.md"), "docs/CHANGELOG.md")
        z.write(CATALOG_PATH, "dist/catalog.json")

    # Lite zip: just catalog + README (no assets)
    lite_zip = os.path.join(DIST, "ultimate-pack-lite.zip")
    with zipfile.ZipFile(lite_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(BASE, "docs", "README.md"), "docs/README.md")
        z.write(CATALOG_PATH, "dist/catalog.json")

    # Update assets count
    catalog["assets_count"] = assets_total
    catalog["generated_at"] = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=2)

if __name__ == "__main__":
    main()
