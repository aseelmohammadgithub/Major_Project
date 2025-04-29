# import os
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.models import load_model

# # ---------------------------
# # Configuration
# # ---------------------------
# IMG_SIZE = (224, 224)
# BATCH_SIZE = 32
# MODEL_PATH = "lung_cancer_model.h5"  # trained model path
# EVAL_DATASET_PATH = "preprocessed/valid"  # You can switch this to "preprocessed/test" too

# # ---------------------------
# # Load the trained model
# # ---------------------------
# model = load_model(MODEL_PATH)
# print(f"✅ Loaded model from {MODEL_PATH}")

# # ---------------------------
# # Load validation/test data
# # ---------------------------
# eval_datagen = ImageDataGenerator(rescale=1./255)

# eval_generator = eval_datagen.flow_from_directory(
#     EVAL_DATASET_PATH,
#     target_size=IMG_SIZE,
#     batch_size=BATCH_SIZE,
#     class_mode='categorical',
#     shuffle=False
# )

# # ---------------------------
# # Perform evaluation
# # ---------------------------
# loss, accuracy = model.evaluate(eval_generator)
# print(f"\n✅ Evaluation Results:")
# print(f"Loss: {loss:.4f}")
# print(f"Accuracy: {accuracy:.4f}")

# # ---------------------------
# # Predictions and Metrics
# # ---------------------------
# y_true = eval_generator.classes
# y_pred_probs = model.predict(eval_generator)
# y_pred = np.argmax(y_pred_probs, axis=1)
# class_labels = list(eval_generator.class_indices.keys())

# print("\n📋 Classification Report:")
# print(classification_report(y_true, y_pred, target_names=class_labels))

# # ---------------------------
# # Confusion Matrix
# # ---------------------------
# cm = confusion_matrix(y_true, y_pred)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)
# disp.plot(cmap=plt.cm.Blues)
# plt.title("Confusion Matrix")
# plt.show()

# new code 2
# import os
# import torch
# import numpy as np
# import matplotlib.pyplot as plt
# from torchvision import datasets, transforms
# from torch.utils.data import DataLoader
# from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
# from model import CNN_ViT_Hybrid

# # Configuration
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# IMG_SIZE = (224, 224)
# BATCH_SIZE = 32
# MODEL_PATH = "model.py"
# EVAL_DATASET_PATH = "preprocessed/valid"

# # Data Transform
# transform = transforms.Compose([
#     transforms.Resize(IMG_SIZE),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
# ])

# # Load Dataset
# eval_dataset = datasets.ImageFolder(EVAL_DATASET_PATH, transform=transform)
# eval_loader = DataLoader(eval_dataset, batch_size=BATCH_SIZE, shuffle=False)

# # Load Model
# model = CNN_ViT_Hybrid(num_classes=len(eval_dataset.classes))
# model.load_state_dict(torch.load(MODEL_PATH))
# model.to(device)
# model.eval()

# # Evaluation
# all_preds, all_labels = [], []
# with torch.no_grad():
#     for images, labels in eval_loader:
#         images, labels = images.to(device), labels.to(device)
#         outputs = model(images)
#         _, preds = torch.max(outputs, 1)
#         all_preds.extend(preds.cpu().numpy())
#         all_labels.extend(labels.cpu().numpy())

# # Classification Report
# print("\n📋 Classification Report:")
# print(classification_report(all_labels, all_preds, target_names=eval_dataset.classes))

# # Confusion Matrix
# cm = confusion_matrix(all_labels, all_preds)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=eval_dataset.classes)
# disp.plot(cmap=plt.cm.Blues)
# plt.title("Confusion Matrix")
# plt.show()

# new code 3

import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from model import CNN_ViT_Hybrid


# Configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
MODEL_PATH = "backend/cnn_vit_model.pth"  # Path to the saved model
EVAL_DATASET_PATH = "../preprocessed/valid"

# Data Transform
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# Load Dataset
eval_dataset = datasets.ImageFolder(EVAL_DATASET_PATH, transform=transform)
eval_loader = DataLoader(eval_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Load Model
model = CNN_ViT_Hybrid(num_classes=len(eval_dataset.classes))
model.load_state_dict(torch.load(MODEL_PATH))  # Load the trained model weights
model.to(device)
model.eval()

# Evaluation
all_preds, all_labels = [], []
with torch.no_grad():
    for images, labels in eval_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Classification Report
print("\n Classification Report:")
print(classification_report(all_labels, all_preds, target_names=eval_dataset.classes))

# Confusion Matrix
cm = confusion_matrix(all_labels, all_preds)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=eval_dataset.classes)
# disp.plot(cmap=plt.cm.Blues)
# plt.title("Confusion Matrix")
# plt.show()
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(14, 12))  # Larger figure size
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=eval_dataset.classes)
disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation=45)

plt.title("Confusion Matrix", fontsize=18)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to not cut labels
plt.savefig("backend/confusion_matrix.png", dpi=300, bbox_inches="tight")  # Save image if needed
plt.show()
