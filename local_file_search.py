import json
import os
import re
import shutil, subprocess

import setting as st


# 绝对路径拆分成歌名和作者
def splite_filename(list: list) -> list:
    final_list = []
    for x in list:
        try:
            r = re.findall(re.compile(r'(.*)[\\/](.*)\.(.*)'), x)[0][1]
            l: list = r.split('-')
            if len(l) == 1:
                final_list.append([l[0], 'NULL'])
            else:
                if len(l) > 2:
                    final_list.append([l.pop(0), '-'.join(l)])
                else:
                    final_list.append(l)
        except:
            print(x)
    return final_list


# 删除路径下的所有文件
def delete_path(path: str):
    for x in os.listdir(path):
        a = os.path.join(path, x)
        if not os.path.isfile(a):
            delete_path(a)
            os.rmdir(a)
        else:
            os.remove(a)


# 删除路径下的文件
def delete_file(filename: str):
    try:
        pa = os.path.split(filename)
        for x in os.listdir(pa[0]):
            if x == pa[1]:
                os.remove(os.path.join(pa[0], x))
                return True
    except:
        print(filename)
        return False


# 查找文件类型
def search_file(dirname: str, filter=None) -> list:
    if filter is None:
        filter = st.filters
    dir = os.walk(dirname)
    file_list = []
    for x, y, z in dir:  # 当前主目录 当前主目录下的所有目录 当前主目录下的所有文件
        for n in z:
            if os.path.splitext(n)[1] in filter:
                file_list.append(os.path.join(x, n))
    return file_list


# 寻找歌单文件
def find_gd():
    gd_list = os.listdir(st.path_song)
    filename_list = []
    for x in gd_list:  # 当前主目录 当前主目录下的所有目录 当前主目录下的所有文件
        filename_list.append(os.path.splitext(x)[0])
    return filename_list


# 查找具体文件
def search_one(filename: str) -> list:
    file_list = []
    for i in range(65, 91):
        vol = chr(i) + ':/'
        if os.path.isdir(vol):
            dir = os.walk(vol)
            for x, y, z in dir:  # 当前主目录 当前主目录下的所有目录 当前主目录下的所有文件
                for n in z:
                    if os.path.splitext(n)[1] == os.path.splitext(filename)[1] and os.path.splitext(filename)[0] in \
                            os.path.splitext(n)[0]:
                        file_list.append(os.path.join(x, n))
    return file_list


# 移动文件
def move_file(filename, disdir):
    shutil.move(filename, disdir)


# 判断文件是否存在
def judge_file(filename: str, path: str):  # 与后缀名无关
    file_list = os.listdir(path=path)
    for x in file_list:
        if filename in x:
            return os.path.join(path, x)
    return False


# 写入json文件
def write_json(filename, test: dict or list, issong: bool = False):  # 不用带后缀名
    if issong:
        filename = st.path_song + '/' + filename + '.json'
    else:
        filename = st.path_json + '/' + filename + '.json'
    with open(filename.replace('|', ''), 'w', encoding='utf-8') as f:
        json.dump(test, f)


# 读取json文件
def read_json(filename, issong: bool = False) -> list:  # 不用带后缀名
    if issong:
        filename = st.path_song + '/' + filename + '.json'
    else:
        filename = st.path_json + '/' + filename + '.json'
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


# ffmpeg转码音频文件
def trans_vedio(filename, filter='.mp3'):
    jmexe = st.conf.get('path_section', 'jmexe')
    p = subprocess.Popen('%s -i \"%s\" \"%s\"' % (jmexe, filename, os.path.splitext(filename)[0] + filter), shell=True)
    p.wait()
    if p.returncode == 0:
        delete_file(filename)
        st.set_confi('path_section', 'jmexe', jmexe)
        return os.path.splitext(filename)[0] + filter
    else:
        st.set_confi('path_section', 'jmexe', 'None')
        return False
