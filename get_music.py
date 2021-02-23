import base64
import codecs
import json
import random
import re
import time
from urllib.parse import urlencode as uc

import requests
from Crypto.Cipher import AES

import setting as st

url = "https://music.liuzhijin.cn/"
heard = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
}
type_llist = ['netease', 'qq', 'kugou', 'xiami']


def find_type(link) -> str:
    for x in st.filters:
        if x in link:
            return x
    return None


def temp_song(filaname, url: list):
    if url[0] is not None:
        re = requests.get(url[0], headers=heard)
        s = find_type(re.url)
        if s is None:
            return False
        newfile_no_encoding(st.path_temp + '\\' + filaname + s, 'wb', re.content)
        if url[1] is not None:
            if 'http' in url[1]:
                re = requests.get(url[1], headers=heard)
                newfile(st.path_temp + '\\' + filaname + '歌词.lrc', 'w',
                        re.text.encode('UTF-8').decode('unicode_escape'), 'utf-8')
            else:
                newfile(st.path_temp + '\\' + filaname + '歌词.lrc', 'w', url[1], 'utf-8')
        return [st.path_temp + '\\' + filaname + s, st.path_temp + '\\' + filaname + '歌词.lrc']
    else:
        return False


def down_song(filaname, url: list):
    if url[0] is not None:
        re = requests.get(url[0], headers=heard)
        s = find_type(re.url)
        if s is None:
            return False
        newfile_no_encoding(st.path + '\\' + filaname + s, 'wb', re.content)
        if url[1] is not None:
            if 'http' in url[1]:
                re = requests.get(url[1], headers=heard)
                newfile(st.path + '\\' + filaname + '歌词.lrc', 'w', re.text.encode('UTF-8').decode('unicode_escape'),
                        'utf-8')
            else:
                newfile(st.path + '\\' + filaname + '歌词.lrc', 'w', url[1], 'utf-8')
        newfile(st.path_txt, 'a',
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : 下载 " + filaname + '\n', 'UTF-8')
        return True
    else:
        return False


def newfile(path_, mode_, text, encoding_):
    f = open(path_, mode=mode_, encoding=encoding_)
    f.write(text)
    f.close()


def newfile_no_encoding(path_, mode_, text):
    f = open(path_, mode=mode_)
    f.write(text)
    f.close()


def get_pix(url):
    r = requests.get(url, headers=heard)
    newfile_no_encoding(st.path_temp + '\\temp_pix.jpg', 'wb', r.content)


# 带了"
def findit(p, t):
    pp = re.compile(r'\"%s\":(.*?),' % p)
    r = re.findall(pp, t)
    return r


# 直接使用
def judgeurl(url):
    if 'uid' in url:
        kgperson(url)
    else:
        kgsong(url)


def kgsong(kgurl):
    # "singer_name":"Taylor Swift","song_name":"Begin Again",
    r = requests.get(kgurl, headers=heard)
    t = r.text.encode('gbk', 'ignore').decode('gbk')
    p = re.compile(r'<script type=\'text/javascript\' >(.*?)</script>')
    g = re.findall(p, t)[0]
    rr = findit('playurl', g)
    name = findit('nick', g)[0]
    song_name = findit('song_name', g)[0]
    if len(rr) > 0:
        k = requests.get(rr[0].replace('\"', ''), headers=heard)
        if '.m4a' in k.url:
            with open('%s\\%s-%s.m4a' % (st.path, song_name.replace('\"', ''), name.replace('\"', '')), 'wb') as f:
                f.write(k.content)
            return True
    return False


def kgperson(url):
    r = requests.get(url, headers=heard)
    time.sleep(0.5)
    t = r.text.encode('gbk', 'ignore').decode('gbk')
    p = re.compile(r'\"ugclist\":\[(.*?)\]')
    g = re.findall(p, t)[0]
    l1 = findit('title', g)
    l2 = findit('shareid', g)
    name = findit('nickname', t)[0].replace('\"', '')
    for i in range(0, len(l1)):
        k = requests.get(url='http://cgi.kg.qq.com/fcgi-bin/fcg_get_play_url?shareid=%s' % l2[i].replace('\"', ''),
                         headers=heard)
        if '.m4a' in k.url:
            with open('%s\\%s-%s.m4a' % (st.path, l1[i].replace('\"', ''), name), 'wb')as f:
                f.write(k.content)
            time.sleep(0.5)
    return True


class bs:
    def __init__(self, text):
        self.text = text

    def select(self, tag, classname) -> list[object]:
        p = re.compile(r'<%s class=\"%s\">(.*?)</%s>' % (tag, classname, tag))
        r = re.findall(p, self.text)
        l = []
        for x in r:
            l.append(bs(x))
        return l

    def select_sx(self, tag, sx) -> list[dict]:
        p = re.compile(r'<%s %s=\"(.*?)\">(.*?)</%s>' % (tag, sx, tag))
        r = re.findall(p, self.text)
        l = []
        for x in r:
            d = {
                'sx': x[0],
                'text': x[1]
            }
            l.append(d)
        return l


class MUSIC163:
    def __init__(self):
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.exponent = "010001"
        self.nonce = "0CoJUm6Qyw8W8jud"
        self.login_url = 'https://music.163.com/weapi/user/playlist'
        self.s = requests.session()
        self.playlist = []
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'origin': 'https://music.163.com',
            'referer': 'https://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
        }

    def get_random_str(self, n):
        random_str = ''
        character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for i in range(n):
            j = random.randint(0, len(character) - 1)
            random_str += character[j]
        return random_str

    def get_encText(self, text, key):
        pad = 16 - len(text) % 16
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text + str(pad * chr(pad))
        iv = '0102030405060708'
        c = AES.new(key=bytes(key, encoding='utf-8'), mode=AES.MODE_CBC, iv=bytes(iv, encoding='utf-8'))
        f = c.encrypt(bytes(text, encoding='utf8'))
        return base64.b64encode(f).decode('utf8')

    def get_encSecKey(self, message):
        modulus = int(self.modulus, 16)
        exponent = int(self.exponent, 16)
        message = int(codecs.encode(message[::-1].encode('utf-8'), 'hex_codec'), 16)
        key = pow(message, exponent, modulus)
        return '{:x}'.format(key).zfill(256)

    def data(self, message):
        random_str = self.get_random_str(16)
        encText = self.get_encText(text=message, key=self.nonce)
        encText = self.get_encText(encText, random_str)
        encSecKey = self.get_encSecKey(random_str)
        return {
            "params": encText,
            "encSecKey": encSecKey
        }

    def get_message(self):
        message = {
            "csrf_token": self.csrf,
            "limit": "36",
            "offset": "0",
            "total": "true",
            "uid": self.uid,
            "wordwrap": "7"
        }
        return json.dumps(message)

    def login(self, need):
        self.playlist.clear()
        p1 = re.compile(r'__csrf=(.*?);')
        p2 = re.compile(r'MUSIC_U=(.*?);')
        p3 = re.compile(r'uid=(.*?);')
        self.csrf = re.findall(p1, need)[0]
        self.music_u = re.findall(p2, need)[0]
        self.uid = re.findall(p3, need)[0]
        self.headers['cookie'] = '__csrf=%s;MUSIC_U=%s' % (self.csrf, self.music_u)
        message = self.get_message()
        data = self.data(message)
        response = self.s.post(self.login_url, headers=self.headers, params={'csrf_token': self.csrf}, data=data)
        if response.json()['code'] == 200:
            data = response.json()
            l = data['playlist']
            for x in l:
                self.playlist.append([x['name'], x['id'], x['trackCount'], x['subscribed']])
        else:
            print('错误')


