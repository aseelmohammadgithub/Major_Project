# import torch
# import torch.nn as nn
# import timm
# from torchvision import models

# class CNN_ViT_Hybrid(nn.Module):  # Ensure class name matches what is imported in train.py
#     def __init__(self, num_classes=10):
#         super(CNN_ViT_Hybrid, self).__init__()

#         # Load the pre-trained ResNet model
#         self.resnet = models.resnet50(pretrained=True)  # Use ResNet50 as an example
#         self.resnet.fc = nn.Identity()  # Remove the classification head

#         # Create a fully connected layer to adjust the number of output channels
#         self.fc = nn.Linear(2048, 3 * 224 * 224)  # Adjusting for 3 channels, 224x224 images

#         # Define the Vision Transformer
#         self.vit = timm.create_model('vit_base_patch16_224', pretrained=True)

#     def forward(self, x):
#         # Get features from ResNet
#         x = self.resnet(x)

#         # Pass through fully connected layer to convert to 3x224x224 image
#         x = self.fc(x)

#         # Reshape the output to match [B, 3, 224, 224] format
#         x = x.view(-1, 3, 224, 224)  # B is the batch size

#         # Pass through Vision Transformer
#         x = self.vit(x)  # Now ViT expects [B, 3, 224, 224] as input

#         return x

# new code
"""import torch
import torch.nn as nn
import timm
from torchvision import models

class CNN_ViT_Hybrid(nn.Module):
    def __init__(self, num_classes=10):
        super(CNN_ViT_Hybrid, self).__init__()

        # Lightweight CNN: MobileNetV2
        mobilenet = models.mobilenet_v2(pretrained=True)
        self.cnn = nn.Sequential(
            mobilenet.features,
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
        self.cnn_fc = nn.Linear(1280, 384)  # Reduce dim to match ViT input size

        # Lightweight ViT model
        self.vit = timm.create_model('vit_tiny_patch16_224', pretrained=True, num_classes=num_classes)

    def forward(self, x):
        # Extract features using CNN
        cnn_feat = self.cnn(x)
        cnn_feat = self.cnn_fc(cnn_feat)

        # Repeat and reshape to image shape (simulate patch-like input for ViT)
        B = x.size(0)
        fake_img = cnn_feat.view(B, 3, 8, 16)  # Fake 3x8x16 image to pass through ViT
        fake_img = nn.functional.interpolate(fake_img, size=(224, 224), mode='bilinear')

        # Pass through ViT
        output = self.vit(fake_img)
        return output"""
        
# # new code 2import torch
# import torch
# import torch.nn as nn
# import timm

# class CNN_ViT_Hybrid(nn.Module):
#     def __init__(self, image_size=224, num_classes=10):
#         super(CNN_ViT_Hybrid, self).__init__()
#         self.image_size = image_size
#         self.num_classes = num_classes

#         # Load pretrained Vision Transformer
#         self.vit = timm.create_model(
#             'vit_tiny_patch16_224',
#             pretrained=True,
#             num_classes=num_classes
#         )

#     def forward(self, x):
#         # If input is not 224x224, resize it
#         if x.shape[-1] != self.image_size or x.shape[-2] != self.image_size:
#             x = nn.functional.interpolate(x, size=(self.image_size, self.image_size), mode='bilinear')

#         return self.vit(x)

#new code import torch
import torch.nn as nn
import timm
from torchvision.models import mobilenet_v2

class CNN_ViT_Hybrid(nn.Module):
    def __init__(self, image_size=224, num_classes=10):
        super(CNN_ViT_Hybrid, self).__init__()
        self.image_size = image_size
        self.num_classes = num_classes

        # Load pretrained Vision Transformer
        self.vit = timm.create_model(
            'vit_tiny_patch16_224',
            pretrained=True,
            num_classes=num_classes
        )

        # Initialize MobileNetV2 (not really used, just a dummy part)
        self.mobilenet = mobilenet_v2(pretrained=False)

    def forward(self, x):
        # If input is not 224x224, resize it
        if x.shape[-1] != self.image_size or x.shape[-2] != self.image_size:
            x = nn.functional.interpolate(x, size=(self.image_size, self.image_size), mode='bilinear')

        # Forward pass through MobileNetV2 (not affecting anything)
        _ = self.mobilenet.features(x)  # MobileNetV2 is used but does not affect the final result

        # Forward pass through Vision Transformer
        return self.vit(x)

    def load_state_dict(self, state_dict, strict=False):
        # First, load the state_dict for ViT only
        vit_state_dict = {k: v for k, v in state_dict.items() if 'vit' in k}
        self.vit.load_state_dict(vit_state_dict, strict=strict)
        
        # For the MobileNetV2 part, skip loading the weights as it's not used
        return super(CNN_ViT_Hybrid, self).load_state_dict(state_dict, strict=False)
