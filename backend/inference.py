
# import torch
# from torchvision import transforms
# from PIL import Image
# from model import CNN_ViT_Hybrid


# # Config
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# MODEL_PATH = "./cnn_vit_model.pth"
# IMG_PATH = "../inp5.png"  

# from torchvision import datasets

# train_dataset = datasets.ImageFolder("../preprocessed/train")
# CLASS_NAMES = train_dataset.classes


# # CLASS_NAMES = ['adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'normal', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa']  # Replace with your actual class names

# # Transform
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5]*3, [0.5]*3)
# ])

# # Load Model
# model = CNN_ViT_Hybrid(num_classes=len(CLASS_NAMES)).to(device)
# model.load_state_dict(torch.load(MODEL_PATH, weights_only=False))
# model.eval()

# # Load Image
# image = Image.open(IMG_PATH).convert('RGB')
# image = transform(image).unsqueeze(0).to(device)

# # Predict
# with torch.no_grad():
#     outputs = model(image)
#     _, pred = torch.max(outputs, 1)
#     predicted_class = CLASS_NAMES[pred.item()]
#     print(f"Predicted Class: {predicted_class}")
 
 # new code 1
 # backend/inference.py

import torch
from torchvision import transforms
from PIL import Image
from model import CNN_ViT_Hybrid
import os

# Config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "cnn_vit_model.pth")

# Load Class Names dynamically
from torchvision import datasets
train_dataset = datasets.ImageFolder(os.path.join(CURRENT_DIR, "../preprocessed/train"))
CLASS_NAMES = train_dataset.classes

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Load Model
model = CNN_ViT_Hybrid(num_classes=len(CLASS_NAMES)).to(device)
model.load_state_dict(torch.load(MODEL_PATH, weights_only=False))
model.eval()

# 🔥 Define predict_image function properly
def predict_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, pred = torch.max(outputs, 1)
        predicted_class = CLASS_NAMES[pred.item()]
    return predicted_class
