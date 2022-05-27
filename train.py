from Module.VGG import VggNet, MyData
from torch.utils.data import DataLoader
import torch
from torch.utils.tensorboard import SummaryWriter
import os
import shutil

if __name__ == '__main__':
    # 加载模型
    mod = VggNet()
    # 当不存在模型时, 保存模型
    if not os.path.isfile('./VGG16.pth'):
        torch.save(mod.state_dict(), 'VGG16.pth')
    mod.load_state_dict(torch.load('./VGG16.pth'))
    if torch.cuda.is_available():
        vgg_net = mod.cuda()

    # 初始化数据集
    data_set = MyData('./data', '00')
    for i in range(1, 10):
        data_set += MyData('./data', '0'+str(i))
    for i in range(10, 20):
        data_set += MyData('./data', str(i))

    # 加载数据集加载器
    data_load = DataLoader(dataset=data_set, batch_size=128, shuffle=True)

    # 损失函数和优化函数
    loss_function = torch.nn.CrossEntropyLoss()
    # 要使用Adam, 同时学习率调低!
    param_optim = torch.optim.Adam(mod.parameters(), 4e-5)
    if torch.cuda.is_available():
        loss_function = loss_function.cuda()

    # 当日志存在时, 删除原先日志
    if os.path.isdir('./logs'):
        shutil.rmtree('./logs')
    writer = SummaryWriter('logs')

    for i in range(1800):
        s = 0
        print(i, 'start!')
        for datas, labels in data_load:
            if torch.cuda.is_available():
                datas = datas.cuda()
                labels = labels.cuda()
            param_optim.zero_grad()
            outputs = mod(datas)
            loss_val = loss_function(outputs, labels)
            s += loss_val
            loss_val.backward()
            param_optim.step()
        print('loss:', s)
        if i % 10 == 0:
            writer.add_scalar('loss', s, i//10)
            print('Saving model, please do not break!')
            torch.save(mod.state_dict(), 'VGG16.pth')
            print('Saving model successfully!')

    writer.close()
    print('trained successfully!')
