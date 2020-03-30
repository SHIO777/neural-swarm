import torch
import torch.nn as nn
import torch.nn.functional as F

class phi_Net(nn.Module):
    def __init__(self):
        super(phi_Net, self).__init__()
        self.fc1 = nn.Linear(6, 25)
        self.fc2 = nn.Linear(25, 40)
        self.fc3 = nn.Linear(40, 40)
        self.fc4 = nn.Linear(40, 40)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x

class rho_Net(nn.Module):
    def __init__(self):
        super(rho_Net, self).__init__()
        self.fc1 = nn.Linear(40, 40)
        self.fc2 = nn.Linear(40, 40)
        self.fc3 = nn.Linear(40, 40)
        self.fc4 = nn.Linear(40, 1)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x