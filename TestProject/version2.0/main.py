import method

if __name__ == '__main__':
    easyMirai = method.Mirai("http://127.0.0.1", "8080", "2508417507", "INITKEYxWntQVgk")
    easyMirai.send.friend(3177045556).text("你好哇哇哇哇哇～")
    print(easyMirai.send.group("just do do").at("这是一条消息").json)
    print(easyMirai.send.friend(3177045556).image(
        "https://i0.hdslb.com/bfs/album/67fc4e6b417d9c68ef98ba71d5e79505bbad97a1.png"))
