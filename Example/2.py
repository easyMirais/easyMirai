from package import easyMirai

if __name__ == '__main__':
    # 初始化->绑定QID->获取消息队列长度返回 字典 类型->运行结束
    mirai = easyMirai.Mirai("http://127.0.0.1", "8080", "123", "123", debug=True)
    print(mirai.begin())
    messageCount = mirai.getCountMessage()
    print(messageCount)
