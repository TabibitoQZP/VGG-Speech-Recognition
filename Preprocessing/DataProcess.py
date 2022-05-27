import os
import shutil

import torch
import librosa
import matplotlib.pyplot as plt
import numpy as np
import shutil

pad_len = 50000


def InitDir(root_path):
    """
    将wav文件转化成mel频谱, 并保存到root_path内, 做好标签
    :param root_path: 数据根目录
    :return: None
    """
    if os.path.isdir(root_path):
        shutil.rmtree(root_path)
    os.mkdir(root_path)
    for i in range(10):
        dir_name = '0' + str(i)
        tmp = os.path.join(root_path, dir_name)
        os.mkdir(tmp)
        dir_name = '1' + str(i)
        tmp = os.path.join(root_path, dir_name)
        os.mkdir(tmp)


def ProducePTH(data_path):
    global pad_len
    wave_data, sample_rate = librosa.load(data_path, sr=8000)
    wave_len = len(wave_data)
    if wave_len > pad_len:
        return False, 0
    left_len = (pad_len-wave_len)//2
    right_len = pad_len-wave_len-left_len
    pad_data = np.pad(wave_data, (left_len, right_len), 'constant', constant_values=(0, 0))
    feat = librosa.stft(pad_data, hop_length=512, n_fft=1024)
    feat = np.abs(feat)**2
    # mel = librosa.feature.melspectrogram(y = pad_data, sr=8000, n_mels=128, n_fft=1024, hop_length=512)
    mel = librosa.feature.melspectrogram(S=feat, sr=8000, n_mels=128)
    # plt.pcolor(mel)
    # plt.show()
    # 这里注意, mel谱是二维的, 但实际上要变成三维的
    mel = mel.reshape((1, mel.shape[0], mel.shape[1]))
    mel_pth = torch.from_numpy(mel)
    return True, mel_pth
    # print(len(pad_data))


def SaveAsPTH(data_path, root_path):
    dirs = []
    for i in range(10):
        dirs.append('0'+str(i))
        dirs.append('1'+str(i))
    dirs.sort()
    for i in dirs:
        data_dir = os.path.join(data_path, i)
        root_dir = os.path.join(root_path, i)
        datas = os.listdir(data_dir)
        for j in datas:
            tmp = os.path.join(data_dir, j)
            if_save, tmp_pth = ProducePTH(tmp)
            if if_save:
                file_path, full_file_name = os.path.split(tmp)
                file_name, ext = os.path.splitext(full_file_name)
                change_name = file_name+'.pth'
                change_path = os.path.join(root_dir, change_name)
                torch.save(tmp_pth, change_path)


if __name__ == '__main__':
    InitDir('../data')
    SaveAsPTH('./original_data', '../data')

