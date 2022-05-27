"""
将原始数据文件夹删除, 并归一到
os          库用于文件和目录的访问和重命名
shutil      库用于移动和删除操作
"""
import os
import shutil


def ChangeFileName(data_path):
    """
    将dat文件统一命名为wav文件
    :param data_path: 数据路径, 将会被递归处理
    :return: None
    """
    path_contain = os.listdir(data_path)
    for i in path_contain:
        tmp = os.path.join(data_path, i)
        if os.path.isdir(tmp):
            # 注意基于函数修改时别忘了递归函数的修改
            ChangeFileName(tmp)
        else:
            file_path, full_file_name = os.path.split(tmp)
            file_name, ext = os.path.splitext(full_file_name)
            if ext == '.dat':
                os.rename(tmp, os.path.join(file_path, file_name + '.wav'))


def MoveToRoot(data_path, root_path):
    """
    将root_path作为根目录, 将data_path内的wav文件全部移动到root_path内, 非wav文件删除
    :param data_path: 需要移动的目录, 这里一般初始递归和root_path是一致的
    :param root_path: 目标目录, 后续递归的使用同一值
    :return: None
    """
    path_contain = os.listdir(data_path)
    for i in path_contain:
        tmp = os.path.join(data_path, i)
        if os.path.isdir(tmp):
            MoveToRoot(tmp, root_path)
        else:
            file_path, full_file_name = os.path.split(tmp)
            file_name, ext = os.path.splitext(full_file_name)
            if ext == '.wav':
                if not os.path.isfile(os.path.join(root_path, i)):
                    shutil.move(tmp, root_path)
            else:
                os.remove(tmp)
    return 0


def ChangeDirFormat(data_path):
    """
    将文件夹归一成/root/课程录音(k)/{datas}的格式
    :param data_path: 数据路径, 会被递归处理
    :return: None
    """
    root_contain = os.listdir(data_path)
    # 假定root下面的就是"课程录音(k)"子目录
    for i in root_contain:
        # tmp1必定是文件夹路径, 根目录下的所有文件一律删除
        tmp1 = os.path.join(data_path, i)
        if not os.path.isdir(tmp1):
            os.remove(tmp1)
            continue
        MoveToRoot(tmp1, tmp1)
        data_contain = os.listdir(tmp1)
        for j in data_contain:
            tmp2 = os.path.join(tmp1, j)
            if os.path.isdir(tmp2):
                # 递归删除目录及其包含的内容
                shutil.rmtree(tmp2)
            else:
                file_path, full_file_name = os.path.split(tmp2)
                file_name, ext = os.path.splitext(full_file_name)
                # 将非wav文件删除
                if ext != '.wav':
                    os.remove(tmp2)


def ChangeIndex(root_path):
    """
    实际观察发现有些人索引是0-19, 有些人索引是1-20, 有人是00-19, 有人是01-20, 需要统一成00-19的格式
    :param root_path: 根目录
    :return: None
    """
    root_contain = os.listdir(root_path)
    for i in root_contain:
        tmp1 = os.path.join(root_path, i)
        # data_contain内部全是wav文件
        data_contain = os.listdir(tmp1)
        index_list = []
        for j in data_contain:
            tmp2 = os.path.join(tmp1, j)
            name_splits = j.split('_')
            # 因为14号数据用'-'分割而不是'_'分割, 数据集会出bug, 春春的杀币
            if len(name_splits) != 3:
                name_splits = j.split('-')
            if len(name_splits) != 3:
                os.remove(tmp2)
            else:
                index_list.append(int(name_splits[1]))
        index_list.sort()
        if index_list[0] == 1 and index_list[-1] == 20:
            for j in data_contain:
                tmp2 = os.path.join(tmp1, j)
                name_splits = j.split('_')
                if len(name_splits) != 3:
                    name_splits = j.split('-')
                data_index = int(name_splits[1]) - 1
                if data_index < 10:
                    new_name = name_splits[0] + '_0' + str(data_index) + '_' + name_splits[2]
                else:
                    new_name = name_splits[0] + '_' + str(data_index) + '_' + name_splits[2]
                os.rename(tmp2, os.path.join(tmp1, new_name))
        else:
            for j in data_contain:
                tmp2 = os.path.join(tmp1, j)
                name_splits = j.split('_')
                if len(name_splits) != 3:
                    name_splits = j.split('-')
                data_index = int(name_splits[1])
                if data_index < 10:
                    new_name = name_splits[0] + '_0' + str(data_index) + '_' + name_splits[2]
                else:
                    new_name = name_splits[0] + '_' + str(data_index) + '_' + name_splits[2]
                os.rename(tmp2, os.path.join(tmp1, new_name))


def InitData(out_path):
    """
    初始化数据文件夹, 倘若有重名, 则递归移除该文件夹及其所有内容
    :param out_path: 需要初始化的文件夹名称以及路径
    :return: None
    """
    if os.path.isdir(out_path):
        shutil.rmtree(out_path)
    os.mkdir(out_path)
    dirs = []
    for i in range(0, 10):
        dirs.append('0' + str(i))
        dirs.append('1' + str(i))
    for i in dirs:
        tmp = os.path.join(out_path, i)
        os.mkdir(tmp)


def MoveOut(root_path, out_path):
    """
    将根目录已经处理好的各个文件全部移动到out_path的00-19文件夹中, 完成原始的数据集分类
    :param root_path: 原始目录文件夹
    :param out_path: 数据集分类文件夹
    :return:
    """
    path_contain = os.listdir(root_path)
    for i in path_contain:
        tmp = os.path.join(root_path, i)
        if os.path.isdir(tmp):
            # 注意基于函数修改时别忘了递归函数的修改
            MoveOut(tmp, out_path)
        else:
            name_splits = i.split('_')
            shutil.copy(tmp, os.path.join(out_path, name_splits[1]))


def FileProcess(data_path, out_path):
    """
    封装上述代码
    :param data_path: 数据路径
    :param out_path: 目标路径
    :return: None
    """
    ChangeFileName(data_path)
    print('成功将dat文件转成wav文件')
    ChangeDirFormat(data_path)
    print('成功修改目录格式!')
    ChangeIndex(data_path)
    print('成功修改数据索引!')
    InitData(out_path)
    print('初始化数据目录!')
    MoveOut(data_path, out_path)
    print('移动分类原始数据!')
    os.system('cls')
    print('数据处理成功!')


if __name__ == '__main__':
    FileProcess('./all', './original_data')
