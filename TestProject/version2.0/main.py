import method

if __name__ == '__main__':
    easyMirai = method.Mirai("http://127.0.0.1", "8080", "2894472041", "INITKEYxWntQVgk")
    # print(easyMirai.send.friend(3177045556).plain("你好哇哇哇哇哇～").json)
    # print(easyMirai.send.friend(3177045556).face(237).json)
    # print(easyMirai.send.friend(3177045556).image("./image.png").dictionary)
    # print(easyMirai.send.friend(3177045556).poke.FangDaZhao.dictionary)
    # print(easyMirai.send.friend(3177045556).poke.poke.dictionary)
    # print(easyMirai.send.friend(3177045556).dice(6).dictionary)
    # print(easyMirai.send.friend(3177045556).musicShare().dictionary) 核心问题待解决！！！

    # print(easyMirai.send.nudge(3177045556).friend.dictionary)

    # print(easyMirai.send.group(862453481).at(3177045556, "憨憨"))
    # print(easyMirai.send.group(862453481).atAll.dictionary)
    # print(easyMirai.send.group(862453481).plain("hello world").dictionary)
    # print(easyMirai.send.group(862453481).face(206).dictionary)
    # print(easyMirai.send.group(862453481).image("./image.png").dictionary)
    # print(easyMirai.send.group(3177045556).poke.FangDaZhao.dictionary)
    # print(easyMirai.send.group(3177045556).poke.poke.dictionary)

    # print(easyMirai.send.nudge(3177045556).group(862453481).dictionary)

    # print(easyMirai.send.temp(862453481).to(3177045556).plain("你好哇").dictionary)
    # print(easyMirai.send.temp(862453481).to(3177045556).image("./image.png").dictionary)
    # print(easyMirai.send.temp(862453481).to(3177045556).face(237).dictionary)

    # print(easyMirai.upload.image("./image.png").friend.dictionary)
