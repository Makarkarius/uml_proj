import os


def write_data(dirlist, file_type, data_type, data, flag):
    file = f'{dirlist}/{data_type}.{file_type}'
    if os.path.isfile(file):
        i = 0
        while os.path.isfile(f'{dirlist}/{data_type}{i}'):
            i += 1
        file = f'{dirlist}/{data_type}{i}.{file_type}'
    with open(file, flag) as target:
        target.write(data)
