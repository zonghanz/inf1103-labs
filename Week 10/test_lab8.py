"""Lab 8 demonstration tests.

Run with:  python test_lab8.py
Each section prints evidence for one requirement in the brief and asserts it.
Write your 'Predict first' answers BEFORE you run the matching section.
"""
import math
from typing import get_type_hints

from supplier import Supplier
from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from inventory import Inventory
from order import Order
from orderline import OrderLine


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def make_products(supplier: Supplier) -> tuple[PhysicalProduct, DigitalProduct]:
    laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.1)
    editor = DigitalProduct("P004", "Photo Editor", 99.0, 100, supplier, 450.0)
    return laptop, editor


# Brief section 6.2: works with ANY Product, so it must work for every subclass.
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


# ---------------------------------------------------------------- Section 2
def test_association_supplier_and_product() -> None:
    heading("2. ASSOCIATION: Supplier and Product")
    # PREDICT FIRST: after `del supplier`, can each Product still show its supplier?
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop, editor = make_products(supplier)

    print("Supplier info through the PhysicalProduct:")
    laptop.display_supplier_information()
    print("\nSupplier info through the DigitalProduct:")
    editor.display_supplier_information()

    assert laptop.supplier is supplier and editor.supplier is supplier
    print("\nSupplier and products are separate objects:",
          supplier is not laptop and supplier is not editor)

    del supplier   # the variable is gone, but the products still hold a reference
    print("\nAfter `del supplier`:")
    laptop.display_supplier_information()
    editor.display_supplier_information()
    assert laptop.supplier.name == "TechSource Pte Ltd"
    assert editor.supplier.name == "TechSource Pte Ltd"
    assert laptop.supplier is editor.supplier   # one shared Supplier object

    # A Supplier can also exist with no products at all.
    lonely = Supplier("S099", "No Products Ltd", "hello@noproducts.example.com")
    lonely.display_information()
    print("PASSED: Supplier and Product are independent (association).")


# ---------------------------------------------------------------- Section 3
def test_aggregation_inventory_and_product() -> None:
    heading("3. AGGREGATION: Inventory and Product")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop, editor = make_products(supplier)       # created BEFORE any Inventory
    inventory_a, inventory_b = Inventory(), Inventory()

    inventory_a.add_product(laptop)
    inventory_a.add_product(editor)
    assert inventory_a.find_product("P001") is laptop
    print("Added both products to Inventory A.")

    # PREDICT FIRST: will the Product still work after being removed from Inventory A?
    removed = inventory_a.remove_product("P001")
    assert removed is True
    assert inventory_a.find_product("P001") is None
    print("\nRemoved P001 from Inventory A. Using the product afterwards:")
    laptop.update_stock(10)
    laptop.display_information()
    assert laptop.stock == 10

    assert inventory_b.add_product(laptop) is True
    assert inventory_b.find_product("P001") is laptop   # the SAME object
    print("\nAdded the same Laptop object to Inventory B:")
    inventory_b.display_all_products()

    # Emptying an inventory does not destroy the products.
    inventory_a.remove_product("P004")
    assert inventory_a.products == []
    editor.update_stock(5)
    assert editor.stock == 5
    print("Inventory A is empty, but the DigitalProduct still works (stock = 5).")

    assert inventory_a.remove_product("P404") is False   # not found
    assert inventory_a.find_product("P404") is None
    print("PASSED: Inventory aggregates Products (add, remove, transfer).")


