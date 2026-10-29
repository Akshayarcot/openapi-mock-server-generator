import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status

"""
Test suite designed for Code (Statement/Line) Coverage analysis.
Executes every executable line in laundry_service.py to achieve 100% line coverage.
"""

# --- Tests for extra_weight_charge ---

def test_extra_weight_charge_unknown_garment():
    """Test unknown garment type raises ValueError (line 6)."""
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("leather", 10, "standard", False)


def test_extra_weight_charge_invalid_weight():
    """Test negative weight raises ValueError (line 8)."""
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -5, "standard", False)


def test_extra_weight_charge_within_included_weight():
    """Test weight within included allowance returns 0 (line 14)."""
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_extra_weight_charge_member_standard_speed():
    """Test member discount allowance and standard speed rate (lines 11, 16)."""
    # regular included is 5; member adds 2 -> 7 kg included.
    # weight 9 -> extra = 2 kg; standard speed rate = 30 -> 60
    assert extra_weight_charge("regular", 9, "standard", True) == 60


def test_extra_weight_charge_express_over_10kg_extra():
    """Test express speed and extra weight > 10 kg surcharge (lines 18, 20, 22, 23)."""
    # regular included is 5; weight 20 -> extra = 15 kg.
    # non-standard rate = 50; extra > 10 adds 15 -> 65; express adds 10 -> 75.
    # 15 * 75 = 1125
    assert extra_weight_charge("regular", 20, "express", False) == 1125


# --- Tests for order_acceptable ---

def test_order_acceptable_delicate_valid():
    """Test delicate order with items <= 5 (line 28)."""
    assert order_acceptable(10, 4, True) is True


def test_order_acceptable_overweight():
    """Test non-delicate order exceeding 25 kg limit returns False (line 30)."""
    assert order_acceptable(30, 20, False) is False


def test_order_acceptable_standard_valid():
    """Test normal order within limits returns items <= 40 (line 31)."""
    assert order_acceptable(15, 25, False) is True


# --- Tests for dropoff_status ---

def test_dropoff_status_bedding_express_accepted():
    """Test bedding + express cutoff (90+30=120) accepted (lines 36, 40, 42)."""
    assert dropoff_status(130, True, True) == "accepted"


def test_dropoff_status_non_bedding_late():
    """Test non-bedding + standard late window (lines 38, 44)."""
    # cutoff = 60; cutoff - 20 = 40; 50 is in [40, 59]
    assert dropoff_status(50, False, False) == "late"


def test_dropoff_status_rejected():
    """Test dropoff rejected when minutes before closing < cutoff - 20 (line 45)."""
    # cutoff = 60; cutoff - 20 = 40; 30 < 40 -> rejected
    assert dropoff_status(30, False, False) == "rejected"
