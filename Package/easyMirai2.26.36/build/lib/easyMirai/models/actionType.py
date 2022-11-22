from .expand.actionGroup import ActionGroup
from .expand.actionFriend import ActionFriend


class actionTypeMode:
    # 操作模式
    def __init__(self, session, uri):
        self._session = session
        self._url = uri

    def __repr__(self):
        return "请选择群操作模式"

    def group(self, target: int):
        return ActionGroup(self._url, self._session, target)

    @property
    def friend(self):
        return ActionFriend(self._url, self._session)
