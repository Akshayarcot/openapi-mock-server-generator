import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status

"""
Test suite designed for comprehensive Branch Coverage analysis.
Tests every decision path, logical branch (both True and False outcomes),
compound conditional combination, and boundary/edge case in laundry_service.py
to achieve 100% Branch Coverage and 100% Line Coverage.
"""

# ============================================================================
# 1. extra_weight_charge Branch and Edge Case Tests
# ============================================================================

def test_extra_weight_unknown_garment():
    """Branch: garment_type not in INCLUDED_KG evaluates to True."""
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("leather", 10, "standard", False)


def test_extra_weight_negative_weight():
    """Branch: weight_kg < 0 evaluates to True."""
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_extra_weight_member_non_bedding():
    """Branch: is_member True AND garment_type != 'bedding' -> True (adds 2kg)."""
    # regular included: 5 + 2 = 7; weight: 7 -> extra = 0
    assert extra_weight_charge("regular", 7, "standard", True) == 0


def test_extra_weight_member_bedding():
    """Branch: is_member True AND garment_type == 'bedding' -> False (no +2kg)."""
    # bedding included: 8 (remains 8); weight: 8 -> extra = 0
    assert extra_weight_charge("bedding", 8, "standard", True) == 0


def test_extra_weight_non_member():
    """Branch: is_member False -> condition evaluates to False."""
    # delicate included: 3; weight: 3 -> extra = 0
    assert extra_weight_charge("delicate", 3, "standard", False) == 0


def test_extra_weight_extra_zero():
    """Branch: extra <= 0 evaluates to True (boundary: weight equals included)."""
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_extra_weight_extra_negative():
    """Branch: extra <= 0 evaluates to True (weight strictly less than included)."""
    assert extra_weight_charge("regular", 2, "standard", False) == 0


def test_extra_weight_extra_positive_standard_speed_no_extra_surcharge():
    """Branch: speed == 'standard' True, extra <= 10 False for surcharge."""
    # regular included: 5; weight: 9 -> extra: 4 (<= 10); rate: 30
    assert extra_weight_charge("regular", 9, "standard", False) == 4 * 30


def test_extra_weight_extra_positive_non_standard_no_extra_surcharge():
    """Branch: speed == 'standard' False (else rate=50), extra <= 10 (no surcharge)."""
    # delicate included: 3; weight: 8 -> extra: 5 (<= 10); rate: 50
    assert extra_weight_charge("delicate", 8, "economy", False) == 5 * 50


def test_extra_weight_surcharge_standard_speed():
    """Branch: extra > 10 True, speed == 'express' False."""
    # regular included: 5; weight: 18 -> extra: 13 (> 10); rate: 30 + 15 = 45
    assert extra_weight_charge("regular", 18, "standard", False) == 13 * 45


def test_extra_weight_surcharge_express_speed():
    """Branch: extra > 10 True, speed == 'express' True."""
    # bedding included: 8; weight: 20 -> extra: 12 (> 10); rate: 50 + 15 + 10 = 75
    assert extra_weight_charge("bedding", 20, "express", False) == 12 * 75


# ============================================================================
# 2. order_acceptable Branch and Edge Case Tests
# ============================================================================

def test_order_acceptable_delicate_within_limit():
    """Branch: is_delicate True, items <= 5 True (boundary items = 5)."""
    assert order_acceptable(10, 5, True) is True


def test_order_acceptable_delicate_exceeds_limit():
    """Branch: is_delicate True, items <= 5 False (items = 6)."""
    assert order_acceptable(10, 6, True) is False


def test_order_acceptable_non_delicate_weight_over_25():
    """Branch: is_delicate False, weight_kg > 25 True."""
    assert order_acceptable(26, 10, False) is False


def test_order_acceptable_non_delicate_weight_boundary():
    """Branch: is_delicate False, weight_kg > 25 False (boundary weight = 25)."""
    assert order_acceptable(25, 40, False) is True


def test_order_acceptable_non_delicate_items_within_limit():
    """Branch: is_delicate False, weight_kg <= 25, items <= 40 True."""
    assert order_acceptable(15, 20, False) is True


def test_order_acceptable_non_delicate_items_exceed_limit():
    """Branch: is_delicate False, weight_kg <= 25, items <= 40 False (items = 41)."""
    assert order_acceptable(15, 41, False) is False


# ============================================================================
# 3. dropoff_status Branch, Edge Case, and Boundary Tests
# ============================================================================

def test_dropoff_has_bedding_is_express_accepted():
    """Branches: has_bedding True (cutoff 90), is_express True (+30 -> 120), >= cutoff."""
    assert dropoff_status(120, True, True) == "accepted"


def test_dropoff_has_bedding_not_express_late():
    """Branches: has_bedding True (90), is_express False (90), late window [70, 89]."""
    assert dropoff_status(75, True, False) == "late"


def test_dropoff_has_bedding_rejected():
    """Branches: has_bedding True (90), is_express False (90), rejected (< 70)."""
    assert dropoff_status(69, True, False) == "rejected"


def test_dropoff_no_bedding_is_express_accepted():
    """Branches: has_bedding False (60), is_express True (+30 -> 90), >= cutoff."""
    assert dropoff_status(95, False, True) == "accepted"


def test_dropoff_no_bedding_not_express_accepted():
    """Branches: has_bedding False (60), is_express False (60), >= 60."""
    assert dropoff_status(60, False, False) == "accepted"


def test_dropoff_no_bedding_late_exact_boundary():
    """Branches: cutoff=60, minutes = cutoff - 20 = 40 (exact late lower bound)."""
    assert dropoff_status(40, False, False) == "late"


def test_dropoff_no_bedding_rejected_boundary():
    """Branches: cutoff=60, minutes = cutoff - 21 = 39 (just below late window)."""
    assert dropoff_status(39, False, False) == "rejected"
