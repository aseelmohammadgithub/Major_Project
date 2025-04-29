# import os
# import torch
# import torch.nn as nn
# from torch.utils.data import DataLoader
# from torchvision import datasets, transforms
# from model import CNN_ViT_Hybrid  # Ensure correct class is imported
# import torch.optim as optim

# # Define device
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Paths
# data_dir = 'preprocessed'
# train_dir = os.path.join(data_dir, 'train')
# val_dir = os.path.join(data_dir, 'valid')

# # Transforms (adjust mean and std if you have different channel counts)
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
# ])

# # Datasets and loaders
# train_ds = datasets.ImageFolder(train_dir, transform=transform)
# val_ds   = datasets.ImageFolder(val_dir, transform=transform)

# train_loader = torch.utils.data.DataLoader(train_ds, batch_size=16, shuffle=True)
# val_loader = torch.utils.data.DataLoader(val_ds, batch_size=16, shuffle=False)

# num_classes = len(train_ds.classes)

# # Instantiate model
# model = CNN_ViT_Hybrid(num_classes=num_classes).to(device)

# # Loss and optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=1e-4)

# # Training loop
# def train_model(model, train_loader, val_loader, criterion, optimizer, epochs=5):
#     for epoch in range(epochs):
#         model.train()
#         total_loss = 0
#         for images, labels in train_loader:
#             images, labels = images.to(device), labels.to(device)
#             outputs = model(images)
#             loss = criterion(outputs, labels)

#             optimizer.zero_grad()
#             loss.backward()
#             optimizer.step()

#             total_loss += loss.item()
            
#         print(f'Epoch {epoch+1}/{epochs} — Loss: {total_loss/len(train_loader):.4f}')
        
#         # Validation evaluation
#         model.eval()
#         correct = 0
#         total = 0
#         with torch.no_grad():
#             for images, labels in val_loader:
#                 images, labels = images.to(device), labels.to(device)
#                 outputs = model(images)
#                 _, predicted = torch.max(outputs.data, 1)
#                 total += labels.size(0)
#                 correct += (predicted == labels).sum().item()
#         print(f'Validation Accuracy: {100 * correct/total:.2f}%')

# if __name__ == '__main__':
#     train_model(model, train_loader, val_loader, criterion, optimizer, epochs=5)
#     # Optionally save your model after training
#     torch.save(model.state_dict(), 'cnn_vit_model.pth')

# new code
"""import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import CNN_ViT_Hybrid
import torch.optim as optim

device = torch.device('cpu')  # Force CPU usage

# Paths
data_dir = 'preprocessed'
train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'valid')

# CPU-efficient transforms
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Smaller image size
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

train_ds = datasets.ImageFolder(train_dir, transform=transform)
val_ds = datasets.ImageFolder(val_dir, transform=transform)

train_loader = DataLoader(train_ds, batch_size=8, shuffle=True)  # Small batch size for CPU
val_loader = DataLoader(val_ds, batch_size=8, shuffle=False)

num_classes = len(train_ds.classes)
model = CNN_ViT_Hybrid(num_classes=num_classes).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

def train_model(model, train_loader, val_loader, criterion, optimizer, epochs=3):
    for epoch in range(epochs):
        model.train()
        running_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print(f"Epoch {epoch+1}: Loss = {running_loss / len(train_loader):.4f}")

        # Eval
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print(f"Validation Accuracy: {100 * correct / total:.2f}%")

if __name__ == '__main__':
    train_model(model, train_loader, val_loader, criterion, optimizer, epochs=3)"""
    
# new code 2
# import torch
# import torchvision.transforms as transforms
# from torch.utils.data import DataLoader
# from torchvision.datasets import ImageFolder
# from model import CNN_ViT_Hybrid  # Replace with your actual model class name
# from torch import nn, optim

# # Set device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Parameters
# image_size = 224  # <-- Updated to match ViT input
# batch_size = 32
# epochs = 3
# learning_rate = 1e-4

# # Transforms
# transform = transforms.Compose([
#     transforms.Resize((image_size, image_size)),
#     transforms.ToTensor(),
# ])

# # Datasets
# train_dataset = ImageFolder(root="preprocessed/train", transform=transform)
# val_dataset = ImageFolder(root="preprocessed/valid", transform=transform)

