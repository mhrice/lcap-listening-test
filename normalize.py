import os
import glob
import argparse
import soundfile
import numpy as np
import pyloudnorm as pyln

from tqdm import tqdm

# loop through all files in the directory and loudness normalize them
# note: this will overwrite the original files
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root_dir",
        type=str,
        default="static/audio/",
        help="Path to the directory containing the audio files",
    )
    parser.add_argument(
        "--target_loudness",
        type=float,
        default=-14.0,
        help="Target loudness in LUFS",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="If true, don't write the normalized files to disk",
    )
    args = parser.parse_args()

    audio_files = []
    for ext in ["**/*.flac", "**/*.mp3", "**/*.wav", "**/*.ogg", "**/*.aiff"]:
        audio_files.extend(glob.glob(os.path.join(args.root_dir, ext), recursive=True))

    print(f"Found {len(audio_files)} audio files")

    for audio_file in tqdm(audio_files):
        try:
            data, rate = soundfile.read(audio_file)
            meter = pyln.Meter(rate)
            loudness_db = meter.integrated_loudness(data)

            # if the audio is already at the target loudness, skip it
            if np.isclose(args.target_loudness, loudness_db, rtol=0.1):
                continue

            loudness_delta = args.target_loudness - loudness_db
            loudness_delta_linear = 10 ** (loudness_delta / 20)
            data_normalized = data * loudness_delta_linear

            if not args.dry_run:
                soundfile.write(audio_file, data_normalized, rate)
        except Exception as e:
            print(f"Error processing {audio_file}: {e}")
            continue
