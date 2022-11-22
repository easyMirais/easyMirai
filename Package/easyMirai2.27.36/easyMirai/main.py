import time

import method

if __name__ == '__main__':
    easyMirai = method.Mirai("http://127.0.0.1", "2233", "2508417507", "INITKEYxWntQVgk")
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
    # print(easyMirai.send.group(862453481).plain("我是天使！").dictionary)
    # print(easyMirai.send.group(862453481).face(206).dictionary)
    # print(easyMirai.send.group(862453481).image("./image.png").dictionary)
    # print(easyMirai.send.group(3177045556).poke.FangDaZhao.dictionary)
    # print(easyMirai.send.group(3177045556).poke.poke.dictionary)

    # print(easyMirai.send.nudge(3177045556).group(862453481).dictionary)

    # print(easyMirai.send.recall(38426).dictionary)

    # print(easyMirai.send.temp(862453481).to(3177045556).plain("你好哇").dictionary)
    # print(easyMirai.send.temp(862453481).to(3177045556).image("./image.png").dictionary)
    # print(easyMirai.send.temp(862453481).to(3177045556).face(237).dictionary)

    # print(easyMirai.action.group(862453481).mute(2894472041).d(3).dictionary)
    # print(easyMirai.action.group(862453481).unmute(2894472041).dictionary)
    # print(easyMirai.action.group(862453481).muteAll.dictionary)
    # print(easyMirai.action.group(862453481).unMuteAll.dictionary)

    # print(easyMirai.action(862453481).group.kick(2181376101).dictionary)
    # print(easyMirai.action(862453481).group.quit.dictionary)

    # print(easyMirai.action.friend.deleteFriend(2894472041).dictionary)

    # print(easyMirai.upload.image("./image.png").friend.dictionary)

    # print(easyMirai.event(1659925849000000).newFriend(2508417507).yes("添加好友啦啦啦啦啦～").dictionary)
    # print(easyMirai.event(123123123).newJoinGroup(377694143, 862453481).yes("欢迎加入群聊").dictionary)
    # print(easyMirai.event(12345678).newBotJoinGroup(87654321, 2468, 27145).yes("接受邀请加入群聊").dictionary)
    # 30

    # print(easyMirai.get.info.dictionary)

    # print(easyMirai.get.message.count.dictionary)
    # print(easyMirai.get.message.fetch(1).dictionary)
    # print(easyMirai.get.message.fetchLatest(1).dictionary)
    print(easyMirai.get.message.peek(1).dictionary)
    # print(easyMirai.get.message.peekLatest(1).dictionary)
    # print(easyMirai.get.message.fromId(21261).dictionary)

    # print(easyMirai.get.list.friend.dictionary)
    # print(easyMirai.get.list.group.dictionary)
    # print(easyMirai.get.list.member(862453481).dictionary)

    # print(easyMirai.get.proFile.bot.dictionary)
    # print(easyMirai.get.proFile.friend(2894472041).dictionary)
    # print(easyMirai.get.proFile.member(862453481, 3177045556).dictionary)
    # print(easyMirai.get.proFile.user(3177045556).dictionary)
    # print(easyMirai.get.groupConfig(862453481).dictionary)
    # 45

    # print(easyMirai.set.essence(117).dictionary)

    # print(easyMirai.set.group(862453481).name("easyMirai").dictionary)
    # print(easyMirai.set.group(862453481).announcement("这是一个公告").dictionary)

    # print(easyMirai.set.group(862453481).confessTalk(True).dictionary)
    # print(easyMirai.set.group(862453481).allowMemberInvite(True).dictionary)
    # print(easyMirai.set.group(862453481).autoApprove(True).dictionary)
    # print(easyMirai.set.group(862453481).anonymousChat(True).dictionary)
    # 52


