import os
import glob
import argparse
import soundfile
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

    audio_files = glob.glob(os.path.join(args.root_dir, "**/*.flac"), recursive=True)
    print(f"Founds {len(audio_files)} audio files")

    for audio_file in tqdm(audio_files):
        data, rate = soundfile.read(audio_file)
        meter = pyln.Meter(rate)
        loudness_db = meter.integrated_loudness(data)
        loudness_delta = args.target_loudness - loudness_db
        loudness_delta_linear = 10 ** (loudness_delta / 20)
        data_normalized = data * loudness_delta_linear

        if not args.dry_run:
            soundfile.write(audio_file, data_normalized, rate)
