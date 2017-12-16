> 起因：前两天在公众号上看到一篇文章内容就是爬取王者荣耀的皮肤，但是内容太大概了，如果跟着他做肯定做不出来，所以我打算自己做。



之前接触过爬虫还是几年前爬取豆瓣电台的歌曲，那时候用的C++，json解析还要用第三方库，总之很麻烦。最近接触到了python，深深的感觉这门语言真好。



进入正题：如何爬取王者荣耀的英雄皮肤照片？



分为两步：

1. 找到皮肤图片的地址
2. 下载图片

### 1. 寻找皮肤图片地址

#### 1.1 找到英雄列表

百度“王者荣耀”进入官网，进入https://pvp.qq.com/，按**F12**进入调试界面，然后按**F5**刷新界面，图中标识的**herolist.json**文件就是我们所需要的英雄列表，其中包括英雄编号、英雄名称、英雄类型、皮肤的名称等信息，在文件上右击复制链接http://pvp.qq.com/web201605/js/herolist.json

![英雄列表](E:\__Python\爬虫\下载王者荣耀皮肤\英雄列表.png)

接下来检验一下我们的成果：

``` python
# 代码片段1
import urllib.request
import json
import os

response = urllib.request.urlopen("http://pvp.qq.com/web201605/js/herolist.json")

hero_json = json.loads(response.read())
hero_num = len(hero_json)

print(hero_json)
print("hero_num : " , str(hero_num))
```

以上代码读取英雄列表存入hero_json，并获取英雄数量，运行效果如图所示：

![英雄列表运行结果](E:\__Python\爬虫\下载王者荣耀皮肤\英雄列表运行结果.png)


#### 1.2 找到英雄皮肤地址

点击首页的“游戏资料”标签页，进入新的界面后点击一个英雄头像进入英雄资料界面，此处我们以孙尚香为例：

![游戏资料](E:\__Python\爬虫\下载王者荣耀皮肤\游戏资料.png)

![孙尚香](E:\__Python\爬虫\下载王者荣耀皮肤\孙尚香.png)

同样F12然后F5，将鼠标在孙尚香几个皮肤上依次扫过，来看看调试窗口![孙尚香皮肤](E:\__Python\爬虫\下载王者荣耀皮肤\孙尚香皮肤.png)

可以看到孙尚香的高清皮肤一共6个，同样我们在第一个皮肤上右键复制链接得到：http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/111/111-bigskin-1.jpg，这就是我们梦寐以求的**英雄皮肤链接**。



分析一下这个链接，其中“111”是英雄的编号，最后的“1”是该英雄的皮肤编号。到此位置，浏览器已经没有用了，该得到的信息我们都有了。



### 2. 下载图片

#### 2.1 英雄有几个皮肤

在第一步获取到的**herolist.json**文件中有**“skin_name”**字段，我们只要解析这个字段就可以获取皮肤数量和皮肤名称。测试代码（接代码片段1）如下：

``` python
  # 代码片段2
  hero_name = hero_json[0]['cname']
  skin_names = hero_json[0]['skin_name'].split('|')
  skin_num = len(skin_names)
    
  print('hero_name: ', hero_name)
  print('skin_names :', skin_names)
  print('skin_num: ' + str(skin_num))
```

运行结果如下：

![廉颇](E:\__Python\爬虫\下载王者荣耀皮肤\廉颇.png)

可以看到廉颇一共两个皮肤，皮肤名称分别为：争议轰爆和地狱岩魂。

#### 2.2 下载文件

下载文件用到**urlretrieve**接口，测试代码如下：

``` python
for i in range(hero_num):
  	# 获取皮肤名称列表
    skin_names = hero_json[i]['skin_name'].split('|')
    
    for cnt in range(len(skin_names)):
        save_file_name = 'D:\heroskin\\' + str(hero_json[i]['ename']) + '-' +hero_json[i]['cname']+ '-' +skin_names[cnt] + '.jpg'
        skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(hero_json[i]['ename'])+ '/' +str(hero_json[i]['ename'])+'-bigskin-' + str(cnt+1) +'.jpg'
        urllib.request.urlretrieve(skin_url, save_file_name)

```

来看下结果：

![皮肤](E:\__Python\爬虫\下载王者荣耀皮肤\皮肤.png)

至此224个皮肤全部下载完毕，都是高清图片。





还没有结束，程序有些不完美的地方：

1. 如果路径D:\herolist\不存在，则程序运行失败；
2. 如果中途下载失败，再次运行程序的时候已经下载过的图片还会再下载一次。

解决方案：

1. 检查文件是否存在，如果不存在则创建，代码如下：

   ``` python
   # 文件夹不存在则创建
   save_dir = 'D:\heroskin'
   if not os.path.exists(save_dir):
   	os.mkdir(save_dir)
   ```

2. 检查文件是否存在，如果存在则跳过下载，代码如下：


   ``` python
   if not os.path.exists(save_file_name):
   	urllib.request.urlretrieve(skin_url, save_file_name)
   ```



至此，大功告成，贴一下完整代码：

``` python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 23:12:17 2017

@author: WangQiang
"""
import urllib.request
import json
import os

response = urllib.request.urlopen("http://pvp.qq.com/web201605/js/herolist.json")

hero_json = json.loads(response.read())
hero_num = len(hero_json)

# 文件夹不存在则创建
save_dir = 'D:\heroskin\\'
if not os.path.exists(save_dir):
	os.mkdir(save_dir)
	
for i in range(hero_num):
	# 获取英雄皮肤列表
	skin_names = hero_json[i]['skin_name'].split('|')
	
	for cnt in range(len(skin_names)):
		save_file_name = save_dir + str(hero_json[i]['ename']) + '-' +hero_json[i]['cname']+ '-' +skin_names[cnt] + '.jpg'
		skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(hero_json[i]['ename'])+ '/' +str(hero_json[i]['ename'])+'-bigskin-' + str(cnt+1) +'.jpg'

		if not os.path.exists(save_file_name):
			urllib.request.urlretrieve(skin_url, save_file_name)
```

出去注释和空行，一共16行代码实现了下载王者荣耀所有皮肤的功能，这些皮肤用来当作桌面背景也是极好的！！！体验一下：

![桌面](E:\__Python\爬虫\下载王者荣耀皮肤\桌面.png)
