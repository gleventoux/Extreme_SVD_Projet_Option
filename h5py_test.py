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


with h5py.File('./matrix/random1Go.hdf5', 'r') as f:
    # 打印文件结构
    print(isinstance(f,h5py.File))
    print_structure(f)
    root_keys = list(f.keys())
    print(root_keys)
    print("Total datasets in root group: ", len([key for key in root_keys if isinstance(f[key], h5py.Dataset)]))
    other_keys = [key for key in root_keys if isinstance(f[key], h5py.Group)]
    for key in other_keys:
        group = f[key]
        print("Total datasets in group '{}': {}".format(key, len([k for k in group.keys() if isinstance(group[k], h5py.Dataset)])))

