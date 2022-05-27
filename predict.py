import torch
from Module.VGG import VggNet
import numpy as np
import os
from Preprocessing.DataProcess import ProducePTH

pad_len = 50000
labels = ['数字', '语音', '语言', '识别', '中国', '忠告', '北京', '背景', '上海', '商行',
          'Speech', 'Speaker', 'Signal', 'Sequence', 'Process', 'Print', 'Project',
          'File', 'Open', 'Close']
total_predict = 0
true_predict = 0
mod = VggNet()
mod.load_state_dict(torch.load('./VGG16.pth', map_location=torch.device('cpu')))


def PredictAll(root_path):
    global mod, true_predict, total_predict
    path_contain = os.listdir(root_path)
    for i in path_contain:
        tmp = os.path.join(root_path, i)
        if os.path.isdir(tmp):
            PredictAll(tmp)
        else:
            file_path, full_file_name = os.path.split(tmp)
            file_name, ext = os.path.splitext(full_file_name)
            if ext == '.wav' or ext == '.dat':
                if_load, data_load = ProducePTH(tmp)
                if if_load:
                    data_load = data_load.reshape(1, data_load.shape[0], data_load.shape[1], data_load.shape[2])
                    class_probability = mod(data_load)
                    class_id = np.argmax(class_probability[0].detach().numpy())
                    if len(file_name.split('_')) != 3:
                        actual_id = int(file_name.split('-')[1])
                    else:
                        actual_id = int(file_name.split('_')[1])
                    if class_id == actual_id:
                        true_predict += 1
                    total_predict += 1


if __name__ == '__main__':
    # PredictAll('./Preprocessing/original_data') # 99%
    # print(mod)
    # do not use the dropout, or the prediction is not sure.
    mod.classifier[3].p = 0
    mod.classifier[6].p = 0
    PredictAll('./MyAudio')  # 77.75%
    print('total predict:', total_predict)
    print('right predict:', true_predict)
    print('rate:', true_predict / total_predict)
