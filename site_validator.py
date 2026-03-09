# =============================================================================
# site_validator.py
#
# Author  : Jose M. Beato
# Created : March 9, 2026
# Built with the assistance of Claude (Anthropic) — claude.ai
#
# Description:
#   Validates a list of branch network sites by checking that each
#   entry has a valid name and a non-placeholder IP address. Valid
#   sites are written to a CSV inventory file; failures are logged
#   to a separate error log for remediation.
#
# Project Setup (run in terminal before opening VS Code):
# ─────────────────────────────────────────────────────
#   1. cd /Users/jmb/PythonProjects
#   2. uv init bulk-site-validator
#   3. cd bulk-site-validator
#   4. code .
#   5. python3 -m venv .venv
#   6. source .venv/bin/activate
#   # No extra packages — 100% Python standard library
#   # Create this file as: site_validator.py
#
# GitHub Commit (after completing):
# ──────────────────────────────────
#   git add site_validator.py
#   git commit -m "refactor: standardize site_validator.py header and structure"
#   git push origin main
# =============================================================================

import time       # Built-in: simulate connection delay per site
import csv        # Built-in: write validated inventory to CSV
from datetime import datetime  # Built-in: timestamp for log entries


# =============================================================================
# SECTION 1 — CONFIGURATION
# Best Practice: Keep file paths and thresholds at the top of the script
# so they're easy to find and update without touching the core logic.
# =============================================================================

OUTPUT_CSV   = "validated_inventory.csv"  # Validated sites output
FAILURE_LOG  = "failed_sites.log"         # Errors and invalid entries
CHECK_DELAY  = 0.1                         # Seconds between site checks


# =============================================================================
# SECTION 2 — VALIDATION LOGIC
# Best Practice: Separate validation rules from I/O. If the rules change,
# you update this one function without touching file-writing code.
# =============================================================================


def validate_site(site, index):
    """
    Validates a single site dictionary for required fields and IP integrity.

    Args:
        site  (dict): Site record with 'name' and 'ip' keys.
        index (int):  1-based position in the input list (for logging).

    Returns:
        dict | None: Validated record dict, or None if invalid.

    Raises:
        ValueError: If name is missing or IP is absent/placeholder.
    """
    name = site.get("name")
    ip   = site.get("ip")

    if not name or not ip or ip == "0.0.0.0":
        raise ValueError(f"Missing name or invalid IP: ip='{ip}'")

    return {"site_name": name, "ip_address": ip, "status": "READY"}


# =============================================================================
# SECTION 3 — BATCH VALIDATION
# Best Practice: The batch function handles I/O (logging) and delegates
# the validation decision to validate_site(). Keeps concerns separated.
# =============================================================================


def validate_sites(site_list):
    """
    Iterates over all sites, validates each one, logs failures, and
    writes valid sites to a CSV inventory file.

    Args:
        site_list (list[dict]): Raw list of site records to validate.

    Returns:
        tuple[int, int]: (success_count, failure_count)
    """
    success_count  = 0
    failure_count  = 0
    validated_data = []

    print()
    print("=" * 60)
    print("  site_validator.py — Starting...")
    print("=" * 60)
    print(f"\n[INFO] Validating {len(site_list)} sites...\n")

    with open(FAILURE_LOG, "w") as log_file:
        log_file.write(f"--- Audit Started: {datetime.now()} ---\n")

        for index, site in enumerate(site_list, start=1):
            try:
                time.sleep(CHECK_DELAY)
                record = validate_site(site, index)
                validated_data.append(record)
                print(f"  [{index}] [INFO]  VALID   → {record['site_name']} ({record['ip_address']})")
                success_count += 1

            except Exception as e:
                site_id = site.get("name", f"Index-{index}")
                log_file.write(f"[{datetime.now()}] SITE: {site_id} | REASON: {e}\n")
                print(f"  [{index}] [WARN]  INVALID → {site_id} — logged to {FAILURE_LOG}")
                failure_count += 1

    # Write all valid sites to CSV
    if validated_data:
        with open(OUTPUT_CSV, "w", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=["site_name", "ip_address", "status"]
            )
            writer.writeheader()
            writer.writerows(validated_data)
        print(f"\n[INFO] Validated inventory written → '{OUTPUT_CSV}'")

    return success_count, failure_count


# =============================================================================
# SECTION 4 — SUMMARY PRINT
# Best Practice: Always print a human-readable summary to the console
# so you know what happened when you run the script.
# =============================================================================


def print_summary(success_count, failure_count):
    """
    Prints a formatted validation summary to the console.

    Args:
        success_count (int): Number of sites that passed validation.
        failure_count (int): Number of sites that failed validation.
    """
    total = success_count + failure_count
    print()
    print("=" * 60)
    print("  SITE VALIDATOR — SUMMARY REPORT")
    print("  Jose M. Beato | March 9, 2026")
    print("=" * 60)
    print(f"  Total sites checked : {total}")
    print(f"  Valid (READY)       : {success_count}")
    print(f"  Invalid (FAILED)    : {failure_count}")
    print(f"  Output CSV          : {OUTPUT_CSV}")
    print(f"  Failure log         : {FAILURE_LOG}")
    print("=" * 60)
    print()


# =============================================================================
# SECTION 5 — MAIN ENTRY POINT
# Best Practice: Always use `if __name__ == "__main__"` to protect your
# main logic. This allows other scripts to import validate_sites()
# without automatically running the pipeline.
# =============================================================================


def main():
    """
    Orchestrates the full pipeline:
    Validate Sites → Write CSV → Print Summary
    """
    raw_sites = [
        {"name": "NY-DATA-01",  "ip": "10.0.0.1"},
        {"name": "LON-OFFICE",  "ip": "0.0.0.1"},     # Bad IP — will fail
        {"ip": "172.16.5.4"},                           # Missing name — will fail
        {"name": "TOK-RETAIL",  "ip": "192.168.1.50"},
    ]

    success_count, failure_count = validate_sites(raw_sites)
    print_summary(success_count, failure_count)


if __name__ == "__main__":
    main()

