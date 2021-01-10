## Made by Flysky NA

##### ❗由于从 `http://dn.blackdesert.com.tw/UploadData/ads/languagedata_tw.loc` 获取到的语言文件版本过低，所以汉化不全。建议从台服客户端中提取语言文件。
<br>

## 使用

说明: `/prestringtable/font/pearl.ttf` 字体文件需自己添加否则界面将乱码(游戏路径下，需自行创建)  

使用: 将exe文件放在游戏里的 ads 目录下(如: `D:\steam\steamapps\common\Black Desert Online\ads` ), 并在每次更新后执行即可

<br>
<br>
<br>

## 自行编译

1、前提：
`python` 环境、并且安装 `requests、pyinstaller` 

``` 
pip install requests
pip install pyinstaller
```

2、打包：
```
pyinstaller -F -i ./BlackDesert.ico ./main.py
``` 
