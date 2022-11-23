import json


class echoTypeMode:

    def __init__(self, context):
        self._context = context

    def __repr__(self):
        return "<Request [OK]>"

    @property
    def json(self) -> str:
        """
        将返回值格式化为字符串类型
        @return: str
        """
        data = json.dumps(self._context)
        return data

    @property
    def dictionary(self) -> dict:
        """
        将返回值格式化为字典类型
        @return: dict
        """
        return self._context
