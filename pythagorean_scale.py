#!/usr/bin/env python3
"""Command-line interface for Pythagorean scale generation."""

import argparse
from pythagorean import PythagoreanScale


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Pythagorean scale demonstrating the Pythagorean comma effect",
        epilog="""
        Examples:
          %(prog)s                     # Default: A440, 3 octaves
          %(prog)s -r 261.63 -o 5      # C4 root, 5 octaves
          %(prog)s -o 7 -d 1.0         # 7 octaves to hear comma accumulation
          %(prog)s -p                  # Play the generated scale
        The Pythagorean comma is the ~23.46 cent drift that occurs because 
        (3/2)^12 ≠ 2^7. This script chains octaves to make the drift audible.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-r",
        "--root",
        type=float,
        default=440.0,
        help="Root note frequency in Hz (default: 440.0)",
    )
    parser.add_argument(
        "-o",
        "--num-octaves",
        type=int,
        default=3,
        help="Number of octaves to generate (default: 3)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=0.5,
        help="Duration of each note in seconds (default: 0.5)",
    )
    parser.add_argument(
        "-p",
        "--play",
        action="store_true",
        help="Play the generated scale",
    )

    args = parser.parse_args()

    # Create scale and generate
    scale = PythagoreanScale(root=args.root, num_octaves=args.num_octaves)

    # Display results
    scale.display()

    # Play if requested
    if args.play:
        scale.play(note_duration=args.duration)
