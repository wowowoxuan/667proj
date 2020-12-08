import torch
import torchvision
import torch.nn as nn
import math
import torch.nn.functional as F
import numpy as np
import sys
import torch.utils.data as data
from torchvision import datasets
import torch.optim as optim

from dataset_utils import Connect4dataset
#CNN model
# class CNNAIPlayer(nn.Module):  
#     def __init__(self,in_channel,out_channel):
#         super(CNNAIPlayer, self).__init__()
#         self.main = nn.Sequential(
#             nn.Conv2d(in_channels=2, out_channels=32, padding=1, kernel_size=3, stride=1),
#             nn.BatchNorm2d(32),
#             nn.ReLU(True),
#             nn.Dropout(),
#             nn.Conv2d(in_channels=32, out_channels=64, padding=1, kernel_size=3, stride=1),
#             nn.BatchNorm2d(64),
#             nn.ReLU(True),
#             nn.Dropout(),
#             nn.Flatten()           
#         )
#         self.fullyconnectblock = nn.Sequential(
#             nn.Linear(in_channel, 1024),
#             nn.BatchNorm1d(1024),
#             nn.ReLU(inplace=True),
#             nn.Dropout(p = 0.5),
#             nn.Linear(1024, 256),
#             nn.BatchNorm1d(256),
#             nn.ReLU(inplace=True),
#             nn.Dropout(p = 0.5),
#             nn.Linear(256, out_channel)
#         )
#     def forward(self, x):
#         x = self.main(x)
#         x = self.fullyconnectblock(x)
#         return F.log_softmax(x, dim=1)

class CNNpolicy(nn.Module):  
    def __init__(self,in_channel,out_channel):
        super(CNNpolicy, self).__init__()

        self.fullyconnectblock = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_channel, 50),
            nn.BatchNorm1d(50),
            nn.ReLU(inplace=True),
            nn.Dropout(p = 0.5),
            nn.Linear(50, 50),
            nn.BatchNorm1d(50),
            nn.ReLU(inplace=True),
            nn.Dropout(p = 0.5),
            nn.Linear(50, out_channel)

        )
    def forward(self, x):
        x = self.fullyconnectblock(x)
        return x

def calscale():
    all_dataset = Connect4dataset('./data/state7x7.npy','./data/action7x7.npy')
    trainloader = torch.utils.data.DataLoader(all_dataset, batch_size=1,shuffle=True)
    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    temp = []
    for state, actiongt in trainloader:
        if actiongt.cpu().clone().detach().numpy()[0] == 0:
            count0 += 1
        if actiongt.cpu().clone().detach().numpy()[0] == 1:
            count1 += 1
        if actiongt.cpu().clone().detach().numpy()[0] == 2:
            count2 += 1
        if actiongt.cpu().clone().detach().numpy()[0] == 3:
            count3 += 1
            print(state[0].shape)
            temp.append(state[0].cpu().clone().detach().numpy())
        if actiongt.cpu().clone().detach().numpy()[0] == 4:
            count4 += 1
        if actiongt.cpu().clone().detach().numpy()[0] == 5:
            count5 += 1
        if actiongt.cpu().clone().detach().numpy()[0] == 6:
            count6 += 1
    # print(count0)
    # print(count1)
    # print(count2)
    # print(count3)
    # print(count4)
    # print(count5)
    # print(count6)
    listt = np.array(temp)
    listt = np.unique(listt, axis=0)

    print(len(temp))
    print(listt.shape)


def train():
    #load dataset
    all_dataset = Connect4dataset('./data1/state7x7.npy','./data1/action7x7.npy')
    print(len(all_dataset))
    train_set_length = int(len(all_dataset) * 0.8)
    val_set_length = len(all_dataset) - train_set_length
    train_set, val_set = data.random_split(all_dataset,[train_set_length,val_set_length])
    trainloader = torch.utils.data.DataLoader(train_set, batch_size=16,shuffle=True)
    valloader = torch.utils.data.DataLoader(val_set, batch_size=100,shuffle=True)
    train_loss_list = []
    test_loss_list = []
    test_acc_list = []
    bestaccuracy = 0
    #train the model
    model = CNNpolicy(98,7).cuda()
    CEloss = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.5, 0.999))
    m = torch.nn.Softmax(dim=1)
    for epoch in range(100):
        print('epoch:' + str(epoch) + 'begin')
        trainlosstotal = 0
        count = 0
        for state, actiongt in trainloader:
            print(state.shape)
            count += 1
            # print(state.shape)
            #print(actiongt)
            model.zero_grad()
            output = model(state)
            #print(m(output))
            #print(output)
            loss = CEloss(output,actiongt)
            #print(actiongt)
            #print("=========trainloss=====")
            trainlosstotal += loss
            #print(loss)
            loss.backward()
            optimizer.step()
        #torch.save(generator.state_dict(), './weight/aegenerator_epoch_%d.pth' % (epoch + 35))
        print('=============================================================================\n')
        #print(trainlosstotal/count)
        trainl = trainlosstotal/count
        trainl = trainl.item()
        train_loss_list.append(trainl)
        #print(trainl)
        print('epoch:' + str(epoch) + 'end')
        model.eval()


        with torch.no_grad():
            correct1 = 0
            total1 = 0
            totalloss = 0
            counttemp = 0
            for val_state, val_action in valloader:          
                counttemp += 1
                output = model(val_state)
                test_loss = CEloss(output, val_action)
                totalloss += test_loss
                _, predicted = torch.max(output.data, 1)
                total1 += val_action.size(0)
                correct1 += (predicted == val_action).sum().item()    
            model.train()
           
            testl = totalloss/counttemp
            testl = testl.item()
            #print(testl)
            test_loss_list.append(testl)
            testc = correct1/total1
            if testc > bestaccuracy:
                torch.save(model.state_dict(), './pretrained2/7x7.pth')
                bestaccuracy = testc
                print('model saved')
                print(epoch)

            #print(testc)
            test_acc_list.append(testc)
            
    torch.save(model.state_dict(), './pretrained2/7x7.pth')
    #print(train_loss_list)
    #print(test_loss_list)
    #print(test_acc_list)
#train()
#calscale()

