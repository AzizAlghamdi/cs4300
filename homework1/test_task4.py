import task4
import pytest

def test_calculate_discount():
	assert task4.calculate_discount(100,10) == 90
	assert task4.calculate_discount(200.1, 20) == pytest.approx(160.0, abs=0.1)
