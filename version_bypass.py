# version_bypass.py

import json
import shutil
import logging
import platform
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def find_product_json(cursor_path: Path) -> Path:
    """
    Recursively search for a 'product.json' file under cursor_path.
    If none, optionally look for 'package.json' containing a version field.
    Return the first one found, or None if not found.
    """
    for root, dirs, files in os.walk(cursor_path):
        if "product.json" in files:
            return Path(root) / "product.json"
        # Some older versions may store version in package.json
        if "package.json" in files:
            # If we detect a valid version field inside, consider it
            pj = Path(root) / "package.json"
            try:
                with open(pj, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "version" in data:
                        return pj
            except:
                continue
    return None


def backup_file(fp: Path):
    if fp.exists():
        bak = fp.with_name(fp.name + ".bak")
        shutil.copy2(fp, bak)
        logging.info(f"  ‣ Backed up: {bak}")


def bypass_version(cursor_path: Path, target_version: str = "0.48.7"):
    """
    1) Locate product.json (or package.json) under cursor_path.
    2) Read its current version.
    3) If current < 0.46.0 (lexicographically), overwrite it with target_version.
    """
    pj = find_product_json(cursor_path)
    if not pj:
        logging.error(f"  ‣ No product.json or package.json found under {cursor_path}.")
        return False

    try:
        with open(pj, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"  ‣ Failed to load JSON from {pj}: {e}")
        return False

    current_version = data.get("version") or data.get("appVersion") or None
    if not current_version:
        logging.warning(f"  ‣ No 'version' field in {pj}. Cannot bypass.")
        return False

    logging.info(f"  ‣ Found version {current_version} in {pj}.")

    # Compare lexicographically (only works if version strings are in semver order)
    if current_version >= "0.50.5":
        logging.info(f"  ‣ Current version ({current_version}) ≥ 0.46.0. No bypass needed.")
        return True

    # Else, patch it:
    backup_file(pj)
    data["version"] = target_version
    try:
        with open(pj, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"  ‣ Overwrote version in {pj} → {target_version}.")
        return True
    except Exception as e:
        logging.error(f"  ‣ Failed to write patched version: {e}")
        return False


def reset_current_version(cursor_path: Path, force_version: str):
    """
    Convenience wrapper to call bypass_version with a non‐default target.
    """
    return bypass_version(cursor_path, target_version=force_version)
