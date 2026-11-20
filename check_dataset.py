
from pathlib import Path
from collections import Counter

DATASET_PATH = Path(
    "data/Audio_Speech_Actors_01-24_16k"
)

emotion_names = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised",
}

audio_files = list(DATASET_PATH.rglob("*.wav"))

print("Total audio recordings found:", len(audio_files))

emotion_counts = Counter()

for file in audio_files:
    parts = file.stem.split("-")

    if len(parts) == 7:
        emotion_code = parts[2]
        emotion = emotion_names.get(emotion_code)

        if emotion:
            emotion_counts[emotion] += 1

print("\nRecordings for each emotion:")

for emotion, count in sorted(emotion_counts.items()):
    print(f"{emotion}: {count}")
