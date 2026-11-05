# Lab 5: Static Code Analysis — Library Catalog System

**Student Name:** A R Akshay Kumar  
**SRN:** PES1UG24CS705  
**Course:** Software Engineering (UE22CS351A / SE Lab)  
**Assigned Repository:** [SETAPESU26/L5_41_library_catalog_system](https://github.com/SETAPESU26/L5_41_library_catalog_system)  
**Program Script:** `library_catalog_system.py`

---

## 1. Overview & Objective

The objective of this lab is to enhance Python code quality, security, and PEP 8 style adherence by utilizing three industry-standard static analysis tools:
1. **Bandit:** Application security analysis for Common Weakness Enumerations (CWEs), dangerous function calls, and error suppression.
2. **Flake8:** PEP 8 style, syntax, whitespace, and lexical analysis.
3. **Pylint:** Deep static code analysis assessing design patterns, variable lifecycle, dangerous defaults, and maintainability.

---

## 2. Deliverables Summary

| Deliverable | File Path | Status |
| :--- | :--- | :--- |
| **Cleaned & Fixed Python Script** | [`library_catalog_system.py`](library_catalog_system.py) | **Cleaned & Verified (Pylint 10.00/10)** |
| **Comprehensive Issue Tracking Table** | [`issues.md`](issues.md) | **Completed (16 issues documented & fixed)** |
| **Detailed Reflection Report** | [`reflection.md`](reflection.md) | **Completed (All 4 reflection questions answered)** |
| **Pylint Baseline Report (Before)** | [`reports/pylint_report_before.txt`](reports/pylint_report_before.txt) | Rating: **5.32 / 10** |
| **Pylint Verification Report (After)** | [`reports/pylint_report_after.txt`](reports/pylint_report_after.txt) | Rating: **10.00 / 10** |
| **Bandit Baseline Report (Before)** | [`reports/bandit_report_before.txt`](reports/bandit_report_before.txt) | **5 Issues** (2 High, 1 Medium, 2 Low) |
| **Bandit Verification Report (After)** | [`reports/bandit_report_after.txt`](reports/bandit_report_after.txt) | **0 Issues Identified** |
| **Flake8 Baseline Report (Before)** | [`reports/flake8_report_before.txt`](reports/flake8_report_before.txt) | **6 Violations** |
| **Flake8 Verification Report (After)** | [`reports/flake8_report_after.txt`](reports/flake8_report_after.txt) | **0 Violations (Clean)** |

---

## 3. Metrics Comparison (Before vs. After)

| Metric | Baseline (Initial Code) | Final (Remediated Code) | Improvement |
| :--- | :--- | :--- | :--- |
| **Bandit Security Issues** | 5 (2 High, 1 Med, 2 Low) | **0 Issues** | 100% elimination of security flaws |
| **Flake8 PEP 8 Violations** | 6 violations | **0 violations** | 100% PEP 8 compliant |
| **Pylint Quality Score** | **5.32 / 10** | **10.00 / 10** | **+4.68 (+88.0% improvement)** |

---

## 4. Key Fixes Implemented

1. **Eliminated Shell Command Injection (Bandit B605 / CWE-78):** Replaced dangerous `os.system("echo ... " + filename)` with Python native formatted `print()` output.
2. **Replaced Dangerous `eval()` with Safe AST Evaluator (Bandit B307 / Pylint W0123 / CWE-78):** Implemented `safe_eval_expr()` using Python's `ast` parser with strict arithmetic operator whitelisting (`+`, `-`, `*`, `/`).
3. **Upgraded Cryptographic Hashing to SHA-256 (Bandit B324 / CWE-327):** Replaced broken MD5 hashing with SHA-256 for patron identification.
4. **Replaced Insecure PRNG with CSPRNG (Bandit B311 / CWE-330):** Used Python standard `secrets.SystemRandom().randint(1000, 9999)` for temporary PIN generation.
5. **Fixed Bare `except: pass` Error Masking (Bandit B110 / Flake8 E722 / Pylint W0702):** Replaced blind exception suppression with explicit containment checks (`if book_id in CATALOG:`).
6. **Eliminated Dangerous Mutable Default Argument (Pylint W0102):** Replaced `active_issues=[]` with `Optional[List[str]] = None` and initialized safely inside the function body.
7. **Cleaned Unused Imports & Variables (Flake8 F401, F841):** Removed unused `import csv`, unused variable `late_fee`, and properly structured variable scoping.
8. **Resource Safety & Encoding (Pylint W1514, R1732):** Wrapped file writes in `with open(..., encoding="utf-8")` context manager.
9. **PEP 8 Naming, Spacing, and Docstrings (Pylint C0103, C0116, Flake8 W292):** Renamed functions to `snake_case`, added comprehensive PEP 257 docstrings, and resolved all line length and newline requirements.
10. **Module Execution Protection:** Enclosed script entrypoint in standard `if __name__ == "__main__": main()`.

---

## 5. Verification Commands

To verify all reports and execute the cleaned script:

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run the cleaned script
python library_catalog_system.py

# 3. Verify Flake8 (zero output = zero errors)
flake8 library_catalog_system.py

# 4. Verify Bandit (zero security issues)
bandit -r library_catalog_system.py

# 5. Verify Pylint (score 10.00/10)
pylint library_catalog_system.py
```
