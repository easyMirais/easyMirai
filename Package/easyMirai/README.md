# easyMirai

![](./Docs/assets/image/title.png)

*介绍本项目的注意事项&主体结构*

**注意**本项目基于**开源软件** [Mirai](https://github.com/mamoe/mirai) 进行二次开发

**本项目地址：** [easyMirai](https://github.com/ExMikuPro/easyMirai/)

[![](https://img.shields.io/badge/blog-@Sfnco-ff69b4.svg)](https://sfnco.com.cn)
![](https://img.shields.io/github/size/ExMikuPro/easyMirai/TST/easyMirai.py)

## 目录

1. [案例](#案例)
2. [调用](#调用)
3. [声明](#声明)

## 案例

这是一个简单的调用例子，实现了复读机的功能

```python

from easyMirai import http as em

if __name__ == '__main__':
    mirai = em.Mirai("YouHost", "YouPort", "YouKey", "YouQid")
    print(mirai.begin())
    while True:
        mirai.delay()
        if mirai.getCountMessage()['data'] != 0:
            message = mirai.getFetchLatestMessageFormat()
            if message['From'] == "FriendMessage":
                msg = {'type': 'Plain', "text": message['Plain'][0]}
                mirai.sendFriendMessage(msg, message['Sender'])

```

更多案例请查阅 **Example** 目录，我们将持续更新相关案例，以方便调用！

**[⬆ back to top](#目录)**

## 调用

关于调用问题一定要**实例化**后进行对于数据的操作！

```python
# bad
if mirai.getFetchLatestMessageFormat() == "text":
    ...

# good
message = mirai.getFetchLatestMessageFormat()
if message == "text":
    ...
```

**[⬆ back to top](#目录)**

## 声明

本项目基于**开源软件** [Mirai](`https://github.com/mamoe/mirai`) 进行二次开发
> 不得扭曲或隐藏免费且开源的事实

**本项目使用AGPLv3**


此项目创建于**2022.05.15**，如果出现开发程序上的各种问题欢迎在**issues**发布！

**[⬆ back to top](#目录)**

<div style="text-align: center;">easyMirai@ExMikuPro</div>
