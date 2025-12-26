import bisect
import sounddevice as sd
import numpy as np


class PythagoreanScale:
    """Generates and manages Pythagorean musical scales."""

    def __init__(self, root=440.0, num_octaves=3):
        """Initialize with root frequency and number of octaves."""
        self.root = root
        self.num_octaves = num_octaves
        self.octaves = []
        self.drifts = []
        self._generate()

    def _generate(self):
        """Generate all octaves and calculate drifts."""
        self.octaves = self._generate_octaves()
        self.drifts = self._calculate_drifts()

    def _generate_octaves(self):
        """Generate multiple octaves, each starting from the last note of previous."""
        all_octaves = []
        current_root = self.root
        for _ in range(self.num_octaves):
            octave = self._generate_single_octave(current_root)
            current_root = octave[-1] * 2
            all_octaves.append(sorted(octave[:-1]))
        return all_octaves

    def _generate_single_octave(self, root):
        """Generate one octave of the Pythagorean scale (13 notes including octave)."""
        scale = [root]
        current = root
        for _ in range(12):
            current = self._find_next_note(current, root)
            scale.append(current)
        return [round(freq, 2) for freq in scale]

    def _find_next_note(self, current_freq, root_freq):
        """Find next note in Pythagorean tuning cycle of fifths."""
        fifth = current_freq * 3 / 2
        octave_reduced = self._octave_reduce(fifth)
        return self._upper_closest(octave_reduced, root_freq)

    @staticmethod
    def _octave_reduce(freq, min_freq=20):
        """Generate ascending list of frequencies reduced by octaves."""
        freqs = []
        while freq > min_freq:
            freqs.append(freq)
            freq /= 2
        return freqs[::-1]

    @staticmethod
    def _upper_closest(nums, x):
        """Find smallest number in sorted list that is >= x."""
        i = bisect.bisect_left(nums, x)
        return nums[i] if i < len(nums) else None

    def _calculate_drifts(self):
        """Calculate drift for each octave compared to previous octave."""
        drifts = [0.0]
        for i in range(1, len(self.octaves)):
            first_note_current = self.octaves[i][0]
            down_octave = first_note_current / 2
            first_note_previous = self.octaves[i - 1][0]
            drift = round(down_octave - first_note_previous, 2)
            drifts.append(drift)
        return drifts

    def display(self):
        """Display octaves and drifts."""
        print(f"{self.num_octaves} octaves (starting from {self.root} Hz):\n")
        for i, (octave, drift) in enumerate(zip(self.octaves, self.drifts), 1):
            print(f"Octave {i}, drift = {drift} Hz")
            print(f"  {octave}")

    def play(self, note_duration=0.5):
        """Play all octaves sequentially."""
        total_notes = sum(len(octave) for octave in self.octaves)
        print(f"\nPlaying {len(self.octaves)} octaves ({total_notes} notes total)...")

        note_count = 1
        for i, octave in enumerate(self.octaves, 1):
            print(f"\nOctave {i}:")
            for freq in octave:
                print(f"  Note {note_count}: {freq} Hz")
                self._play_frequency(freq, note_duration)
                note_count += 1

        print("Done!")

    @staticmethod
    def _play_frequency(freq, duration=0.5, sample_rate=44100):
        """Play a pure tone at given frequency."""
        t = np.linspace(0, duration, int(sample_rate * duration))
        wave = np.sin(2 * np.pi * freq * t)
        sd.play(wave, sample_rate)
        sd.wait()
