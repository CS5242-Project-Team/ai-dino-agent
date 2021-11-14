import torch
import torch.nn as nn
import torch.nn.functional as F

#################################### MLP ##############################################
class MLP(nn.Module):
    '''
      Multilayer Perceptron.
    '''

    def __init__(self, ):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Flatten(),
            # nn.Linear(255 * 255 * 3, 64),
            nn.Linear(255 * 255 * 1, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        '''Forward pass'''
        return self.layers(x)
#######################################################################################
#################################### CNN ##############################################
class LeNet5_convnet(nn.Module):
    def __init__(self):
        super(LeNet5_convnet, self).__init__()

        # CL1:   30 x 30  -->    50 x 28 x 28
        self.conv1 = nn.Conv2d(1, 50, kernel_size=3, padding=0)

        # MP1: 50 x 28 x 28 -->    50 x 14 x 14
        self.pool1 = nn.MaxPool2d(2, 2)

        # CL2:   50 x 14 x 14  -->    100 x 14 x 14
        self.conv2 = nn.Conv2d(50, 100, kernel_size=3, padding=1)

        # MP2: 100 x 14 x 14 -->    100 x 7 x 7
        self.pool2 = nn.MaxPool2d(2, 2)

        # LL1:   100 x 7 x 7 = 4900 -->  100
        self.linear1 = nn.Linear(4900, 100)

        # LL2:   100  -->  2
        self.linear2 = nn.Linear(100, 2)

    def forward(self, x):
        # CL1:   30 x 30  -->    50 x 28 x 28
        x = self.conv1(x)
        x = F.relu(x)

        # MP1: 50 x 28 x 28 -->    50 x 14 x 14
        x = self.pool1(x)

        # CL2:   50 x 14 x 14  -->    100 x 14 x 14
        x = self.conv2(x)
        x = F.relu(x)

        # MP2: 100 x 14 x 14 -->    100 x 7 x 7
        x = self.pool2(x)

        # LL1:   100 x 7 x 7 = 4900  -->  100
        x = x.view(-1, 4900)
        x = self.linear1(x)
        x = F.relu(x)

        # LL2:   4900  -->  2
        x = self.linear2(x)

        return x


class VGG_convnet(nn.Module):

    def __init__(self):
        super(VGG_convnet, self).__init__()

        # block 1:         1 x 32 x 32 --> 64 x 16 x 16
        self.conv1a = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        self.conv1b = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)

        # block 2:         64 x 16 x 16 --> 128 x 8 x 8
        self.conv2a = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv2b = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(2, 2)

        # block 3:         128 x 8 x 8 --> 256 x 4 x 4
        self.conv3a = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv3b = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(2, 2)

        # block 4:          256 x 4 x 4 --> 512 x 2 x 2
        self.conv4a = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.pool4 = nn.MaxPool2d(2, 2)

        # linear layers:   512 x 2 x 2 --> 2048 --> 4096 --> 4096 --> 2
        self.linear1 = nn.Linear(2048, 4096)
        self.linear2 = nn.Linear(4096, 4096)
        self.linear3 = nn.Linear(4096, 2)

    def forward(self, x):
        # block 1:         3 x 32 x 32 --> 64 x 16 x 16
        x = self.conv1a(x)
        x = F.relu(x)
        x = self.conv1b(x)
        x = F.relu(x)
        x = self.pool1(x)

        # block 2:         64 x 16 x 16 --> 128 x 8 x 8
        x = self.conv2a(x)
        x = F.relu(x)
        x = self.conv2b(x)
        x = F.relu(x)
        x = self.pool2(x)

        # block 3:         128 x 8 x 8 --> 256 x 4 x 4
        x = self.conv3a(x)
        x = F.relu(x)
        x = self.conv3b(x)
        x = F.relu(x)
        x = self.pool3(x)

        # block 4:          256 x 4 x 4 --> 512 x 2 x 2
        x = self.conv4a(x)
        x = F.relu(x)
        x = self.pool4(x)

        # linear layers:   512 x 2 x 2 --> 2048 --> 4096 --> 4096 --> 2
        x = x.view(-1, 2048)
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        x = F.relu(x)
        x = self.linear3(x)

        return x


class Apple(nn.Module):

    def __init__(self):
        super(Apple, self).__init__()

        # CL1:   102 x 102  -->    50 x 100 x 100
        self.conv1 = nn.Conv2d(1, 50, kernel_size=3, padding=0)

        # MP1: 50 x 100 x 100 -->    50 x 50 x 50
        self.pool1 = nn.MaxPool2d(2, 2)

        # CL2:   50 x 50 x 50  -->    100 x 50 x 50
        self.conv2 = nn.Conv2d(50, 100, kernel_size=3, padding=1)

        # MP2: 100 x 50 x 50 -->    100 x 25 x 25
        self.pool2 = nn.MaxPool2d(2, 2)

        # LL1:   100 x 25 x 25 = 62500 -->  100
        self.linear1 = nn.Linear(100 * 25 * 25, 100)

        # LL2:   100  -->  2
        self.linear2 = nn.Linear(100, 2)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool2(x)

        x = x.view(-1, 100 * 25 * 25)
        x = self.linear1(x)
        x = F.relu(x)

        x = self.linear2(x)

        return x


class Banana(nn.Module):

    def __init__(self):
        super(Banana, self).__init__()

        # CL1:   51 x 51  -->    100 x 50 x 50
        self.conv1 = nn.Conv2d(1, 100, kernel_size=2, padding=0)

        # MP1: 100 x 50 x 50 -->    100 x 25 x 25
        self.pool1 = nn.MaxPool2d(2, 2)

        # CL2:   100 x 25 x 25  -->    200 x 26 x 26
        self.conv2 = nn.Conv2d(100, 200, kernel_size=2, padding=1)

        # MP2: 200 x 26 x 26 -->    200 x 13 x 13
        self.pool2 = nn.MaxPool2d(2, 2)

        # LL1:   200 x 13 x 13  -->  1000
        self.linear1 = nn.Linear(200 * 13 * 13, 1000)

        # LL2:   1000  -->  2
        self.linear2 = nn.Linear(1000, 2)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool2(x)

        x = x.view(-1, 200 * 13 * 13)
        x = self.linear1(x)
        x = F.relu(x)

        x = self.linear2(x)

        return x
#######################################################################################
#################################### RNN ##############################################
class VanillaRNN(nn.Module):
    def __init__(self, input_size):
        super(VanillaRNN, self).__init__()
        self.layers = 1
        self.input_size = input_size
        self.layer1 = nn.RNN(input_size, input_size, self.layers, batch_first=True)
        self.layer2 = nn.Linear(input_size, 2)

    def forward(self, x, h_init):
        h_seq, h_final = self.layer1(x, h_init)
        score_seq = self.layer2(h_seq)
        score_seq = score_seq[:, -1]
        return score_seq, h_final