# ---------------------------------------------------------------- Section 4
def test_composition_order_and_orderline() -> None:
    heading("4. COMPOSITION: Order and OrderLine")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop, editor = make_products(supplier)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(editor, 2)
    order_1.display_order()
    expected = laptop.price * 1 + editor.price * 2
    assert math.isclose(order_1.calculate_total(), expected)
    assert all(isinstance(line, OrderLine) for line in order_1.order_lines)

    # PREDICT FIRST: same Product in two Orders. How many OrderLines? How many Products?
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 3)
    order_2.display_order()

    line_1 = order_1.order_lines[0]
    line_2 = order_2.order_lines[0]
    print("\nSame Product object in both lines? ", line_1.product is line_2.product)
    print("Same OrderLine object in both orders?", line_1 is line_2)
    print(f"id(line_1)={id(line_1)}  id(line_2)={id(line_2)}")
    print(f"id(line_1.product)={id(line_1.product)}  id(line_2.product)={id(line_2.product)}")
    assert line_1.product is line_2.product
    assert line_1 is not line_2
    all_lines = order_1.order_lines + order_2.order_lines
    distinct_products = {id(line.product) for line in all_lines}
    print(f"OrderLine objects: {len(all_lines)}, Product objects: {len(distinct_products)}")
    assert len(all_lines) == 3 and len(distinct_products) == 2

    # Removing a line goes through the Order. The Product is not affected.
    assert order_1.remove_order_line("P001") is True
    assert math.isclose(order_1.calculate_total(), editor.price * 2)
    assert order_2.order_lines[0].product is laptop    # Order 2 still has its own line
    print("\nRemoved the Laptop line from Order O001; the Laptop and Order O002 are unaffected.")

    # The Order exposes only a copy of its lines, so outside code cannot add or move lines.
    order_1.order_lines.clear()
    assert len(order_1.order_lines) == 1
    # An invalid quantity is rejected by the part itself.
    try:
        order_1.add_order_line(laptop, 0)
        raise AssertionError("quantity 0 should be rejected")
    except ValueError as error:
        print(f"Rejected invalid quantity: {error}")
    print("PASSED: Order creates and manages its OrderLines; OrderLine only refers to Product.")


# ---------------------------------------------------------------- Section 5
def test_type_hints_present() -> None:
    heading("5. TYPE HINTS")
    checks = [
        (Product.__init__, "supplier", Supplier),
        (Product.__init__, "price", float),
        (Product.update_stock, "quantity", int),
        (Product.get_fulfilment_info, "return", str),
        (Inventory.add_product, "product", Product),
        (Inventory.remove_product, "product_id", str),
        (Inventory.find_product, "return", Product | None),
        (Inventory.products.fget, "return", list[Product]),
        (OrderLine.__init__, "product", Product),
        (OrderLine.__init__, "quantity", int),
        (OrderLine.calculate_subtotal, "return", float),
        (Order.add_order_line, "product", Product),
        (Order.calculate_total, "return", float),
        (Order.order_lines.fget, "return", list[OrderLine]),
        (Supplier.display_information, "return", type(None)),
        (PhysicalProduct.__init__, "supplier", Supplier),
        (DigitalProduct.__init__, "supplier", Supplier),
    ]
    for function, name, expected_type in checks:
        actual = get_type_hints(function)[name]
        print(f"{function.__qualname__:36} {name:12} -> {actual}")
        assert actual == expected_type, f"{function.__qualname__}.{name}"
    print("PASSED: type hints are present and match the UML diagram.")


# ---------------------------------------------------------------- Sections 6 and 7
def test_lsp_and_polymorphism() -> None:
    heading("6 & 7. LSP AND POLYMORPHISM")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop, editor = make_products(supplier)

    print("show_product_details() called with a PhysicalProduct:")
    show_product_details(laptop)
    print("\nshow_product_details() called with a DigitalProduct:")
    show_product_details(editor)

    # Both types live in ONE Inventory, typed as Product.
    inventory = Inventory()
    assert inventory.add_product(laptop) and inventory.add_product(editor)

    print("\nOne loop over the Product collection (no isinstance, no separate loops):")
    messages = []
    for product in inventory.products:
        product.display_information()
        message = product.get_fulfilment_info()
        print(message)
        messages.append(message)
    assert messages[0] != messages[1]               # each subclass answers differently
    assert "physical" in messages[0].lower()
    assert "digital" in messages[1].lower()

    # LSP: both subclasses keep the expectation Product sets for update_stock().
    print("\nLSP check on update_stock():")
    for product in inventory.products:
        product.update_stock(42)                    # valid input accepted
        assert product.stock == 42
        try:
            product.update_stock(-1)                # invalid input rejected as in Product
            raise AssertionError("negative stock should raise ValueError")
        except ValueError:
            assert product.stock == 42              # and the stock is left unchanged
        print(f"{type(product).__name__}: accepts 42, rejects -1, stock stays {product.stock}")
    print("PASSED: both subclasses can stand in for Product (LSP + polymorphism).")


if __name__ == "__main__":
    test_association_supplier_and_product()
    test_aggregation_inventory_and_product()
    test_composition_order_and_orderline()
    test_type_hints_present()
    test_lsp_and_polymorphism()
    print("\nALL LAB 8 CHECKS PASSED")
