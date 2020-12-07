import torch
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
import sys

from torch.autograd import Variable
 
class Connect4dataset(Dataset):
    def __init__(self, state_dir, action_dir, repeat=1):
        actions = np.load(action_dir)
        states = np.load(state_dir)
        idx = np.argwhere(actions == -1)
        idx = np.squeeze(idx)
        self.states = np.delete(states,idx,axis = 0)
        self.actions = np.delete(actions,idx)
        print(self.states.shape)
        print(self.actions.shape)
        self.len = self.actions.shape[0]
        self.repeat = repeat

    def __getitem__(self, i):
        index = i % self.len
        action = self.actions[index]
        state = self.states[index]
        variable_state = Variable(torch.FloatTensor(state))
        cuda_state = variable_state.cuda()
        cuda_state.retain_grad()
        variable_action = Variable(torch.tensor(action))
        cuda_action = variable_action.cuda()
        #cuda_action.retain_grad()
        return cuda_state, cuda_action
 
    def __len__(self):
        if self.repeat == None:
            data_len = self.len
        else:
            data_len = self.len * self.repeat
        return data_len

