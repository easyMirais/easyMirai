import time

from Package import easyMirai

if __name__ == '__main__':
    # 初始化->绑定QID->注销Session->运行结束
    mirai = easyMirai.Mirai("http://127.0.0.1", "8080", "123", "123", debug=True)
    print(mirai.begin())
    time.sleep(2)  # 延时两秒后释放session
    mirai.releaseSession()
