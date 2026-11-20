
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, classification_report

# 1. Set up
torch.manual_seed(42)
np.random.seed(42)

DEVICE = torch.device("cpu")
DATA_PATH = Path("data/processed_data.npz")
MODEL_PATH = Path("models/emotion_model.pth")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# 2. Load prepared audio features
data = np.load(DATA_PATH, allow_pickle=False)

X_train = data["X_train"]
X_test = data["X_test"]
y_train = data["y_train"]
y_test = data["y_test"]
class_names = data["class_names"].tolist()

print("Training recordings:", len(X_train))
print("Testing recordings:", len(X_test))
print("Emotions:", class_names)

# 3. Normalize MFCC features using training data only
mean = X_train.mean()
std = X_train.std() + 1e-8

X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

# CNN input shape: recordings, channels, MFCCs, time
X_train = torch.tensor(X_train, dtype=torch.float32).unsqueeze(1)
X_test = torch.tensor(X_test, dtype=torch.float32).unsqueeze(1)

y_train = torch.tensor(y_train, dtype=torch.long)
y_test = torch.tensor(y_test, dtype=torch.long)

train_loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=32,
    shuffle=True
)

# 4. Define a small CNN

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
        x = self.features(x)
        return self.classifier(x)


model = EmotionCNN(len(class_names)).to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 5. Train the model
EPOCHS = 50

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for inputs, targets in train_loader:
        inputs = inputs.to(DEVICE)
        targets = targets.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * inputs.size(0)
        predictions = outputs.argmax(dim=1)
        correct += (predictions == targets).sum().item()
        total += targets.size(0)

    average_loss = total_loss / total
    train_accuracy = correct / total * 100

    print(
        f"Epoch {epoch + 1:02d}/{EPOCHS} | "
        f"Loss: {average_loss:.4f} | "
        f"Training accuracy: {train_accuracy:.2f}%"
    )

# 6. Evaluate on recordings not used for training
model.eval()

with torch.no_grad():
    outputs = model(X_test.to(DEVICE))
    predictions = outputs.argmax(dim=1).cpu().numpy()

test_accuracy = accuracy_score(y_test.numpy(), predictions)

print("\nTest accuracy:", f"{test_accuracy * 100:.2f}%")
print("\nClassification report:")
print(
    classification_report(
        y_test.numpy(),
        predictions,
        labels=list(range(len(class_names))),
        target_names=class_names,
        zero_division=0
    )
)

# 7. Save model and normalization information
torch.save(
    {
        "model_state_dict": model.state_dict(),
        "class_names": class_names,
        "mean": float(mean),
        "std": float(std),
        "n_mfcc": 40,
        "sample_rate": 16000,
        "max_frames": 300,
        "test_accuracy": float(test_accuracy)
    },
    MODEL_PATH
)

print("\nModel saved to:", MODEL_PATH)
