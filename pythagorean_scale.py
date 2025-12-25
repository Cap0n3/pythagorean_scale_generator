import bisect
import sounddevice as sd
import numpy as np
import argparse


def upper_closest(nums, x):
    """Find smallest number in sorted list that is >= x."""
    i = bisect.bisect_left(nums, x)
    return nums[i] if i < len(nums) else None


def octave_reduce(freq, min_freq=20):
    """Generate ascending list of frequencies reduced by octaves."""
    freqs = []
    while freq > min_freq:
        freqs.append(freq)
        freq /= 2
    return freqs[::-1]


def find_next_note(current_freq, root_freq):
    """Find next note in Pythagorean tuning cycle of fifths."""
    fifth = current_freq * 3 / 2
    octave_reduced = octave_reduce(fifth)
    return upper_closest(octave_reduced, root_freq)


def generate_pythagorean_scale_octave(root=440):
    """Generate one octave of the Pythagorean scale (13 notes including octave)."""
    scale = [root]
    num_notes = 12
    current = root
    for _ in range(num_notes):
        current = find_next_note(current, root)
        scale.append(current)
    return [round(freq, 2) for freq in scale]


def generate_octaves(root, num_octaves=3):
    """Generate multiple octaves, each starting from the last note of previous."""
    all_octaves = []
    current_root = root
    for _ in range(num_octaves):
        octave = generate_pythagorean_scale_octave(current_root)
        current_root = octave[-1] * 2  # Next octave root note
        all_octaves.append(sorted(octave[:-1]))  # Remove 13th note and sort
    return all_octaves


def calculate_drifts(all_octaves):
    """Calculate drift for each octave compared to previous octave."""
    drifts = [0.0]  # First octave has no drift

    for i in range(1, len(all_octaves)):
        first_note_current = all_octaves[i][0]
        down_octave = first_note_current / 2
        first_note_previous = all_octaves[i - 1][0]
        drift = round(down_octave - first_note_previous, 2)
        drifts.append(drift)

    return drifts


def play_frequency(freq, duration=0.5, sample_rate=44100):
    """Play a pure tone at given frequency."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * freq * t)
    sd.play(wave, sample_rate)
    sd.wait()


def play_scale(all_octaves, note_duration=0.5):
    """Play all octaves sequentially."""
    total_notes = sum(len(octave) for octave in all_octaves)
    print(f"\nPlaying {len(all_octaves)} octaves ({total_notes} notes total)...")

    note_count = 1
    for i, octave in enumerate(all_octaves, 1):
        print(f"\nOctave {i}:")
        for freq in octave:
            print(f"  Note {note_count}: {freq} Hz")
            play_frequency(freq, duration=note_duration)
            note_count += 1

    print("Done!")


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

    # Generate multiple octaves
    all_octaves = generate_octaves(args.root, args.num_octaves)
    drifts = calculate_drifts(all_octaves)

    print(f"{args.num_octaves} octaves (starting from {args.root} Hz):\n")

    for i, (octave, drift) in enumerate(zip(all_octaves, drifts), 1):
        print(f"Octave {i}, drift = {drift} Hz")
        print(f"  {octave}")

    # Play all octaves if requested
    if args.play:
        play_scale(all_octaves, note_duration=args.duration)
