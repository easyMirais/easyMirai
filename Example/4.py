import time

import easyMirai

if __name__ == '__main__':
    # 初始化->绑定QID->获取尾部消息队列返回 字典 类型->循环获取
    mirai = easyMirai.Mirai("http://127.0.0.1", "8080", "123", "123", debug=True)
    print(mirai.begin())
    while True:
        time.sleep(2)
        message = mirai.getFetchLatestMessage()
        print(message)
