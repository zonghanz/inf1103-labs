"""Lab 9 automated tests: Strategy, Factory, validation and exception handling.

Run from the project folder (no extra packages needed, so it also runs in Docker / CI):
    python -m unittest discover -s tests -v
"""
import csv
import inspect
import io
import math
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from bulkdiscount import BulkDiscount
from digitalproduct import DigitalProduct
from discountstrategy import DiscountStrategy
from inventory import Inventory
from nodiscount import NoDiscount
from order import Order
from orderline import OrderLine
from percentagediscount import PercentageDiscount
from physicalproduct import PhysicalProduct
from product import Product
from productfactory import ProductFactory
from studentdiscount import StudentDiscount
from supplier import Supplier

SAMPLE_CSV = [
    ["product_type", "product_id", "name", "price", "stock_quantity"],
    ["physical", "P001", "Desk Lamp", "25.00", "10"],
    ["digital", "D001", "Photo Editor", "49.90", "100"],
    ["service", "S001", "Installation", "30.00", "5"],
    ["physical", "P002", "Office Chair", "abc", "3"],
    ["physical", "P003", "Monitor Stand", "39.50", "7"],
]


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")


def order_totalling_250() -> Order:
    # Two lines that add up to 250: 2 x 100 + 1 x 50
    supplier = make_supplier()
    order = Order("O001")
    order.add_order_line(ProductFactory.create("physical", "P001", "Desk", 100.0, 5, supplier), 2)
    order.add_order_line(ProductFactory.create("digital", "D001", "Editor", 50.0, 5, supplier), 1)
    return order


# ------------------------------------------------------------------ Section 2: Strategy
class TestDiscountStrategies(unittest.TestCase):

    def test_discount_strategy_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_every_strategy_is_a_discount_strategy(self) -> None:
        for strategy in (NoDiscount(), PercentageDiscount(10), BulkDiscount(200, 20),
                         StudentDiscount()):
            self.assertIsInstance(strategy, DiscountStrategy)

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount(self) -> None:
        self.assertTrue(math.isclose(PercentageDiscount(10).apply(250.0), 225.0))

    def test_bulk_discount_at_and_below_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250.0), 230.0)
        self.assertEqual(bulk.apply(200.0), 180.0)    # "200 or more" includes 200
        self.assertEqual(bulk.apply(199.99), 199.99)

    def test_student_discount_is_five_percent(self) -> None:
        self.assertTrue(math.isclose(StudentDiscount().apply(200.0), 190.0))


class TestOrderUsesStrategy(unittest.TestCase):

    def test_order_defaults_to_no_discount(self) -> None:
        order = order_totalling_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_predict_first_bulk_then_percentage(self) -> None:
        # Section 2.3 predict first: 250 -> 230 with BulkDiscount(200, 20) -> 225 with 10% off
        order = order_totalling_250()
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertTrue(math.isclose(order.calculate_total(), 225.0))

    def test_strategy_can_be_given_when_order_is_created(self) -> None:
        order = Order("O002", BulkDiscount(200, 20))
        self.assertIsInstance(order.discount, BulkDiscount)

    def test_new_strategy_added_without_changing_order(self) -> None:
        # StudentDiscount was added after Order was written; Order still works with it.
        order = order_totalling_250()
        order.set_discount(StudentDiscount())
        self.assertTrue(math.isclose(order.calculate_total(), 237.5))

    def test_order_has_no_discount_if_elif_logic(self) -> None:
        lines = inspect.getsource(Order.calculate_total).splitlines()
        source = "\n".join(line for line in lines if not line.strip().startswith("#"))
        self.assertIn(".apply(", source)
        for word in ("if ", "elif", "isinstance", "Percentage", "Bulk", "Student"):
            self.assertNotIn(word, source)

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        order_a, order_b = order_totalling_250(), order_totalling_250()
        order_a.set_discount(shared)
        order_b.set_discount(shared)
        self.assertIs(order_a.discount, order_b.discount)    # association, not composition


# ------------------------------------------------------------------ Section 3: Factory
class TestProductFactory(unittest.TestCase):

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.0, 10,
                                        make_supplier(), weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.weight, 1.5)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.9, 100,
                                        make_supplier(), download_size=450.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 450.0)

    def test_unknown_type_raises_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, make_supplier())
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_main_creates_products_through_factory(self) -> None:
        # main.py no longer imports or calls the concrete product classes.
        source = inspect.getsource(main)
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)
        item = {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15,
                "supplier_id": "S001", "type": "physical", "weight": 2.1}
        with patch.object(ProductFactory, "create", wraps=ProductFactory.create) as spy:
            product = main.product_from_dict(item, {"S001": make_supplier()})
        spy.assert_called_once()
        self.assertIsInstance(product, PhysicalProduct)


