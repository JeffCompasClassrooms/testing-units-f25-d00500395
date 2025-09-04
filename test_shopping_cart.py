# test_shopping_cart.py
# Unit tests for shopping_cart.py
# Program Author: AutomationPanda on GitHub
# Test Author: Ayden Wayman

import pytest
from shopping_cart import *

def test_calculate_total_normal():
    assert calculate_total(100, 10, 5, 0.07) == 112.35

def test_calculate_total_zero_subtotal():
    assert calculate_total(0, 10, 5, 0.07) == 5.35

def test_calculate_total_negative_subtotal():
    with pytest.raises(ValueError):
        calculate_total(-100, 10, 5, 0.07)

def test_calculate_total_negative_shipping():
    with pytest.raises(ValueError):
        calculate_total(100, -10, 5, 0.07)

def test_calculate_total_negative_discount():
    with pytest.raises(ValueError):
        calculate_total(100, 10, -5, 0.07)

def test_calculate_total_negative_tax():
    with pytest.raises(ValueError):
        calculate_total(100, 10, 5, -0.07)

def test_item_calculate_total():
    assert Item("Tire", 379.99, 5).calculate_item_total() == 1899.95

def test_item_calculate_total_zero_quantity():
    assert Item("Tire", 379.99, 0).calculate_item_total() == 0.00

def test_item_calculate_total_return_case():
    assert Item("Tire", 379.99, -3).calculate_item_total() == -1139.97

def test_order_add_item():
    order = Order()
    item = Item("Tire", 379.99, 5)
    order.add_item(item)
    assert len(order.items) == 1
    assert order.items[0] == item

def test_order_add_no_items():
    order = Order()
    assert len(order.items) == 0

def test_order_add_multiple_items():
    order = Order()
    item1 = Item("Tire", 379.99, 5)
    item2 = Item("Oil Change", 29.99, 1)
    order.add_item(item1)
    order.add_item(item2)
    assert len(order.items) == 2
    assert order.items[0] == item1
    assert order.items[1] == item2

def test_order_add_item_none():
    order = Order()
    assert order.items == []

def test_order_calculate_subtotal():
    order = Order()
    item1 = Item("Tire", 379.99, 5)
    item2 = Item("Oil Change", 29.99, 1)
    order.add_item(item1)
    order.add_item(item2)
    assert order.calculate_subtotal() == 1929.94

def test_order_calculate_subtotal_no_items():
    order = Order()
    assert order.calculate_subtotal() == 0

def test_order_calculate_subtotal_return_item():
    order = Order()
    item1 = Item("Tire", 379.99, -5)
    order.add_item(item1)
    assert order.calculate_subtotal() == -1899.95

def test_order_calculate_order_total():
    order = Order(shipping=10, discount=5, tax_percent=0.07)
    item1 = Item("Tire", 379.99, 5)
    item2 = Item("Oil Change", 29.99, 1)
    order.add_item(item1)
    order.add_item(item2)
    assert order.calculate_order_total() == 2070.39

def test_order_calculate_order_total_no_items():
    order = Order(shipping=10, discount=5, tax_percent=0.07)
    assert order.calculate_order_total() == 5.35

def test_order_calculate_order_total_negative_subtotal():
    order = Order(shipping=10, discount=5, tax_percent=0.07)
    item1 = Item("Tire", 379.99, -5)
    order.add_item(item1)
    with pytest.raises(ValueError):
        order.calculate_order_total()

def test_order_calculate_order_total_no_shipping():
    order = Order(shipping=0, discount=5, tax_percent=0.07)
    item1 = Item("Tire", 379.99, 5)
    item2 = Item("Oil Change", 29.99, 1)
    order.add_item(item1)
    order.add_item(item2)
    assert order.calculate_order_total() == 2059.69

def test_get_reward_points():
    order = Order(shipping=10, discount=5, tax_percent=0.07)
    item1 = Item("Tire", 379.99, 5)
    item2 = Item("Oil Change", 29.99, 1)
    order.add_item(item1)
    order.add_item(item2)
    assert order.get_reward_points() == 2080

def test_get_reward_points_no_items():
    order = Order(shipping=10, discount=5, tax_percent=0.07)
    assert order.get_reward_points() == 5

def test_get_latest_price():
    item = DynamicallyPricedItem(1, 3)
    assert item.get_latest_price(19.99) == 19.99

def test_get_latest_price_invalid_id():
    with pytest.raises(ValueError):
        item = DynamicallyPricedItem(9999, 3)

def test_get_latest_price_zero_quantity():
    item = DynamicallyPricedItem(1, 0)
    assert item.get_latest_price(0.00) == 0.00

def test_get_latest_price_negative_quantity():
    item = DynamicallyPricedItem(1, -3)
    assert item.get_latest_price(-59.97) == -59.97

def test_dynamic_calculate_item_total():
    item = DynamicallyPricedItem(1, 3)
    assert item.calculate_item_total(19.99) == 59.97

def test_dynamic_calculate_item_total_zero_quantity():
    item = DynamicallyPricedItem(1, 0)
    assert item.calculate_item_total(0.00) == 0.00

def test_dynamic_calculate_item_total_negative_quantity():
    item = DynamicallyPricedItem(1, -3)
    assert item.calculate_item_total(19.99) == -59.97

def test_dynamic_calculate_item_total_invalid_id():
    with pytest.raises(ValueError):
        item = DynamicallyPricedItem(9999, 3)
        item.calculate_item_total(19.99)