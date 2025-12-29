"""Tests for PythagoreanScale class."""

import pytest
from pythagorean import PythagoreanScale


# Pythagorean ratios for each note relative to root
PYTHAGOREAN_RATIOS = [
    (1, 2187 / 2048),  # Index 1, Note 2
    (2, 9 / 8),  # Index 2, Note 3
    (3, 19683 / 16384),  # Index 3, Note 4
    (4, 81 / 64),  # Index 4, Note 5
    (5, 177147 / 131072),  # Index 5, Note 6
    (6, 729 / 512),  # Index 6, Note 7
    (7, 3 / 2),  # Index 7, Note 8
    (8, 6561 / 4096),  # Index 8, Note 9
    (9, 27 / 16),  # Index 9, Note 10
    (10, 59049 / 32768),  # Index 10, Note 11
    (11, 243 / 128),  # Index 11, Note 12
]


@pytest.mark.parametrize("freq", [660, 990, 1485, 2227.5, 3341.25, 5011.875])
def test_octave_reduce(freq):
    """Test octave reduction with multiple frequencies."""
    result = PythagoreanScale._octave_reduce(freq)
    print(f"\n{freq} Hz -> {result}")

    assert len(result) > 0
    assert result == sorted(result)
    assert all(f >= 20 for f in result)


@pytest.mark.parametrize("freq", [110, 220, 440, 835.31])
def test_generate_single_octave(freq):
    """Test single octave generation with correct ratios."""
    scale = PythagoreanScale()
    root = freq
    octave = scale._generate_single_octave(root)

    # 1. Check if octave is generated
    assert octave is not None
    assert isinstance(octave, list)

    # 2. Check if octave contains 13 notes (12 + root)
    assert len(octave) == 13

    # 3. Check if ratios between notes and root are correct
    # Sort octave (without the 13th note which is the comma)
    sorted_octave = sorted(octave[:-1])
    print(f"\nSorted octave: {sorted_octave}")

    for index, ratio in PYTHAGOREAN_RATIOS:
        expected = round(root * ratio, 2)
        actual = sorted_octave[index]
        print(
            f"Index {index} (Note {index + 1}): expected={expected}, actual={actual}, ratio={ratio}"
        )
        assert actual == expected


@pytest.mark.parametrize(
    "root,num_octaves", [(110, 2), (110, 8), (220, 8), (440, 8), (261.63, 8)]
)
def test_generate_octaves(root, num_octaves):
    """Test multiple octaves generation with correct ratios."""
    scale = PythagoreanScale(root=root, num_octaves=num_octaves)
    octaves = scale.octaves

    # 1. Check if octaves are correctly generated
    assert octaves is not None
    assert isinstance(octaves, list)
    assert len(octaves) == num_octaves

    # 2. Check if ratios are correct in each generated octave
    for octave_num, octave in enumerate(octaves, 1):
        # Use first note of sorted octave as reference
        octave_root = octave[0]
        print(f"\nOctave {octave_num}, root={octave_root}")
        print(f"Notes: {octave}")

        # Each octave should have 12 notes
        assert len(octave) == 12

        # Check ratios for this octave
        for index, ratio in PYTHAGOREAN_RATIOS:
            expected = round(octave_root * ratio, 2)
            actual = octave[index]
            print(
                f"  Index {index}: expected={expected}, actual={actual}, ratio={ratio}"
            )
            assert actual == expected