class handle_music:
    def __init__(self):
        self.mes_list = []  # [x['title'], x['author'], x['url'], x['lrc'],x['pic']]
        self.hearder = {
            'authority': 'music.liuzhijin.cn',
            'method': 'POST',
            'path': '/',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://music.liuzhijin.cn',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.song_name = None
        self.singer = None
        self.curtype = None
        self.page = 1
        self.data = {}
        self.wyy = MUSIC163()

    def reset(self, type_index, song_name):
        self.song_name = song_name
        self.mes_list.clear()
        self.curtype = type_llist[type_index]
        self.page = 1
        self.data = {
            'input': self.song_name,
            'filter': 'name',
            'type': self.curtype,
            'page': str(self.page)
        }
        self.hearder['cookie'] = 'Hm_lvt_2f84312e8a038aea180d43256cb0aa7c = 1609057802, 1611553995;' \
                                 'Hm_lvt_50027a9c88cdde04a70f5272a88a10fa = 1613028690, 1613043636, 1613138013, %s;' \
                                 'Hm_lpvt_50027a9c88cdde04a70f5272a88a10fa = %s' % (
                                     str(int(time.time()) - 2000), str(int(time.time())))
        result = self.get_song_list()
        return result

    def reset_2(self, type_index, id_list):
        self.mes_list.clear()
        self.curtype = type_llist[type_index]
        self.page = 1
        self.data = {
            'input': '0',
            'filter': 'id',
            'type': self.curtype,
            'page': str(self.page)
        }
        for x in id_list:
            self.data['input'] = x
            self.hearder['cookie'] = 'Hm_lvt_2f84312e8a038aea180d43256cb0aa7c = 1609057802, 1611553995;' \
                                     'Hm_lvt_50027a9c88cdde04a70f5272a88a10fa = 1613028690, 1613043636, 1613138013, %s;' \
                                     'Hm_lpvt_50027a9c88cdde04a70f5272a88a10fa = %s' % (
                                         str(int(time.time()) - 2000), str(int(time.time())))
            time.sleep(1)
            result = self.get_song_list()
            if result is not True:
                print(result)
        return

    def hand_more(self):
        self.page += 1
        self.data['page'] = str(self.page)
        result = self.get_song_list()
        return result

    def get_song_list(self):  # ['index','title','author','url','lrc' ,'pic']
        try:
            response = requests.post(url, headers=self.hearder, data=self.data, timeout=5)
            if response.status_code == 200:
                text = response.json()
                for x in text['data']:
                    self.mes_list.append([x['title'], x['author'], x['url'], x['lrc'], x['pic']])
                return True
            else:
                return '连接失败'
        except requests.exceptions.ConnectTimeout:
            return '连接超时'

    def down_song(self, index):
        r = requests.get(url=self.mes_list[index][2], headers=heard)
        s = find_type(r.url)
        if s is None:
            return False
        else:
            filename_song = st.path + '\\' + self.mes_list[index][0] + '-' + self.mes_list[index][1] + s
            filename_lrc = st.path + '\\' + self.mes_list[index][0] + '-' + self.mes_list[index][1] + '歌词.lrc'
            newfile(filename_lrc, 'w+', self.mes_list[index][3], encoding_='utf-8')
            newfile_no_encoding(filename_song, 'wb', r.content)
            if 'http' in self.mes_list[index][3]:
                rr = requests.get(self.mes_list[index][3], headers=heard)
                newfile(filename_lrc, 'w', rr.text.encode('UTF-8').decode('unicode_escape'), 'utf-8')
            else:
                newfile(filename_lrc, 'w', self.mes_list[index][3], 'utf-8')
            newfile(st.path_txt, 'a',
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : 下载 " + self.mes_list[index][
                        0] + '-' + self.mes_list[index][1] + '\n', 'utf-8')
            return [filename_song, filename_lrc]

    # 网易云歌单解析歌单id
    def parse(self, link) -> str:  # https://music.163.com/#/playlist?id=2829816518
        # 分享雪域哦弄创建的歌单「english」: http://music.163.com/playlist/3196628516/1721114513/?userid=1721114513 (来自@网易云音乐)
        # https://y.qq.com/n/yqq/playlist/2041213723.html#stat=y_new.index.playlist.pic
        p = re.compile(r'playlist/(\d*)[/\.]')
        t = re.findall(p, link)[0]
        return t

    # 获得歌单的歌曲id列表并请求
    def hand_id(self, link):
        if 'music.163.com' in link:
            if '分享' in link:
                url = 'https://music.163.com/playlist'
                para = {
                    'id': self.parse(link)
                }
                r = requests.get(url=url, headers=self.wyy.headers, params=para)
            else:
                r = requests.get(url=link.replace('/#/', '/'), headers=self.wyy.headers)
            data = r.text.encode('GBK', 'ignore').decode('GBK')
            soup = bs(data)
            d = soup.select('ul', 'f-hide')[0]
            dd = d.select_sx('a', 'href')
            l = []
            for x in dd:
                y = re.findall(re.compile(r'id=(\d*)'), x['sx'])[0]
                l.append(y)
            self.reset_2(0, l)
        elif 'y.qq.com' in link:
            l = self.qq_list(self.parse(link))
            self.reset_2(1, l[1])
        ll = self.mes_list.copy()
        self.mes_list.clear()
        for x in ll:
            self.mes_list.append({
                'title': x[0],
                'author': x[1],
                'url': x[2],
                'lrc_content': x[3],
                'pix': x[4],
            })
        if 'music.163.com' in link:
            return soup.select('h2', 'f-ff2 f-brk')[0].text
        elif 'y.qq.com' in link:
            return l[0]
        else:
            return False

    # 解析QQ音乐歌单id
    def qq_list(self, id):
        url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg'
        para = {
            "type": '1',
            "json": '1',
            "utf8": '1',
            "onlysong": '0',
            "new_format": '1',
            "disstid": id,
            "g_tk_new_20200303": '5381',
            "g_tk": '5381',
            "loginUin": '0',
            "hostUin": '0',
            "format": 'json',
            "inCharset": 'utf8',
            "outCharset": 'utf-8',
            "notice": '0',
            "platform": 'yqq.json',
            "needNewCode": '0'
        }
        heard = {
            'origin': 'https://y.qq.com',
            'referer': 'https://y.qq.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
        }
        r = requests.get(url=url, headers=heard, params=para)
        data = r.json()
        list1 = data['cdlist'][0]
        name = list1['dissname']
        songlist = list1['songlist']
        idlist = []
        for xx in songlist:
            idlist.append(xx['mid'])
        return [name, idlist]


