import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt
from ghost_net import ghost_net
plt.rcParams['figure.dpi']=50 
epochs = 10
batch_size = 200

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
 
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True)
 
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


#net = Ghost_ResNet.resnet56()
net = ghost_net(width_mult=1.0)


criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.0001)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)
plt_loss = []

def show_loss(plt_loss):
    plt.plot(range(len(plt_loss)),plt_loss)
    #plt.xlim((0,100)
    plt.ylim((0,10))
    plt.show()

def train(resume):
    if resume == True:
        net.load_state_dict(torch.load("ghostnet.weights"))
    for epoch in range(epochs):
        print("epoch:"+str(epoch+1))
        for i, data in enumerate(
                torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                        shuffle=False), 0):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)
        
            optimizer.zero_grad()
        
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            plt_loss.append(loss.item())
            print('[%d, %5d] loss: %.4f' %(epoch + 1, (i+1)*batch_size, loss.item()))
        show_loss(plt_loss)
        torch.save(net.state_dict(), 'ghostnet'+str(epoch+1)+'.weights')
    torch.save(net.state_dict(), 'ghostnet.weights')
    
train(resume=True)
#test()
