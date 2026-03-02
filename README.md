# Bulk Site Validator

A professional-grade infrastructure auditing tool designed to process large-scale site inventories. This utility focuses on **Defensive Programming**, ensuring that malformed data or missing attributes do not crash the migration workflow.

## 🚀 Key Features
* **Resilient Batch Processing:** Iterates through site dictionaries with granular `try-except` blocks to handle `KeyError` and `ValueError` without interruption.
* **Automated Error Logging:** Generates a timestamped `failed_sites.log` containing specific reasons for data rejection (e.g., invalid IP formats or missing site names).
* **Data Integrity Guardrails:** Validates IP address structures and mandatory fields before allowing a site into the "Validated Inventory."
* **Executive Summary:** Provides a high-level terminal report of success vs. failure counts for quick project management updates.

## 🏗️ Architecture
The tool uses an "Audit-First" approach. Instead of assuming data quality, it treats every input as potentially "dirty," making it ideal for SD-WAN migrations and global site hardware refreshes where source data (CSVs/Excel) is often inconsistent.



## 🛠️ Installation & Usage
1. **Sync Environment:**
   ```bash
   uv sync