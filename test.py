import h5py


def print_structure(item, level=0):
    if isinstance(item, h5py.File):
        print(item.filename)
        print(len(item.keys()))
        for key in item.keys():
            print_structure(item[key], level + 1)
    elif isinstance(item, h5py.Group):
        print(' ' * level + '+', item.name)
        for key in item.keys():
            print_structure(item[key], level + 1)
    elif isinstance(item, h5py.Dataset):
        print(' ' * level + '-', item.name)

# 打开HDF5文件
with h5py.File('./matrix/random1Go.hdf5', 'r') as f:
    # 打印文件结构
    print(isinstance(f,h5py.File))
    print_structure(f)
    
    # 获取根组的名称列表
    root_keys = list(f.keys())
    # 输出根组下的数据集数量
    print("Total datasets in root group: ", len([key for key in root_keys if isinstance(f[key], h5py.Dataset)]))
    # 获取其他组的名称列表
    other_keys = [key for key in root_keys if isinstance(f[key], h5py.Group)]
    # 遍历每个组并输出其中数据集的数量
    for key in other_keys:
        group = f[key]
        print("Total datasets in group '{}': {}".format(key, len([k for k in group.keys() if isinstance(group[k], h5py.Dataset)])))

