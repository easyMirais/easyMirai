import easyMirai

if __name__ == '__main__':
    mirai = easyMirai.Mirai("http://127.0.0.1", "8080", "INITKEYxWntQVgk", "377694143")  # 初始化机器
    print(mirai.begin())

