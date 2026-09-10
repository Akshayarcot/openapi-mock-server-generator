#!/usr/bin/env python3
"""
Software Engineering Lab 3: Component Modelling & Architectural Pattern Selection
System: Self-Service Coffee Kiosk System
Architecture: 3-Tier Layered Architecture (Presentation, Business, Data)

This script demonstrates the component interactions and interface boundaries
as modeled in the UML Component Diagram.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import sqlite3
import sys
from typing import Dict, List, Optional, Tuple


# =====================================================================
# DATA DEFINITIONS & ENUMS
# =====================================================================

class CoffeeType(str, Enum):
    ESPRESSO = "Espresso"
    AMERICANO = "Americano"
    LATTE = "Latte"


class DrinkSize(str, Enum):
    SMALL = "Small"
    LARGE = "Large"


@dataclass
class MenuItem:
    coffee_type: CoffeeType
    base_price: float
    description: str


@dataclass
class OrderItem:
    coffee_type: CoffeeType
    size: DrinkSize
    price: float


@dataclass
class Order:
    order_id: str
    items: List[OrderItem] = field(default_factory=list)
    total_amount: float = 0.0
    status: str = "CREATED"
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    payment_reference: Optional[str] = None


# =====================================================================
# 1. DATA LAYER: Database Component
# =====================================================================

class IDatabaseInterface:
    """Provided interface by Database Component (SQL / Data Query Interface)."""
    def get_menu(self) -> Dict[CoffeeType, MenuItem]:
        raise NotImplementedError

    def get_size_multiplier(self, size: DrinkSize) -> float:
        raise NotImplementedError

    def save_order(self, order: Order) -> bool:
        raise NotImplementedError


class DatabaseComponent(IDatabaseInterface):
    """
    «component» Database Component
    Data Layer: Stores menu items, size multiplier pricing rules, and order audit records.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                coffee_type TEXT PRIMARY KEY,
                base_price REAL,
                description TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS size_multipliers (
                size TEXT PRIMARY KEY,
                multiplier REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                items_json TEXT,
                total_amount REAL,
                status TEXT,
                timestamp TEXT,
                payment_ref TEXT
            )
        """)
        self.conn.commit()
        self._seed_data()

    def _seed_data(self):
        cursor = self.conn.cursor()
        menu_data = [
            (CoffeeType.ESPRESSO.value, 3.00, "Rich, concentrated shot of espresso"),
            (CoffeeType.AMERICANO.value, 3.75, "Espresso diluted with hot water"),
            (CoffeeType.LATTE.value, 4.50, "Espresso with steamed milk and light foam"),
        ]
        cursor.executemany(
            "INSERT OR REPLACE INTO menu (coffee_type, base_price, description) VALUES (?, ?, ?)",
            menu_data
        )

        size_data = [
            (DrinkSize.SMALL.value, 1.0),
            (DrinkSize.LARGE.value, 1.4),  # Large is 40% more
        ]
        cursor.executemany(
            "INSERT OR REPLACE INTO size_multipliers (size, multiplier) VALUES (?, ?)",
            size_data
        )
        self.conn.commit()

    def get_menu(self) -> Dict[CoffeeType, MenuItem]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT coffee_type, base_price, description FROM menu")
        results = {}
        for row in cursor.fetchall():
            c_type = CoffeeType(row[0])
            results[c_type] = MenuItem(coffee_type=c_type, base_price=row[1], description=row[2])
        return results

    def get_size_multiplier(self, size: DrinkSize) -> float:
        cursor = self.conn.cursor()
        cursor.execute("SELECT multiplier FROM size_multipliers WHERE size = ?", (size.value,))
        row = cursor.fetchone()
        return row[0] if row else 1.0

    def save_order(self, order: Order) -> bool:
        cursor = self.conn.cursor()
        items_payload = json.dumps([
            {"coffee_type": i.coffee_type.value, "size": i.size.value, "price": i.price}
            for i in order.items
        ])
        cursor.execute("""
            INSERT OR REPLACE INTO orders (order_id, items_json, total_amount, status, timestamp, payment_ref)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order.order_id, items_payload, order.total_amount, order.status, order.timestamp, order.payment_reference))
        self.conn.commit()
        return True


# =====================================================================
# 2. BUSINESS LAYER: Payment Service Component
# =====================================================================

class IPaymentInterface:
    """Provided interface by Payment Service Component (PCI-DSS Card Processing API)."""
    def process_payment(self, order_id: str, amount: float, card_number: str, expiry: str, cvv: str) -> Tuple[bool, str]:
        raise NotImplementedError


