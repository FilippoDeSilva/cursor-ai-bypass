# machine_reset.py

import os
import sys
import uuid
import hashlib
import json
import sqlite3
import shutil
import logging
import platform
import subprocess
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def _get_default_paths(config):
    """
    Determine default storage.json, state.vscdb, and machineId paths 
    based on OS and optional overrides in config.
    """
    home = Path.home()
    os_type = platform.system()

    # If user explicitly set paths in config, use those:
    storage_json = config.get("storage_json_path")
    sqlite_db    = config.get("sqlite_db_path")
    machine_id   = config.get("machine_id_path")

    if storage_json and sqlite_db and machine_id:
        return Path(storage_json).expanduser(), Path(sqlite_db).expanduser(), Path(machine_id).expanduser()

    if os_type == "Windows":
        # Windows: typically under %APPDATA%\Cursor\
        appdata = os.getenv("APPDATA")
        if not appdata:
            logging.error("APPDATA not found. Cannot detect Cursor paths on Windows.")
            sys.exit(1)
        base = Path(appdata) / "Cursor"
        storage_json = base / "User" / "globalStorage" / "storage.json"
        sqlite_db    = base / "User" / "globalStorage" / "state.vscdb"
        machine_id   = base / "machineId"

    elif os_type == "Darwin":
        # macOS: typically under ~/Library/Application Support/Cursor
        base = home / "Library" / "Application Support" / "Cursor"
        storage_json = base / "User" / "globalStorage" / "storage.json"
        sqlite_db    = base / "User" / "globalStorage" / "state.vscdb"
        machine_id   = base / "machineId"

    elif os_type == "Linux":
        # Linux: typically under ~/.config/Cursor
        base = home / ".config" / "Cursor"
        storage_json = base / "User" / "globalStorage" / "storage.json"
        sqlite_db    = base / "User" / "globalStorage" / "state.vscdb"
        # Some Linux installs use "machineid" (lowercase) or "machineId"
        mid1 = base / "machineId"
        mid2 = base / "machineid"
        machine_id = mid1 if mid1.exists() else (mid2 if mid2.exists() else mid1)

    else:
        logging.error(f"Unsupported OS: {os_type}")
        sys.exit(1)

    return storage_json, sqlite_db, machine_id


def generate_new_ids():
    """
    Create new random IDs exactly as the repo expects:
      - telemetry.devDeviceId: UUID4
      - telemetry.machineId: SHA256(random)
      - telemetry.macMachineId: SHA512(random)
      - telemetry.sqmId: uppercase UUID4 in braces
      - storage.serviceMachineId: UUID4
    """
    return {
        "telemetry.devDeviceId":   str(uuid.uuid4()),
        "telemetry.machineId":     hashlib.sha256(os.urandom(32)).hexdigest(),
        "telemetry.macMachineId":  hashlib.sha512(os.urandom(64)).hexdigest(),
        "telemetry.sqmId":         "{" + str(uuid.uuid4()).upper() + "}",
        "storage.serviceMachineId": str(uuid.uuid4()),
    }


def backup_file(fp: Path):
    """
    Create a timestamped .bak backup if file exists.
    """
    if fp.exists():
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        bak = fp.with_name(fp.name + f".{ts}.bak")
        shutil.copy2(fp, bak)
        logging.info(f"  ‣ Backup saved: {bak}")


def patch_storage_json(storage_json: Path, ids: dict):
    """
    Update storage.json by setting keys from ids dict.
    """
    if not storage_json.exists():
        logging.warning(f"storage.json not found at {storage_json}. Skipping JSON patch.")
        return False

    backup_file(storage_json)
    try:
        with open(storage_json, "r+", encoding="utf-8") as f:
            data = json.load(f) if storage_json.stat().st_size > 0 else {}
            # Merge new IDs
            for k, v in ids.items():
                data[k] = v
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        logging.info("  ‣ storage.json patched.")
        return True
    except Exception as e:
        logging.error(f"  ‣ Failed to patch storage.json: {e}")
        return False


