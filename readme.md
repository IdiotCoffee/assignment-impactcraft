# Invoice Data Generator & Percentile Analyzer

This project includes two Python scripts:

1. **Data Generation** — Creates synthetic invoice data with date, amount, and tag fields.
2. **Analysis** — Computes percentiles over the generated data in multiple modes.

---

## 📁 Scripts

### 1. `assignment.py` – Data Generation

Generates invoice entries and writes them to a CSV.

#### ✅ Features:
- Fields: `date`, `amount`, `tags`
- Two generation modes:
  - **Mode A (Date Range)**:
    - Generate invoices between a given start and end date.
    - Optionally specify number of transactions per day.
  - **Mode B (Random Spread)**:
    - Generate a fixed total number of invoices.
    - Spread randomly across the last *N* days (default: 90 days).

---

### 2. `percentiles.py` – Analysis Tool

Reads invoice data and computes percentile values using multiple modes.

#### 🎯 Input:
- Invoice CSV file
- Desired percentile (e.g., 75 for 75th percentile)

#### 🧠 Modes:
- **Mode 1: Weekly Percentiles**
  - Groups invoices by week and computes the given percentile per week.

- **Mode 2: Tag-Based Percentiles**
  - Computes the percentile for each individual tag (e.g., `"cash"`, `"upi"`).

- **Mode 3: OR-Tag Match**
  - Filters invoices containing **any** of the given tags.
  - Computes the percentile over this filtered subset.

- **Mode 4: AND-Tag Match (Strict)**
  - Filters invoices containing **all** specified tags.
  - Computes the percentile over this subset.
  - Stricter than Mode 3 (requires exact match).

---
