# 🛡️ Semwal Bespoke Fabrics — Production Audit & Operations Guide

**System Health Status**: `PRODUCTION READY` ✅  
**Audit Timestamp**: August 10, 2026

---

## 📊 1. Deep Production Audit Results

| Metric / Audit Check | Status | Details |
|---|---|---|
| **Git Repository** | Clean ✅ | `main` branch fully in sync with `origin/main` |
| **Active Fabrics** | 262 | All active images present in `images/` folder |
| **Archived (Out of Stock)** | 51 | Safely preserved in `archive/out-of-stock/` |
| **Low-Stock Items (<5m)** | 26 | Displaying visual Low Stock progress bar on website |
| **Data Synchronization** | 100% | Zero discrepancy between `catalog-data.json` & `fabric-tags.json` |
| **Data Leakage Check** | 0 Leaks | Zero active fabrics exist in the archive directory |
| **PDF Catalog** | 25 MB | `semwal-bespoke-fabrics-catalog.pdf` verified & current |
| **Website Filters** | Active | Series, Pattern, Color, Style & **Less Than 5 Mtrs** filter live |

---

## ⚡ 2. One-Command Automation (`deploy.sh`)

You no longer need to execute manual terminal steps or handle multiple scripts. Use **`./deploy.sh`** for all catalog operations:

### 🔹 Mark Fabrics Out of Stock
Automates moving image to `archive/out-of-stock/`, clearing meters tag, regenerating catalog + PDF, and pushing to GitHub.
```bash
./deploy.sh PI-531
./deploy.sh I-440 I-306 I-256
```

### 🔹 Restore Archived Fabrics
Automates moving image back to `images/`, regenerating catalog + PDF, and pushing to GitHub.
```bash
./deploy.sh restore I-440
```

### 🔹 Set Remaining Meters (Low Stock Bar)
```bash
./deploy.sh meters I-217 4
```

### 🔹 General Catalog Update & Push
```bash
./deploy.sh
```

---

## ⚙️ 3. CI/CD Pipeline Overview (`.github/workflows/catalog-ci.yml`)

A full **GitHub Actions** CI/CD pipeline has been added to the repository:
1. Triggers on every push to `main`.
2. Sets up Python 3.11 environment with `reportlab` & `Pillow`.
3. Runs `analyze_fabric_tags.py`, `generate_catalog.py`, and `generate_pdf_catalog.py`.
4. Verifies catalog integrity and builds the PDF in the cloud to guarantee no broken builds reach production.

---

## 📋 4. Catalog Architecture Overview

```
images/ & archive/out-of-stock/ ──> analyze_fabric_tags.py ──> fabric-tags.json
                                                                    │
semwal-bespoke-fabrics-catalog.pdf <── generate_pdf_catalog.py <── generate_catalog.py
                                                                    │
                                                                    ▼
                                                            catalog-data.json
                                                                    │
                                                                    ▼
                                                          index.html (Website)
```
