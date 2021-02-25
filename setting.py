import configparser as cf
import os
conf_path = 'resource/文件/setting.cfg'
conf = cf.ConfigParser()
conf.read(conf_path)
# pyinstaller -w Yuye.py Main.py get_music.py local_file_search.py lrc.py setting.py -i resource\图片\Yuyeicon.ico

def set_confi(sectionname, optionname, value):
    conf.set(sectionname, optionname, value)
    conf.write(open(conf_path, "w"))


def add_confi(sectionname):
    conf.add_section(sectionname)
    conf.write(open(conf_path, "w"))


path_exe = conf.get('path_section', 'path_exe')
if os.path.exists(conf.get('path_section', 'path')):
    path = conf.get('path_section', 'path')
else:
    path = path_exe+'/music'
    set_confi('path_section', 'path', path)
path_txt = path_exe + '/日志.txt'
path_temp = path_exe + '/temp'
path_json = path_exe + '/json'
path_song = path_json + '/song_list'
filters = conf.get('base', 'filters').split(',')
