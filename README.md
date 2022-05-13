# easyMirai

*斜体，一句话说明文章简介*

> **注意**: 这里是阅读前需要注意的内容[Babel](https://babeljs.io)

![Downloads](https://img.shields.io/github/downloads/ExMikuPro/easyMirai/total)
[![](https://img.shields.io/badge/blog-@Sfnco-ff69b4.svg)](https://sfnco.com.cn)
![](https://img.shields.io/github/size/ExMikuPro/easyMirai/TST/easyMirai.py)


## 目录

  1. [案例](#案例) 
  1. [调用](#调用)
## 案例
 这是一个简单的调用例子，实现了复读机的功能
```python
import  easyMirai
    
    
if __name__ == '__main__':
mirai = easyMirai.Mirai("YouHost", "YouPort", "YouKey", "YouQid")  # 初始化机器
print(mirai.begin())
while True:
    mirai.delay()
    if mirai.getCountMessage()['data'] != 0:
        message = mirai.getFetchLatestMessageFormat()
        if message['From'] == "FriendMessage":
            msg = {'type': 'Plain', "text": message['Plain'][0]}
            mirai.sendFriendMessage(msg, message['Sender'])

```

**[⬆ back to top](#目录)**

## 调用
关于调用问题一定要**实例化**后进行对于数据的操作！
```python
# bad
if mirai.getFetchLatestMessageFormat() == "test":
    ...

# good
message = mirai.getFetchLatestMessageFormat()
if message == "test":
    ...
```

**[⬆ back to top](#目录)**