def patch_sqlite_db(sqlite_db: Path, ids: dict):
    """
    Update state.vscdb: for each key in ids, do an UPSERT into ItemTable.
    If the table/key doesn't exist exactly as upstream expects, this replicates the repo's logic.
    """
    if not sqlite_db.exists():
        logging.warning(f"SQLite DB not found at {sqlite_db}. Skipping DB patch.")
        return False

    backup_file(sqlite_db)
    try:
        conn = sqlite3.connect(str(sqlite_db))
        cur = conn.cursor()
        # Ensure ItemTable exists. Upstream always has it, but just in case:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ItemTable (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        # Insert or replace (UPSERT)
        for k, v in ids.items():
            cur.execute("""
                INSERT INTO ItemTable (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value;
            """, (k, v))
        conn.commit()
        conn.close()
        logging.info("  ‣ state.vscdb patched.")
        return True
    except Exception as e:
        logging.error(f"  ‣ Failed to patch SQLite DB: {e}")
        return False


def patch_machine_id(machine_id_path: Path, new_mid: str):
    """
    Overwrite the machineId file with new_mid (SHA256).
    """
    if not machine_id_path.exists():
        logging.warning(f"machineId file not found at {machine_id_path}. Skipping machineId patch.")
        return False

    backup_file(machine_id_path)
    try:
        with open(machine_id_path, "w", encoding="utf-8") as f:
            f.write(new_mid)
        logging.info("  ‣ machineId file patched.")
        return True
    except Exception as e:
        logging.error(f"  ‣ Failed to patch machineId file: {e}")
        return False


def reset_machine_identifiers(config: dict):
    """
    Master function to reset:
      1) OS‐level machine ID (Windows: Registry/PS, Linux: dbus-machine-id, macOS: skipped)
      2) storage.json
      3) state.vscdb
      4) machineId file under Cursor
    """
    os_type = platform.system()
    logging.info(f"➜  Resetting machine IDs on {os_type}...")

    # 1) OS‐level machine ID:
    try:
        if os_type == "Windows":
            # Remove SQMClient MachineId from registry (requires Admin)
            subprocess.run([
                "powershell", "-Command",
                "Remove-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\SQMClient' -Name 'MachineId' -ErrorAction SilentlyContinue"
            ], check=False, capture_output=True)
            logging.info("  ‣ Windows registry MachineId entry removed (if existed).")

        elif os_type == "Linux":
            # Remove and re‐generate /var/lib/dbus/machine-id
            # Many distros require sudo; if not run as root, this may fail.
            _ = subprocess.run(["sudo", "rm", "-f", "/var/lib/dbus/machine-id"], capture_output=True)
            _ = subprocess.run(["sudo", "dbus-uuidgen", "--ensure"], capture_output=True)
            logging.info("  ‣ Linux /var/lib/dbus/machine-id regenerated (if sudo permitted).")

        elif os_type == "Darwin":
            # macOS does not expose a simple machine ID to patch, so skip.
            logging.info("  ‣ macOS detected: skipping OS‐level machine ID (no public method).")

        else:
            logging.warning(f"  ‣ Unsupported OS: {os_type}. OS‐level machine ID not patched.")
    except Exception as e:
        logging.error(f"  ‣ Failed OS‐level reset: {e}")

    # 2) Patch Cursor‐specific files:
    storage_json, sqlite_db, machine_id_file = _get_default_paths(config)
    new_ids = generate_new_ids()

    # a) Patch storage.json
    r1 = patch_storage_json(storage_json, new_ids)

    # b) Patch state.vscdb
    r2 = patch_sqlite_db(sqlite_db, new_ids)

    # c) Patch machineId file (use telemetry.machineId for content)
    mid = new_ids["telemetry.machineId"]
    r3 = patch_machine_id(machine_id_file, mid)

    if r1 or r2 or r3:
        logging.info("✔ Machine identifiers reset completed (Cursor side).")
    else:
        logging.error("✘ None of the Cursor files could be patched. Please check paths/permissions.")

