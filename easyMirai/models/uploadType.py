from .expand.uplaodImage import expandUploadImage


class uploadTypeMode:
    # 上传模式
    def __init__(self, session, uri):
        self._session = session
        self._url = uri

    def __repr__(self):
        return "请选择上传模式"

    def image(self, path: str):
        return expandUploadImage(self._url, self._session, path)
