# import os
# import torch
# from torch.utils.data import DataLoader
# from torchvision import datasets, transforms
# from model import CNN_ViT_Hybrid
# from sklearn.metrics import classification_report, confusion_matrix

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Paths
# data_dir = 'preprocessed'
# test_dir = os.path.join(data_dir, 'test')

# # Transforms – same normalization as training
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
# ])

# # Dataset and loader
# test_ds = datasets.ImageFolder(test_dir, transform=transform)
# test_loader = DataLoader(test_ds, batch_size=32)

# # Load the model (make sure num_classes matches)
# num_classes = len(test_ds.classes)
# model = CNN_ViT_Hybrid(num_classes=num_classes)
# model.load_state_dict(torch.load('cnn_vit_model.pth'))
# model.to(device)
# model.eval()

# all_preds = []
# all_labels = []

# with torch.no_grad():
#     for images, labels in test_loader:
#         images, labels = images.to(device), labels.to(device)
#         outputs = model(images)
#         _, preds = torch.max(outputs, 1)
#         all_preds.extend(preds.cpu().numpy())
#         all_labels.extend(labels.cpu().numpy())

# print("Classification Report:")
# from sklearn.metrics import classification_report
# print(classification_report(all_labels, all_preds, target_names=test_ds.classes))

# print("Confusion Matrix:")
# from sklearn.metrics import confusion_matrix
# cm = confusion_matrix(all_labels, all_preds)
# print(cm)

# new code 1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model import CNN_ViT_Hybrid

from sklearn.metrics import accuracy_score

# Config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
TEST_DIR = "../preprocessed/test"
BATCH_SIZE = 32
MODEL_PATH = "backend/cnn_vit_model.pth"

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Dataset & Loader
test_dataset = datasets.ImageFolder(TEST_DIR, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Load Model
model = CNN_ViT_Hybrid(num_classes=len(test_dataset.classes)).to(device)
model.load_state_dict(torch.load(MODEL_PATH, weights_only=False))
model.eval()

# Prediction
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Accuracy
acc = accuracy_score(all_labels, all_preds)
print(f"\nTest Accuracy: {acc * 100:.2f}%")