class handle_vip:
    def __init__(self):
        self.list = []
        self.page = 1
        self.url = 'https://myhkw.cn/api/web'
        self.tt = [{'source': 'netease', 'type': 'wy'}, {'source': 'tencent', 'type': 'qq'},
                   {'source': 'kugou', 'type': 'kg'}, {'source': 'migu', 'type': 'mg'}, ]

    def jxsong(self, index, name):
        self.list.clear()
        self.page = 1
        self.source = self.tt[index]['source']
        self.type1 = self.tt[index]['type']
        self.para = {
            'types': 'search',
            'count': '20',
            'source': self.source,
            'pages': str(self.page),
            'name': name,
            '_': str(int(time.time()))
        }
        try:
            r = requests.get(self.url, headers=heard, params=self.para, timeout=5)
            if r.status_code == 200:
                self.parse_list(r.json())
                return True
            else:
                return '连接失败'
        except requests.exceptions.ConnectTimeout:
            return '连接超时'

    def parse_list(self, l: list):
        for x in l:
            ll = [x.pop('name'), ','.join(x.pop('artist')), 'https://myhkw.cn/api/musicUrl?' + uc({
                'songId': x['id'],
                'type': self.type1,
                'id': '155782152289'
            }), 'https://myhkw.cn/api/musicLyric?' + uc({
                'type': self.type1,
                'songId': x['id'],
                'id': 'myhkwebplayer',
                '_': str(int(time.time()))
            }), 'https://myhkw.cn/api/musicPic?' + uc({
                'picId': x['pic_id'],
                'type': self.type1,
                'size': 'big'
            })]
            self.list.append(ll)

    def handle_more(self):
        self.page += 1
        self.para['pages'] = str(self.page)
        r = requests.get(self.url, headers=heard, params=self.para)
        self.parse_list(r.json())
