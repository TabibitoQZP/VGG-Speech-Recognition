import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    # tmp = torch.empty((1, 1, 128, 98))
    # v_net = VggNet()
    # writer = SummaryWriter('logs')
    # writer.add_graph(v_net, tmp)
    # writer.close()
    plt.style.use('ggplot')
    rand_len = 256
    paded = 128
    y = np.random.random(rand_len)-0.5
    x = np.arange(rand_len)
    plt.plot(x, y)
    plt.savefig('./img/original_wave.png', bbox_inches='tight')
    plt.show()
    y_ = np.pad(y, (128, 128), 'constant')
    x_ = np.arange(paded*2 + rand_len)
    plt.plot(x_, y_)
    plt.savefig('./img/padding_wave.png', bbox_inches='tight')
    plt.show()
