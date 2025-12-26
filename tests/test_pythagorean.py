"""Tests for PythagoreanScale class."""

import pytest
from pythagorean import PythagoreanScale


@pytest.mark.parametrize("freq", [660, 990, 1485, 2227.5, 3341.25, 5011.875])
def test_octave_reduce(freq):
    """Test octave reduction with multiple frequencies."""
    result = PythagoreanScale._octave_reduce(freq)
    print(f"\n{freq} Hz -> {result}")

    assert len(result) > 0
    assert result == sorted(result)
    assert all(f >= 20 for f in result)

    for i in range(len(result) - 1):
        assert result[i + 1] / result[i] == 2.0
