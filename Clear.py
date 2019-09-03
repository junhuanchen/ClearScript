#coding=utf-8

import os,sys
from stat import *

'''
os.walk:
    这个方法返回的是一个三元tupple(dirpath, dirnames, filenames)
    dirpath为起始路径，dirpath是一个string，代表目录的路径。
    dirnames为起始路径下的文件夹，是一个list，包含了dirpath下所有子目录的名字。
    filenames为起始路径下的文件，包含了非目录文件的名字.这些名字不包含路径信息，如果需要得到全路径，需要使用 os.path.join(dirpath, name)。
'''

# 声明欲删除的文件后缀名集合
DelFiles=['pyc', 'tmp', 'map', 'lst', 'sdf', 'log', 'db', 'o', 'd', 'crf']

# 声明欲删除的文件夹名集合
DelFolders=['ipch', 'Debug', 'Release', 'output', 'html', 'rtf', 'latex', 'OBJ', 'Coordinator', 'EndDeviceCollect', 'EndDeviceEB', 'RouterEB']

def PurgeCatalog(path):
    count = 0
    for item in os.listdir(path):
        subpath = os.path.join(path, item)
        mode = os.stat(subpath).st_mode
        if S_ISDIR(mode):
            count += PurgeCatalog(subpath)
        else:
            os.chmod(subpath, S_IREAD|S_IWRITE)
            os.unlink(subpath)
            count += 1
    os.rmdir(path)
    count += 1
    return count
    
def ClearCatalog(path):
    for catalog in os.walk(path):
        print("find files : %s." % catalog[2])
        for file_name in catalog[2]:
            if '.' in file_name: # 判断文件名是否存在后缀
                file_type  = file_name.rsplit('.', 1)[1]
                if file_type in DelFiles:
                    print('file %s deleted.' % (os.path.join(catalog[0], file_name)))
                    os.remove(os.path.join(catalog[0], file_name))
        print("find folders : %s." % catalog[1])
        for file_folder in catalog[1]:
            print("into file_folder %s." % file_folder)
            if file_folder in DelFolders:
                print("file_folder %s deleted." % os.path.join(catalog[0], file_folder))
                print("files %d deleted." % PurgeCatalog(os.path.join(catalog[0], file_folder)))

if __name__ == '__main__':
    #判断命令行参数 # 批处理格式（bat）：python %cd%/Clear.py %cd%
    if len(sys.argv) != 2:
        print( 'please add argv path : %s ' % sys.argv[0]) # %cd%
        sys.exit(1)
    ClearCatalog(sys.argv[1])
