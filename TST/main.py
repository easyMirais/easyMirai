import easyMirai

if __name__ == '__main__':
    mirai = easyMirai.Mirai("http://127.0.0.1", "8080", "INITKEYxWntQVgk", "1901731529")  # 初始化机器
    print(mirai.begin())
    while True:
        mirai.delay()
        msg = mirai.getFriendList()
        for liast in msg["data"]:
            string = str(liast["id"])
            file = open("T.log", 'a+', encoding='utf-8')
            readFile = open("T.log", 'r', encoding='UTF-8')
            data = readFile.read()
            if string in data:
                file.close()
            else:
                urls = mirai.uploadImage("friend", "./8CCD5AA34CF0EC837F64B1857121B58F.png")
                file.write(str(string) + "\n")
                print("正在写入")
                msg1: dict = {
                    "type": "Plain",
                    "text": "你好哇哇哇！"
                }
                msg2: dict = {
                    "type": "Image",
                    "url": urls['url']
                }
                mirai.sendFriendMessage(msg1, string)
                mirai.sendFriendMessage(msg2, string)
