import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
from torch.nn import Conv2d, ReLU, MaxPool2d, Linear, Dropout, Flatten
import os


word_dict = {'00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8, '09': 9,
             '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17, '18': 18, '19': 19}


class VggNet(torch.nn.Module):
    def __init__(self):
        super(VggNet, self).__init__()
        self.features = torch.nn.Sequential(
            Conv2d(1, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False),
            Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False),
            Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False),
            Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False),
            Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)), ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        )
        self.classifier = torch.nn.Sequential(
            Flatten(),
            Linear(in_features=6144, out_features=4096, bias=True),
            ReLU(inplace=True),
            Dropout(p=0.5, inplace=False),
            Linear(in_features=4096, out_features=4096, bias=True),
            ReLU(inplace=True),
            Dropout(p=0.5, inplace=False),
            Linear(in_features=4096, out_features=20, bias=True),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class MyData(Dataset):
    # 注意别抄错, init不是int, 不知道为啥自动补全给补的int... 傻逼
    def __init__(self, root_dir, label_dir):
        # 数据根目录
        self.root_dir = root_dir
        # 标签目录, 本身也可以作为标签使用
        self.label_dir = label_dir
        # 标签目录一般是子目录, 因此要用join得到绝对路径
        self.path = os.path.join(self.root_dir, self.label_dir)
        # 得到数据的相对路径, 这是一个列表, 所有的数据都将在这里, 比如['1.jpg', '2.jpg'], 是同一label下的所有数据
        self.data_path = os.listdir(self.path)

    # __getitem__定义以后, 可以通过class_instance[idx]访问return的数据了
    def __getitem__(self, idx):
        # 获取单个数据, 比如idx=0, 则得到'1.jpg'
        data_name = self.data_path[idx]
        # 获取该单个数据的绝对路径
        data_item_path = os.path.join(self.root_dir, self.label_dir, data_name)
        # 数据处理, 要处理成数组之类的
        data = torch.load(data_item_path)
        # 标签, 一般就是类别相对目录, 需要转为数字, 这样才能进一步转为tensor
        label = word_dict[self.label_dir]
        return data, label

    def __len__(self):
        # 返回数据的数量
        return len(self.data_path)


if __name__ == '__main__':
    nt = torchvision.models.vgg16()
    print(nt)
    mod = VggNet()
    data_set = MyData('../data', '00')
    for i in range(1, 10):
        data_set += MyData('../data', '0'+str(i))
    for i in range(10, 20):
        data_set += MyData('../data', str(i))
    data_load = DataLoader(dataset=data_set, batch_size=10, shuffle=True)
    for datas, labels in data_load:
        print(datas, labels)
        print(datas.shape)
        print(mod(datas))
        break
