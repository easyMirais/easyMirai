from .expand.evenNewFriend import EventNewFriend
from .expand.eventJoinGroup import EventJoinGroup
from .expand.eventBotJoinGroup import EventBotJoinGroup


class eventTypeMode:
    # 操作模式
    def __init__(self, session, uri, eventId):
        self._session = session
        self._url = uri
        self._eventId = eventId  # 事件ID

    def __repr__(self):
        return "请选择事件处理类型"

    def newFriend(self, target: int, groupId: int = 0):
        return EventNewFriend(self._url, self._session, target, self._eventId, groupId)

    def newJoinGroup(self, target: int, groupId: int):
        return EventJoinGroup(self._url, self._session, target, self._eventId, groupId)

    def newBotJoinGroup(self, target: int, groupId: int, fromId: int):
        return EventBotJoinGroup(self._url, self._session, target, self._eventId, groupId, fromId)
