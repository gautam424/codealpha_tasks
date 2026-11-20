
from pathlib import Path
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATASET_PATH = Path("data/Audio_Speech_Actors_01-24_16k")
OUTPUT_PATH = Path("data/processed_data.npz")

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

features = []
labels = []

audio_files = sorted(DATASET_PATH.rglob("*.wav"))

print("Preparing", len(audio_files), "audio recordings...")

for i, file in enumerate(audio_files, start=1):
    parts = file.stem.split("-")

    if len(parts) != 7:
        continue

    emotion = emotion_names.get(parts[2])

    if emotion is None:
        continue

    try:
        audio, sample_rate = librosa.load(
            file, sr=16000, duration=3.0
        )

        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=40,
            n_fft=512,
            hop_length=160
        )

        # Make every recording have the same feature length.
        if mfcc.shape[1] < 300:
            mfcc = np.pad(
                mfcc,
                ((0, 0), (0, 300 - mfcc.shape[1]))
            )
        else:
            mfcc = mfcc[:, :300]

        features.append(mfcc)
        labels.append(emotion)

    except Exception as error:
        print("Could not process:", file.name, error)

    if i % 100 == 0:
        print(f"Checked {i}/{len(audio_files)} recordings")

X = np.array(features, dtype=np.float32)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

np.savez_compressed(
    OUTPUT_PATH,
    X_train=X_train,
    X_test=X_test,
    y_train=y_train,
    y_test=y_test,
    class_names=label_encoder.classes_
)

print("\nData preparation complete!")
print("Feature shape:", X.shape)
print("Training recordings:", len(X_train))
print("Testing recordings:", len(X_test))
print("Emotion classes:", list(label_encoder.classes_))
print("Saved to:", OUTPUT_PATH)
