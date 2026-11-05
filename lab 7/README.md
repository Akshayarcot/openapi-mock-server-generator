# L6_L7_41 — Laundry Service

**Lab 7: Fuzzing for Input Validation Bugs**  
**Student Name:** A R AKSHAY KUMAR  
**SRN:** PES1UG24CS705  
**Course:** Software Engineering & Test Automation (SE / SETA)

---

## Overview

This lab demonstrates **dynamic fuzz testing** using the **Hypothesis** property-based testing framework to automatically uncover hidden input validation bugs, crashes, and unhandled edge cases in the laundry service processing module, followed by defensive programming to harden the implementation.

---

## Files & Deliverables

| File | Description |
|------|-------------|
| `laundry_service.py` / `processor.py` | Defensively hardened application script |
| `test_laundry_service.py` / `test_processor.py` | Hypothesis fuzz test suite |
| `PES1UG24CS705_Lab7.pdf` | Comprehensive lab report with screenshots & analysis |
| `screenshot_step2_buggy_run.png` | Step 2: Execution of initial script |
| `screenshot_step4_tests_failing.png` | Step 4: Fuzz testing exposing exceptions |
| `screenshot_step5_fixed_run.png` | Step 5: Execution of hardened script |
| `screenshot_step6_tests_passing.png` | Step 6: 100% tests passing under fuzzing |

---

## Running the Tests

1. **Install dependencies:**
   ```bash
   pip install hypothesis pytest
   ```

2. **Execute the application:**
   ```bash
   python processor.py
   # or
   python laundry_service.py
   ```

3. **Run Hypothesis fuzz tests:**
   ```bash
   pytest test_processor.py
   # or
   pytest test_laundry_service.py
   ```