class PaymentServiceComponent(IPaymentInterface):
    """
    «component» Payment Service Component
    Business Layer: Isolated component for secure credit-card authorization.
    Accepts ONLY credit card payments per scenario constraints.
    """

    def process_payment(self, order_id: str, amount: float, card_number: str, expiry: str, cvv: str) -> Tuple[bool, str]:
        clean_num = card_number.replace(" ", "").replace("-", "")
        if not clean_num.isdigit() or len(clean_num) not in (15, 16):
            return False, "Payment Rejected: Invalid credit card number."
        
        if not (len(cvv) in (3, 4) and cvv.isdigit()):
            return False, "Payment Rejected: Invalid CVV security code."

        masked_card = f"****-****-****-{clean_num[-4:]}"
        auth_code = f"AUTH-{datetime.now().strftime('%H%M%S')}-{clean_num[-4:]}"
        return True, auth_code


# =====================================================================
# 3. BUSINESS LAYER: Receipt Printer Component
# =====================================================================

class IReceiptInterface:
    """Provided interface by Receipt Printer Component (Hardware Printing Driver)."""
    def print_receipt(self, order: Order, masked_card: str, auth_code: str) -> str:
        raise NotImplementedError


class ReceiptPrinterComponent(IReceiptInterface):
    """
    «component» Receipt Printer Component
    Business Layer: Hardware abstraction driver to format and send ESC/POS print jobs.
    """

    def print_receipt(self, order: Order, masked_card: str, auth_code: str) -> str:
        receipt_lines = [
            "==========================================",
            "          CAFE CENTRAL KIOSK              ",
            "       SELF-SERVICE ORDER RECEIPT         ",
            "==========================================",
            f" Order Number : #{order.order_id}",
            f" Date & Time  : {order.timestamp}",
            "------------------------------------------",
            f" {'ITEM':<20} {'SIZE':<8} {'PRICE ($)':>10}",
            "------------------------------------------",
        ]
        for item in order.items:
            receipt_lines.append(
                f" {item.coffee_type.value:<20} {item.size.value:<8} {item.price:>10.2f}"
            )
        receipt_lines.extend([
            "------------------------------------------",
            f" {'TOTAL AMOUNT:':<29} ${order.total_amount:>8.2f}",
            "==========================================",
            " PAYMENT METHOD: Credit Card Only",
            f" Card Number   : {masked_card}",
            f" Auth Code     : {auth_code}",
            f" Payment Status: SUCCESS / PAID",
            "==========================================",
            "       Thank you for your order!          ",
            "       Please collect at counter.         ",
            "==========================================\n",
        ])
        receipt_text = "\n".join(receipt_lines)
        return receipt_text


# =====================================================================
# 4. BUSINESS LAYER: Order Manager Component
# =====================================================================

class IOrderInterface:
    """Provided interface by Order Manager Component (GUI Events / Kiosk IPC)."""
    def get_available_menu(self) -> Dict[CoffeeType, MenuItem]:
        raise NotImplementedError

    def calculate_price(self, coffee_type: CoffeeType, size: DrinkSize) -> float:
        raise NotImplementedError

    def create_order(self, coffee_type: CoffeeType, size: DrinkSize) -> Order:
        raise NotImplementedError

    def submit_payment_and_complete(self, order: Order, card_number: str, expiry: str, cvv: str) -> Tuple[bool, str, Optional[str]]:
        raise NotImplementedError


class OrderManagerComponent(IOrderInterface):
    """
    «component» Order Manager Component
    Business Layer: Core coordinator managing business rules, pricing, order state,
    and delegating to Payment, Printer, and Database components.
    """

    def __init__(
        self,
        db_component: IDatabaseInterface,
        payment_component: IPaymentInterface,
        printer_component: IReceiptInterface,
    ):
        self.db = db_component
        self.payment_service = payment_component
        self.printer = printer_component
        self._order_seq = 100

    def get_available_menu(self) -> Dict[CoffeeType, MenuItem]:
        return self.db.get_menu()

    def calculate_price(self, coffee_type: CoffeeType, size: DrinkSize) -> float:
        menu = self.db.get_menu()
        if coffee_type not in menu:
            raise ValueError(f"Unknown coffee type: {coffee_type}")
        base = menu[coffee_type].base_price
        multiplier = self.db.get_size_multiplier(size)
        return round(base * multiplier, 2)

    def create_order(self, coffee_type: CoffeeType, size: DrinkSize) -> Order:
        self._order_seq += 1
        order_id = f"K{self._order_seq:04d}"
        price = self.calculate_price(coffee_type, size)
        item = OrderItem(coffee_type=coffee_type, size=size, price=price)
        order = Order(order_id=order_id, items=[item], total_amount=price, status="PENDING_PAYMENT")
        return order

    def submit_payment_and_complete(
        self, order: Order, card_number: str, expiry: str, cvv: str
    ) -> Tuple[bool, str, Optional[str]]:
        success, auth_msg = self.payment_service.process_payment(
            order_id=order.order_id,
            amount=order.total_amount,
            card_number=card_number,
            expiry=expiry,
            cvv=cvv
        )

        if not success:
            order.status = "PAYMENT_FAILED"
            self.db.save_order(order)
            return False, auth_msg, None

        order.status = "COMPLETED"
        order.payment_reference = auth_msg
        self.db.save_order(order)

        masked_card = f"****-****-****-{card_number.replace(' ', '')[-4:]}"
        receipt_output = self.printer.print_receipt(order, masked_card=masked_card, auth_code=auth_msg)

        return True, f"Order #{order.order_id} completed successfully!", receipt_output


