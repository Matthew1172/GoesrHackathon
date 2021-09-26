import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision
from torch.utils.data import DataLoader
from myCustomDataset import GoesrDataset 

in_c = 3
n_c = 10
l_r = 1e-3
b_s = 32
n_e = 1

rd = "/home/matthew/Desktop/FullDiskPngs/CloudMoistureImagery"
csv = "CMI.csv"
dataset = GoesrDataset(csv_file = csv, root_dir=rd, transform=transforms.ToTensor())


