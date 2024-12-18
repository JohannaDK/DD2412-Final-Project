import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import flatten
import torch.optim
from src.utils.utils import *

class TST(nn.Module):
    def __init__(self, dataset="MNIST", latent_dim=128, num_classes=10, separate_body=False, pretrained_qyx = None, accelerator="cpu", MLP_size=3,
                 paper=None, simple_CNN=False, ViT_experiment=False, reinit_experiment=False, model_name_or_path='google/vit-base-patch16-224-in21k',
                 ResNet50_experiment = False, EfficientNet_experiment = False):
        super().__init__()
        self.latent_dim = latent_dim
        
        if dataset == "CIFAR10" or separate_body:
            self.separate_body = True
        else:
            self.separate_body = False
        if dataset == "CIFAR10" or self.separate_body:
            self.qzx_body = construct_ClassYEncoderBody(pretrained_model=pretrained_qyx, simple_CNN=simple_CNN, ViT_experiment=ViT_experiment, dataset=dataset, model_name_or_path=model_name_or_path,
                                                        ResNet50_experiment=ResNet50_experiment, EfficientNet_experiment=EfficientNet_experiment)

        if reinit_experiment:
            self.reinit_experiment = True
            self.pyz = reset_CIFA10LabelDecoder(num_classes=num_classes)
        else:
            self.reinit_experiment = False
            self.qzx_model = construct_ClassYEncoder(dataset, latent_dim, simple_CNN=simple_CNN, num_layers=MLP_size, ViT_experiment=ViT_experiment, ResNet50_experiment=ResNet50_experiment, EfficientNet_experiment=EfficientNet_experiment)
            self.pyz = construct_LabelDecoder(dataset, self.latent_dim, num_classes=num_classes)

        self.return_z = False

        self.num_classes = num_classes
        if dataset.find("MNIST") == -1:
            self.input_h = 28
            self.input_w = 28
        elif dataset=="CIFAR10":
            self.input_h = 32
            self.input_w = 32  

        if accelerator == "gpu":
            self.device = "cuda:0"
        else:
            self.device = "cpu"

    def encode(self, x):
        if self.separate_body:
            x = self.qzx_body(x)
            if self.reinit_experiment:
                return x
        return self.qzx_model(x)

    def decode(self, z):
        pyz = self.pyz(z)
        return pyz

    def forward(self, x):
        z = self.encode(x)
        y = self.decode(z)
        if self.training:
            return y, z
        else:
            if self.return_z:
                return y, z
            else:
                return y
