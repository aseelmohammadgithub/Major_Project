
# import torch
# import torchvision.transforms as transforms
# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
# from PIL import Image
# from model import CNN_ViT_Hybrid


# # Config
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# MODEL_PATH = "./cnn_vit_model.pth"
# IMG_PATH = "../inp5.png"  # Change this to the image path

# # Dataset
# from torchvision import datasets
# train_dataset = datasets.ImageFolder("../preprocessed/train")
# CLASS_NAMES = train_dataset.classes

# # Preprocessing
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
# original_image = Image.open(IMG_PATH).convert('RGB')
# image = transform(original_image).unsqueeze(0).to(device)

# # Forward hook
# features = {}

# def hook_fn(module, input, output):
#     features["attn"] = output
    
# # Function to generate dynamic explanation
# def generate_explanation(pred_class, center, radius, detected_feature):
#     """
#     This function dynamically generates explanations based on the predicted class
#     and the features detected in the image.
#     """
#     if pred_class.lower() != "normal":
#         # Generate explanation for cancer or abnormal conditions
#         return (f"Based on the input image, the model detected {detected_feature} in the region "
#                 f"near the coordinates ({center[0]}, {center[1]}) with a radius of {radius} pixels. "
#                 f"These features are typically associated with {pred_class} growth, which led the model "
#                 f"to classify the image as {pred_class}.")
#     else:
#         # Generate explanation for normal conditions
#         return ("The model analyzed the image and found no irregularities or suspicious patterns. "
#                 "Therefore, the image was classified as normal, indicating no signs of cancer or abnormalities.")


# # Register hook to an earlier block
# hook = model.vit.blocks[5].register_forward_hook(hook_fn)

# # Forward pass
# output = model(image)
# _, pred = torch.max(output, 1)
# pred_class = CLASS_NAMES[pred.item()]
# print(f"Predicted Class: {pred_class}")

# # Attention Map from last block
# attn = features["attn"].squeeze(0).mean(dim=0).detach().cpu().numpy()
# attn = cv2.resize(attn, (224, 224))

# # Normalize attention map
# attn_norm = (attn - attn.min()) / (attn.max() - attn.min())

# # Threshold the attention map to highlight significant areas
# threshold = 0.7  # You can experiment with 0.4 to 0.7
# mask = (attn_norm > threshold).astype(np.uint8) * 255

# # Find contours of the highlighted areas
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Convert PIL image to OpenCV format for overlay
# original_image_cv = np.array(original_image.resize((224, 224)))[:, :, ::-1] / 255.0

# # Prepare explanation text
# explanation_text = ""
# output_img = np.copy(original_image_cv)  # Create a copy of the original image for overlay

# # Check if the predicted class is normal
# if pred_class.lower() != "normal":
#     # If cancer, draw red circle and explain
#     if contours:
#         largest_contour = max(contours, key=cv2.contourArea)  # Get the largest contour

#         # Find the center and radius of the largest contour to highlight the region
#         (x, y), radius = cv2.minEnclosingCircle(largest_contour)
#         center = (int(x), int(y))
#         radius = int(radius)

#         # Draw a dark red circle around the cancerous area
#         cv2.circle(output_img, center, radius, (0, 0, 139), 3)

#         # Dynamically generate the explanation text
#         explanation_text = generate_explanation(pred_class, center, radius, "irregular patterns")
# else:
#     # If normal, explain no abnormal areas detected
#     explanation_text = generate_explanation(pred_class, None, None, "no abnormal patterns")

# # Convert the image back to RGB for displaying
# output_img = cv2.cvtColor(np.uint8(output_img * 255), cv2.COLOR_BGR2RGB)

# # Display the image with explanation
# plt.imshow(output_img)
# plt.title(f"Grad-CAM Visualization - {pred_class}")
# plt.axis('off')

# # Add dynamic textual explanation
# plt.figtext(0.5, 0.05, explanation_text, wrap=True, horizontalalignment='center', fontsize=10)

# # Save the output image with Grad-CAM visualization
# plt.savefig("./gradcam_output_with_explanation.jpg", dpi=300)
# plt.show()

# # Remove hook
# hook.remove()

# new code 
# backend/gradcam.py

# import torch
# import torchvision.transforms as transforms
# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
# from PIL import Image
# from model import CNN_ViT_Hybrid
# import os

# # Config
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(CURRENT_DIR, "cnn_vit_model.pth")

# # Dataset
# from torchvision import datasets
# train_dataset = datasets.ImageFolder(os.path.join(CURRENT_DIR, "../preprocessed/train"))
# CLASS_NAMES = train_dataset.classes

# # Preprocessing
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5]*3, [0.5]*3)
# ])

# # Load Model
# model = CNN_ViT_Hybrid(num_classes=len(CLASS_NAMES)).to(device)
# model.load_state_dict(torch.load(MODEL_PATH, weights_only=False))
# model.eval()

# #  Define reusable generate_gradcam function
# def generate_gradcam(input_image_path, output_image_path):
#     original_image = Image.open(input_image_path).convert('RGB')
#     image = transform(original_image).unsqueeze(0).to(device)

