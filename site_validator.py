import time
import csv
from datetime import datetime


def validate_sites(site_list):
    success_count = 0
    failure_count = 0
    validated_data = []  # List to store "Good" sites

    print(f"🚀 Starting validation of {len(site_list)} sites...\n")

    with open("failed_sites.log", "w") as log_file:
        log_file.write(f"--- Audit Started: {datetime.now()} ---\n")

        for index, site in enumerate(site_list, start=1):
            try:
                time.sleep(0.1)
                name = site.get("name")
                ip = site.get("ip")

                if not name or not ip or ip == "0.0.0.0":
                    raise ValueError(f"Missing Name or Invalid IP: {ip}")

                print(f"[{index}] ✅ VALID: {name}")
                # Store the good data
                validated_data.append(
                    {"site_name": name, "ip_address": ip, "status": "READY"}
                )
                success_count += 1

            except Exception as e:
                site_id = site.get("name", f"Index-{index}")
                log_file.write(f"[{datetime.now()}] SITE: {site_id} | REASON: {e}\n")
                print(f"[{index}] ❌ ERROR: Logged to failed_sites.log")
                failure_count += 1

    # --- NEW: Write the Success Log (CSV) ---
    if validated_data:
        with open("validated_inventory.csv", "w", newline="") as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=["site_name", "ip_address", "status"]
            )
            writer.writeheader()
            writer.writerows(validated_data)
        print(f"\n📦 Success: 'validated_inventory.csv' generated.")

    print(f"📋 SUMMARY: {success_count} Success / {failure_count} Failed")


if __name__ == "__main__":
    raw_sites = [
        {"name": "NY-DATA-01", "ip": "10.0.0.1"},
        {"name": "LON-OFFICE", "ip": "0.0.0.1"},  # Bad IP
        {"ip": "172.16.5.4"},  # Missing Name
        {"name": "TOK-RETAIL", "ip": "192.168.1.50"},  # Good
    ]
    validate_sites(raw_sites)
