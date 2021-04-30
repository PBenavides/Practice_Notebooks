### Acá definiremos el modelo Pytorch que usaremos.

import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import functional as F

input_size = 4
output_size = 3 #del target
hidden_size = 30 #Nro de neuronas por layer.

class ModeloIris(nn.Module):
    
    def __init__(self):
        super(ModeloIris, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.layer3 = nn.Linear(hidden_size, hidden_size)
        self.layerOut = nn.Linear(hidden_size, output_size)
        
    def forward(self, X):
        X = torch.sigmoid((self.layer1(X)))
        X = torch.sigmoid((self.layer2(X)))
        X = torch.sigmoid((self.layer3(X)))
        X = self.layerOut(X)
        
        return F.log_softmax(X, dim =-1)