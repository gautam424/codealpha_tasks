
import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import librosa
import os

# Application settings
st.set_page_config(
    page_title="Speech Emotion Recognition",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Speech Emotion Recognition")
st.write(
    "Upload a speech recording and let the AI model "
    "predict the emotion expressed in the voice."
)

# Device
DEVICE = torch.device("cpu")

# Model architecture — must match train_model.py
class EmotionCNN(nn.Module):
    def __init__(self, number_of_classes):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),

            nn.AdaptiveAvgPool2d((4, 10)),
            nn.Flatten()
        )

        self.classifier = nn.Sequential(
            nn.Linear(128 * 4 * 10, 128),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(128, number_of_classes)
        )

    def forward(self, x):
        return self.classifier(self.features(x))


# Load the saved model
@st.cache_resource
def load_model():
    path = os.path.join("models", "emotion_model.pth")

    checkpoint = torch.load(
        path, map_location=DEVICE, weights_only=False
    )

    class_names = checkpoint["class_names"]

    model = EmotionCNN(len(class_names))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, class_names, checkpoint


try:
    model, class_names, checkpoint = load_model()
    st.success("Trained model loaded successfully!")
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()


# Audio feature extraction — must match prepare_data.py
def extract_features(audio_path):
    audio, sr = librosa.load(
        audio_path, sr=16000, duration=3.0
    )

    max_length = 16000 * 3

    if len(audio) < max_length:
        audio = np.pad(
            audio, (0, max_length - len(audio))
        )
    else:
        audio = audio[:max_length]

    mfcc = librosa.feature.mfcc(
        y=audio, sr=16000, n_mfcc=40
    )

    target_frames = 300

    if mfcc.shape[1] < target_frames:
        mfcc = np.pad(
            mfcc,
            ((0, 0), (0, target_frames - mfcc.shape[1]))
        )
    else:
        mfcc = mfcc[:, :target_frames]

    mean = float(checkpoint["mean"])
    std = float(checkpoint["std"])
    mfcc = (mfcc - mean) / (std + 1e-8)

    return torch.tensor(
        mfcc, dtype=torch.float32
    ).unsqueeze(0).unsqueeze(0)


# Upload audio
uploaded_file = st.file_uploader(
    "Choose a speech recording",
    type=["wav"]
)

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("Predict Emotion"):
        with st.spinner("Analyzing the voice..."):
            try:
                features = extract_features(
                    uploaded_file
                )

                with torch.no_grad():
                    outputs = model(features)
                    probabilities = torch.softmax(
                        outputs, dim=1
                    )[0]

                predicted_index = int(
                    torch.argmax(probabilities).item()
                )

                emotion = class_names[predicted_index]
                confidence = (
                    probabilities[predicted_index].item()
                    * 100
                )

                st.subheader("Prediction")
                st.markdown(f"### 🎯 {emotion.capitalize()}")
                st.write(
                    f"Model confidence: {confidence:.2f}%"
                )

                st.caption(
                    "This is the model's confidence in its "
                    "predicted class, not a guarantee that "
                    "the emotion is correct."
                )

                st.subheader("All emotion scores")

                for i, name in enumerate(class_names):
                    score = probabilities[i].item()
                    st.write(
                        f"{name.capitalize()}: {score * 100:.1f}%"
                    )
                    st.progress(score)

            except Exception as e:
                st.error(f"Prediction failed: {e}")
