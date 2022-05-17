import easyMirai

if __name__ == '__main__':
    mirai = easyMirai.Mirai("http://127.0.0.1", "8080", "INITKEYxWntQVgk", "377694143")  # 初始化机器
    print(mirai.begin())

    f = open("id.txt", "a")

    for lists in mirai.getGroupList("658436145")["data"]:
        if lists['permission'] == 'MEMBER':
            print("成功写入：" + str(lists['id']))
            f.write(str(lists['id']) + "\n")
    f.close()