#     # Forward hook
#     features = {}
#     def hook_fn(module, input, output):
#         features["attn"] = output

#     hook = model.vit.blocks[5].register_forward_hook(hook_fn)

#     # Forward pass
#     output = model(image)
#     _, pred = torch.max(output, 1)
#     pred_class = CLASS_NAMES[pred.item()]

#     # Attention Map
#     attn = features["attn"].squeeze(0).mean(dim=0).detach().cpu().numpy()
#     attn = cv2.resize(attn, (224, 224))

#     # Normalize
#     attn_norm = (attn - attn.min()) / (attn.max() - attn.min())

#     # Threshold the attention map
#     threshold = 0.7
#     mask = (attn_norm > threshold).astype(np.uint8) * 255

#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Overlay
#     original_image_cv = np.array(original_image.resize((224, 224)))[:, :, ::-1] / 255.0
#     output_img = np.copy(original_image_cv)

#     if pred_class.lower() != "normal" and contours:
#         largest_contour = max(contours, key=cv2.contourArea)
#         (x, y), radius = cv2.minEnclosingCircle(largest_contour)
#         center = (int(x), int(y))
#         radius = int(radius)
#         cv2.circle(output_img, center, radius, (0, 0, 139), 3)

#     # Convert to RGB and Save
#     output_img = cv2.cvtColor(np.uint8(output_img * 255), cv2.COLOR_BGR2RGB)
#     plt.imshow(output_img)
#     plt.axis('off')
#     plt.title(f"Grad-CAM Visualization - {pred_class}")
#     plt.savefig(output_image_path, dpi=200, bbox_inches='tight')
#     plt.close()

#     hook.remove()
import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
from model import CNN_ViT_Hybrid
import os

# Config
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "cnn_vit_model.pth")

# Dataset (to get class names)
from torchvision import datasets
train_dataset = datasets.ImageFolder(os.path.join(CURRENT_DIR, "../preprocessed/train"))
CLASS_NAMES = train_dataset.classes

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Load Model
model = CNN_ViT_Hybrid(num_classes=len(CLASS_NAMES)).to(device)
model.load_state_dict(torch.load(MODEL_PATH, weights_only=False))
model.eval()

# Helper: generate explanation text
def generate_explanation(pred_class, center, radius, detected_feature):
    if pred_class.lower() != "normal":
        return (
            f"Based on the input image, the model detected {detected_feature} in the region "
            f"near the coordinates ({center[0]}, {center[1]}) with a radius of {radius} pixels. "
            f"These features are typically associated with {pred_class} growth, which led the model "
            f"to classify the image as {pred_class}."
        )
    else:
        return (
            "The model analyzed the image and found no irregularities or suspicious patterns. "
            "Therefore, the image was classified as normal, indicating no signs of cancer or abnormalities."
        )

# Generate Grad-CAM and overlay text
def generate_gradcam(input_image_path, output_image_path):
    # Load & preprocess image
    original_image = Image.open(input_image_path).convert('RGB')
    image = transform(original_image).unsqueeze(0).to(device)

    # Hook to capture attention
    features = {}
    def hook_fn(module, inp, outp):
        features['attn'] = outp
    hook = model.vit.blocks[5].register_forward_hook(hook_fn)

    # Forward pass
    output = model(image)
    _, pred = torch.max(output, 1)
    pred_class = CLASS_NAMES[pred.item()]

    # Build attention map
    attn = features['attn'].squeeze(0).mean(dim=0).detach().cpu().numpy()
    attn = cv2.resize(attn, (224, 224))
    attn_norm = (attn - attn.min()) / (attn.max() - attn.min())
    mask = (attn_norm > 0.7).astype(np.uint8) * 255

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Prepare image for overlay
    original_cv = np.array(original_image.resize((224, 224)))[:, :, ::-1] / 255.0
    output_img = original_cv.copy()

    # Initialize explanation
    explanation_text = ''
    center = None
    radius = None

    if pred_class.lower() != 'normal' and contours:
        largest = max(contours, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(largest)
        center = (int(x), int(y))
        radius = int(r)
        cv2.circle(output_img, center, radius, (0, 0, 139), 3)
        explanation_text = generate_explanation(pred_class, center, radius, 'irregular patterns')
    else:
        explanation_text = generate_explanation(pred_class, None, None, 'no abnormal patterns')

    # Convert to displayable RGB
    output_img = cv2.cvtColor((output_img * 255).astype(np.uint8), cv2.COLOR_BGR2RGB)

    # Plot image and explanation separately
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [4, 1]})

    # Image
    ax1.imshow(output_img)
    ax1.set_title(f"Grad-CAM Visualization - {pred_class}")
    ax1.axis('off')

    # Text
    ax2.axis('off')
    ax2.text(0.5, 0.5, explanation_text, wrap=True, horizontalalignment='center', verticalalignment='center', fontsize=10)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()

    hook.remove()
