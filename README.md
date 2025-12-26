# Pythagorean Scale Generator

A Python tool to generate and visualize the Pythagorean comma - the tuning discrepancy that occurs when building musical scales using the cycle of perfect fifths.

## What is the Pythagorean Comma?

The Pythagorean comma is a fundamental problem in music theory: when you stack 12 perfect fifths (ratio 3/2), you should theoretically return to your starting note 7 octaves higher. However, mathematically:

**(3/2)¹² ≠ 2⁷**

The difference is approximately **23.46 cents** (the Pythagorean comma). This script makes this drift both visible and audible by chaining octaves together, allowing the error to accumulate.

> *Note: 1 Hz is equal to roughly 4 cents*

## Features

- Generate Pythagorean scales using the cycle of fifths method
- Calculate and display frequency drift across multiple octaves
- Optional audio playback to *hear* the comma accumulation
- Customizable root frequency, number of octaves, and note duration

## Installation

```bash
pip install sounddevice numpy
```

## Usage

### Basic Examples

```bash
# Generate 3 octaves starting from A440 (default)
python pythagorean_scale.py

# Generate and play the scale
python pythagorean_scale.py -p

# Use C4 (261.63 Hz) as root with 5 octaves
python pythagorean_scale.py -r 261.63 -o 5

# Generate 7 octaves to clearly hear comma accumulation
python pythagorean_scale.py -o 7 -p -d 1.0
```

### Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--root` | `-r` | Root note frequency in Hz | 440.0 |
| `--num-octaves` | `-o` | Number of octaves to generate | 3 |
| `--duration` | `-d` | Duration of each note in seconds | 0.5 |
| `--play` | `-p` | Play the generated scale | False |

### Example Output

```
3 octaves (starting from 440.0 Hz):

Octave 1, drift = 0.0 Hz
  [247.5, 260.74, 278.44, 297.0, 330.0, 371.25, 391.11, 440.0, 495.0, 556.88, 594.0, 660.0]
Octave 2, drift = 1.59 Hz
  [495.0, 521.48, 556.88, 594.0, 660.0, 742.5, 782.22, 880.0, 990.0, 1113.76, 1188.0, 1320.0]
Octave 3, drift = 3.19 Hz
  [990.0, 1042.96, 1113.76, 1188.0, 1320.0, 1485.0, 1564.44, 1760.0, 1980.0, 2227.52, 2376.0, 2640.0]
```

## How It Works

1. **Cycle of Fifths**: Starting from the root note, multiply by 3/2 to get the next fifth
2. **Octave Reduction**: Bring the fifth back down to the same octave range as the root
3. **Scale Building**: Repeat 12 times to generate a complete chromatic scale
4. **Chaining Octaves**: Use the 13th note (octave + comma) as the root for the next octave
5. **Drift Calculation**: Compare each octave's starting frequency to what it "should" be

## Historical Context

This tuning problem has been known since ancient Greece and is why:
- Pure Pythagorean tuning doesn't work for keyboard instruments
- Various temperaments were developed (meantone, well-tempered)
- Modern equal temperament became the standard (each semitone = 2^(1/12))

## Testing

Run tests with pytest:

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run with output
pytest -v

# Run with print statements visible
pytest -s
```

## Author

Coded by **Alex Guillin**

## License

MIT