# =====================================================================
# 5. PRESENTATION LAYER: User Interface Component
# =====================================================================

class UserInterfaceComponent:
    """
    «component» User Interface Component
    Presentation Layer: Handles touch screen interactions, presents coffee selection,
    drink size buttons, captures credit card input, and displays receipt previews.
    """

    def __init__(self, order_manager: IOrderInterface):
        self.order_manager = order_manager

    def display_touchscreen_menu(self):
        menu = self.order_manager.get_available_menu()
        print("\n" + "=" * 55)
        print("  ☕  WELCOME TO CAFE CENTRAL SELF-SERVICE KIOSK  ☕")
        print("=" * 55)
        print(" Available Beverages:")
        for idx, (c_type, item) in enumerate(menu.items(), start=1):
            s_price = self.order_manager.calculate_price(c_type, DrinkSize.SMALL)
            l_price = self.order_manager.calculate_price(c_type, DrinkSize.LARGE)
            print(f"  [{idx}] {c_type.value:<10} - {item.description}")
            print(f"      Small: ${s_price:.2f}  |  Large: ${l_price:.2f}")
        print("=" * 55)

    def simulate_user_ordering(
        self,
        coffee_type: CoffeeType,
        size: DrinkSize,
        card_number: str,
        expiry: str,
        cvv: str
    ) -> Tuple[bool, str, Optional[str]]:
        print(f"\n[Touch Interaction] User selected: {coffee_type.value} ({size.value})")
        order = self.order_manager.create_order(coffee_type, size)
        print(f"[Touch Screen] Order created #{order.order_id} | Total: ${order.total_amount:.2f}")
        print(f"[Touch Screen] Entering Payment Details (Card: **** {card_number[-4:]})")
        
        success, msg, receipt = self.order_manager.submit_payment_and_complete(
            order, card_number, expiry, cvv
        )
        return success, msg, receipt


def main():
    print("=" * 60)
    print("Lab 3: Architectural Pattern Selection & Component Modelling")
    print("System: Self-Service Coffee Kiosk System")
    print("Architecture: 3-Tier Layered Architecture")
    print("=" * 60)

    db = DatabaseComponent()
    payment_service = PaymentServiceComponent()
    receipt_printer = ReceiptPrinterComponent()
    order_manager = OrderManagerComponent(
        db_component=db,
        payment_component=payment_service,
        printer_component=receipt_printer
    )
    ui = UserInterfaceComponent(order_manager=order_manager)

    ui.display_touchscreen_menu()

    # Scenario Test 1: Order Americano (Large)
    print("\n--- TEST CASE 1: Valid Order (Americano Large) ---")
    success, msg, receipt = ui.simulate_user_ordering(
        coffee_type=CoffeeType.AMERICANO,
        size=DrinkSize.LARGE,
        card_number="4111-2222-3333-4444",
        expiry="12/28",
        cvv="123"
    )
    print(f"Result: {msg}")
    if receipt:
        print("\n[Receipt Printer Hardware Output]:")
        print(receipt)

    # Scenario Test 2: Order Latte (Small)
    print("\n--- TEST CASE 2: Valid Order (Latte Small) ---")
    success, msg, receipt = ui.simulate_user_ordering(
        coffee_type=CoffeeType.LATTE,
        size=DrinkSize.SMALL,
        card_number="5500-0000-0000-9876",
        expiry="08/29",
        cvv="456"
    )
    print(f"Result: {msg}")
    if receipt:
        print("\n[Receipt Printer Hardware Output]:")
        print(receipt)

    # Scenario Test 3: Invalid Card Failure Test
    print("\n--- TEST CASE 3: Payment Failure Handling ---")
    success, msg, receipt = ui.simulate_user_ordering(
        coffee_type=CoffeeType.ESPRESSO,
        size=DrinkSize.SMALL,
        card_number="123",
        expiry="01/25",
        cvv="00"
    )
    print(f"Result: {msg}")
    assert not success, "Should fail on invalid credit card"

    print("\nAll 3 test scenarios completed successfully!")


if __name__ == "__main__":
    main()
