# easyMirai

![](./Docs/assets/image/title-v2.png)

*介绍本项目的注意事项&主体结构*

**注意**本项目基于**开源软件** [Mirai](https://github.com/mamoe/mirai) 进行二次开发

> easyMriai webSocket版本正在紧张开发中 >w< 详情：[easyMirai webSocket](https://github.com/easyMirais/easyMirai-webSocket)

目前**easyMirai**已经进入全新的**2.0**时代！！🥳

> 注意⚠️：不与1.0版本相兼容 1.0版本将停留在**1.2.36 LTS**版本 

开发文档请移步到[easyMirai Wiki](https://github.com/easyMirais/easyMirai/wiki/Home)

> 注意⚠：当从以前升级到此版本(2.27.39)需要将`get.message.count`修改成`get.message.count()`可以传入bool类型，用于在重复调用`get.message.count`以防止日志过多造成控制台崩溃
> 
> True:仅不输出get类日志 ， False输出get类日志
> >感谢提供的建议和新的版本(2.27.39)

[![](https://img.shields.io/badge/blog-@Sfnco-ff69b4.svg?style=flat-square&)](https://sfnco.com.cn)
![](https://img.shields.io/github/size/easyMirais/easyMirai/README.md?style=flat-square&logo=appveyor)
![](https://img.shields.io/badge/Python-3.6+-73b1e2?style=flat-square&logo=appveyor)
![](https://img.shields.io/badge/easyMirai-2.0-73d1a4?style=flat-square)

## 目录

1. [案例](#案例)
2. [调用](#调用)
3. [声明](#声明)

## 案例

这是一个简单的调用例子，实现了发送普通文字的功能

```python

import easyMirai

if __name__ == '__main__':
    mirai = easyMirai.Mirai("YouHost", "YouPort", "YouQid", "YouKey")
    mirai.send.friend(12345678).plain("hello world!").dictionary

```

> 很好理解吧....(大概)

更多案例请查阅 **Example** 目录，我们将持续更新相关案例，以方便调用！

> 本Python库，为了方便各版本移植，除重大错误外理论上不会再次改变函数方法和命名～
> 本库基于HTTP轮询实现，接下来会编写相对应的webSocket的相关程序～


**[⬆ back to top](#目录)**

## 调用

```shell
pip3 install easyMirai
```

关于调用问题一定要**实例化**后进行对于数据的操作！

```python
# bad

if mirai.get.message.peek(1).dictionary == "text":
    ...

# good
message = mirai.get.message.peek(1).dictionary
if message == "text":
    ...
```

**[⬆ back to top](#目录)**

## 声明

本项目基于**开源软件** [Mirai](`https://github.com/mamoe/mirai`) 进行二次开发

> 不得扭曲或隐藏免费且开源的事实

**本项目使用AGPLv3**

> 关于文档👩‍💻&🧑‍💻正在抓紧完善，会尽快发布～


此项目创建于**2022.05.15**，如果出现开发程序上的各种问题欢迎在**issues**发布！

**[⬆ back to top](#目录)**

<div style="text-align: center;">easyMirai@ExMikuPro&@HexMikuMax</div>
