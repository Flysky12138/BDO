from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock
from requests import get, head
import os
import sys
import time
import ctypes
lock = Lock()


class Downloader():
    def __init__(self, url, nums, file):
        self.url = url
        self.num = nums
        self.name = file
        r = head(self.url)
        # 若资源显示302,则迭代找寻源文件
        while r.status_code == 302:
            self.url = r.headers['Location']
            print("该url已重定向至{}".format(self.url))
            r = head(self.url)
        self.size = int(r.headers['Content-Length'])

    def down(self, start, end):
        headers = {'Range': 'bytes={}-{}'.format(start, end)}
        # stream = True 下载的数据不会保存在内存中
        r = get(self.url, headers=headers, stream=True)
        # 写入文件对应位置,加入文件锁
        lock.acquire()
        with open(self.name, "rb+") as fp:
            fp.seek(start)
            fp.write(r.content)
            # 释放锁
            lock.release()

    def run(self):
        if os.path.exists(self.name):
            if os.path.getsize(self.name) == self.size:
                print('本地文件和远端文件一样，无需再次下载！')
                time.sleep(3)
                return
            else:
                # 备份
                bakfilepath = dir + "\\languagedata_en.loc.bak"
                if os.path.exists(bakfilepath):
                    os.remove(bakfilepath)
                os.rename(self.name, bakfilepath)
                print('备份文件  [ ' + bakfilepath + ' ]')
        print('开始下载  [ Size: %s M ] [ %s ]' %
              (format(self.size/1024000, '.2f'), self.url))
        time_start = time.time()
        # 创建一个和要下载文件一样大小的文件
        fp = open(self.name, "wb")
        fp.truncate(self.size)
        fp.close()
        # 启动多线程写文件
        part = self.size // self.num
        pool = ThreadPoolExecutor(max_workers=self.num)
        futures = []
        for i in range(self.num):
            start = part * i
            # 最后一块
            if i == self.num - 1:
                end = self.size - 1
            else:
                end = start + part - 1
            futures.append(pool.submit(self.down, start, end))
        wait(futures)
        time_end = time.time()
        print('下载完成  [ Time: %s S ]  [ %s ]' %
              (format(time_end-time_start, '.2f'), self.name))
        time.sleep(3)


# 窗口标题
ctypes.windll.kernel32.SetConsoleTitleW("Made by Flysky")
# 黑沙地址
dir = os.getcwd()
# 仓库
print('https://github.com/Flysky12138/BDO\n')
# 下载loc文件
Downloader('http://dn.blackdesert.com.tw/UploadData/ads/languagedata_tw.loc',
           16, dir + "\\languagedata_en.loc").run()
# 启动黑沙
gamepath = "\"" + os.path.dirname(dir) + \
    "\\Black Desert Online Steam Launcher.exe\""
if sys.argv[len(sys.argv) - 1] == "-s":
    os.system(gamepath)
