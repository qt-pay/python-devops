

import os
files = '/etc/ansible/hosts'
file_list = os.listdir(files)
for file in file_list:
    print(os.path.isfile(os.path.join(files, file)))
    print(os.path.join(files, file))
    print(file)