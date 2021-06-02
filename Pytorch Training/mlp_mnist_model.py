import torch.nn as nn

class MLP(nn.Module):
  def __init__(self, i, u, v, o):
    """
    Donde i,u,v,o son los números de neuronas de 
    entrada y salida que tendrá mi red.
    """
    super().__init__()
    self.relu_layer = nn.ReLU()
    self.dense_1 = nn.Linear(i, u)
    self.b1 = nn.BatchNorm1d(20)
    self.dense_2 = nn.Linear(u,v)
    self.dense_output = nn.Linear(v, o)


  def forward(self, x):
    x = self.relu_layer(self.dense_1(x)) # activation( Capa )
    x = self.b1(x) #Batch Layer
    x = self.relu_layer(self.dense_2(x)) # Activation(Capa)

    logits = self.dense_output(x)

    return logits