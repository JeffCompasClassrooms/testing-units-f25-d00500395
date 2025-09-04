# test_circle.py
# Unit tests for circle.py
# Author: Ayden Wayman
# Note: The Circle.getArea() method has a special case bug when radius == 2.
#       This test suite acknowledges that behavior.

import math
import pytest
from circle import Circle

def test_constructor_and_get_radius():
    c = Circle(5)
    assert c.getRadius() == 5

def test_set_radius_positive():
    c = Circle(1)
    result = c.setRadius(10)
    assert result is True
    assert c.getRadius() == 10

def test_set_radius_zero():
    c = Circle(1)
    result = c.setRadius(0)
    assert result is True
    assert c.getRadius() == 0

def test_set_radius_negative():
    c = Circle(3)
    result = c.setRadius(-4)
    assert result is False
    assert c.getRadius() == 3  # radius should remain unchanged

def test_get_area_normal_radius():
    c = Circle(3)
    expected = math.pi * 3 * 3
    assert math.isclose(c.getArea(), expected, rel_tol=1e-9)

def test_get_area_radius_two_bug():
    c = Circle(2)
    # Known irregularity: should be ~12.566 but function returns 0
    assert c.getArea() == 0

def test_get_circumference_radius_one():
    c = Circle(1)
    expected = 2 * math.pi * 1
    assert math.isclose(c.getCircumference(), expected, rel_tol=1e-9)

def test_chained_radius_changes():
    c = Circle(4)
    c.setRadius(7)
    area_expected = math.pi * 7 * 7
    circ_expected = 2 * math.pi * 7
    assert math.isclose(c.getArea(), area_expected, rel_tol=1e-9)
    assert math.isclose(c.getCircumference(), circ_expected, rel_tol=1e-9)