# ------------------------------------------------------------------ Section 4: Validation
class TestValidation(unittest.TestCase):

    def test_price_must_be_greater_than_zero(self) -> None:
        for price in (0, -5.0):
            with self.assertRaises(ValueError) as context:
                ProductFactory.create("physical", "P001", "Desk", price, 1, make_supplier())
            self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("digital", "D001", "Editor", 10.0, -1, make_supplier())
        self.assertEqual(str(context.exception), "Stock cannot be negative.")

    def test_zero_stock_is_allowed(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk", 10.0, 0, make_supplier())
        self.assertEqual(product.stock, 0)

    def test_both_subclasses_keep_the_product_rules(self) -> None:
        # LSP: neither subclass skips the validation that Product defines.
        for product_type in ("physical", "digital"):
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "X1", "Item", -1.0, 1, make_supplier())
            product = ProductFactory.create(product_type, "X1", "Item", 1.0, 1, make_supplier())
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk", 10.0, 5, make_supplier())
        for quantity in (0, -3):
            with self.assertRaises(ValueError) as context:
                OrderLine(product, quantity)
            self.assertEqual(str(context.exception), "Quantity must be greater than zero.")


# ------------------------------------------------------------------ Section 5.1: User input
class TestGetPositiveFloat(unittest.TestCase):

    def test_keeps_asking_until_valid(self) -> None:
        # Section 5.1 predict first: abc, then -5, then 12.50
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = main.get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_rejected(self) -> None:
        with patch("builtins.input", side_effect=["0", "3"]), redirect_stdout(io.StringIO()):
            self.assertEqual(main.get_positive_float("Price: "), 3.0)

    def test_get_non_negative_int_keeps_asking(self) -> None:
        with patch("builtins.input", side_effect=["x", "-1", "2.5", "0"]), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(main.get_non_negative_int("Stock: "), 0)


# ------------------------------------------------------------------ Section 5.2: Loading a file
class TestLoadProducts(unittest.TestCase):

    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")
        with open(self.path, "w", newline="") as file:
            csv.writer(file).writerows(SAMPLE_CSV)

    def tearDown(self) -> None:
        self.folder.cleanup()

    def run_load(self, path: str, inventory: Inventory) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            main.load_products(path, inventory, make_supplier())
        return output.getvalue().splitlines()

    def test_bad_rows_are_skipped_and_valid_rows_load(self) -> None:
        inventory = Inventory()
        lines = self.run_load(self.path, inventory)
        self.assertEqual([p.product_id for p in inventory.products], ["P001", "D001", "P003"])
        self.assertTrue(lines[0].startswith("Skipped line 4"))
        self.assertIn("Unknown product type: service", lines[0])
        self.assertTrue(lines[1].startswith("Skipped line 5"))
        self.assertIn("could not convert string to float: 'abc'", lines[1])
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_loaded_products_are_the_right_types(self) -> None:
        inventory = Inventory()
        self.run_load(self.path, inventory)
        self.assertIsInstance(inventory.find_product("P001"), PhysicalProduct)
        self.assertIsInstance(inventory.find_product("D001"), DigitalProduct)

    def test_missing_file_is_handled_gracefully(self) -> None:
        inventory = Inventory()
        missing = os.path.join(self.folder.name, "missing.csv")
        lines = self.run_load(missing, inventory)   # must not raise
        self.assertEqual(lines, [f"Products file not found: {missing}",
                                 "Load attempt finished."])
        self.assertEqual(inventory.products, [])

    def test_duplicate_ids_are_reported_not_added_twice(self) -> None:
        inventory = Inventory()
        self.run_load(self.path, inventory)
        lines = self.run_load(self.path, inventory)
        self.assertIn("0 products loaded.", lines)
        self.assertEqual(len(inventory.products), 3)


# ------------------------------------------------------------------ Review: specific excepts
class TestSpecificExceptions(unittest.TestCase):

    def test_no_bare_or_broad_except_in_source(self) -> None:
        folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".py"):
                with open(os.path.join(folder, filename)) as file:
                    source = file.read()
                self.assertNotIn("except:", source, filename)
                self.assertNotIn("except Exception", source, filename)


if __name__ == "__main__":
    unittest.main()