# # Loaders
# train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
# val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# # Model
# model = CNN_ViT_Hybrid(image_size=image_size, num_classes=len(train_dataset.classes))
# model = model.to(device)

# # Loss and optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# # Training function
# def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
#     for epoch in range(epochs):
#         model.train()
#         running_loss = 0.0
#         correct = 0
#         total = 0

#         for images, labels in train_loader:
#             images = images.to(device)
#             labels = labels.to(device)

#             optimizer.zero_grad()
#             outputs = model(images)
#             loss = criterion(outputs, labels)
#             loss.backward()
#             optimizer.step()

#             running_loss += loss.item()
#             _, predicted = torch.max(outputs.data, 1)
#             total += labels.size(0)
#             correct += (predicted == labels).sum().item()

#         accuracy = 100 * correct / total
#         print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}, Accuracy: {accuracy:.2f}%")

# # Train
# train_model(model, train_loader, val_loader, criterion, optimizer, epochs)
# new code 3

# import torch
# import torchvision.transforms as transforms
# from torch.utils.data import DataLoader
# from torchvision.datasets import ImageFolder
# from model import CNN_ViT_Hybrid  # Import the model class
# from torch import nn, optim

# # Set device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Parameters
# image_size = 224  # Match the ViT input size
# batch_size = 32
# epochs = 6
# learning_rate = 3e-5

# # Transforms
# transform = transforms.Compose([
#     transforms.Resize((image_size, image_size)),
#     transforms.ToTensor(),
# ])

# # Datasets
# train_dataset = ImageFolder(root="preprocessed/train", transform=transform)
# val_dataset = ImageFolder(root="preprocessed/valid", transform=transform)

# # Loaders
# train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
# val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# # Model
# model = CNN_ViT_Hybrid(image_size=image_size, num_classes=len(train_dataset.classes))
# model = model.to(device)

# # Loss and optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# # Training function
# def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
#     for epoch in range(epochs):
#         model.train()
#         running_loss = 0.0
#         correct = 0
#         total = 0

#         for images, labels in train_loader:
#             images = images.to(device)
#             labels = labels.to(device)

#             optimizer.zero_grad()
#             outputs = model(images)
#             loss = criterion(outputs, labels)
#             loss.backward()
#             optimizer.step()

#             running_loss += loss.item()
#             _, predicted = torch.max(outputs.data, 1)
#             total += labels.size(0)
#             correct += (predicted == labels).sum().item()

#         accuracy = 100 * correct / total
#         print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}, Accuracy: {accuracy:.2f}%")

#     # Save model after training
#     torch.save(model.state_dict(), "cnn_vit_model.pth")
#     print("Model saved to cnn_vit_model.pth")

# # Train the model
# train_model(model, train_loader, val_loader, criterion, optimizer, epochs)

# new code 4
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model import CNN_ViT_Hybrid

import torch.optim as optim

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Parameters
image_size = 224  # Match ViT expected input
batch_size = 32
epochs = 6
learning_rate = 3e-5

# Paths
train_dir = "../preprocessed/train"
val_dir = "../preprocessed/valid"

# Transforms
train_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.5] * 3, [0.5] * 3)
])

val_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.5] * 3, [0.5] * 3)
])

# Datasets
train_dataset = datasets.ImageFolder(root=train_dir, transform=train_transform)
val_dataset = datasets.ImageFolder(root=val_dir, transform=val_transform)

# Loaders
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# Model
num_classes = len(train_dataset.classes)
model = CNN_ViT_Hybrid(image_size=image_size, num_classes=num_classes).to(device)

# Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training Function
def train_model(model, train_loader, val_loader, criterion, optimizer, epochs):
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss/len(train_loader):.4f}, Train Accuracy: {train_accuracy:.2f}%")

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()

        val_accuracy = 100 * val_correct / val_total
        print(f"Validation Accuracy: {val_accuracy:.2f}%")

    # Save model
    torch.save(model.state_dict(), "backend/cnn_vit_model.pth")
    print(" Model saved to cnn_vit_model.pth")

# Entry point
if __name__ == "__main__":
    train_model(model, train_loader, val_loader, criterion, optimizer, epochs)
