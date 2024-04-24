from rich.console import Console

from easyMirai.logger.level import LogLevel


class Logger:
    def __init__(self, isSlice):
        self._c = Console()
        self._isSlice = isSlice

    def Notice(self, content):
        if self._isSlice:
            self._c.log("[" + LogLevel.Notice.name + "]:" + content, style=LogLevel.Notice.value)

    def Warning(self, content):
        if self._isSlice:
            self._c.log("[" + LogLevel.Warning.name + "]:" + content, style=LogLevel.Warning.value)

    def Error(self, content):
        if self._isSlice:
            self._c.log("[" + LogLevel.Error.name + "]:" + content, style=LogLevel.Error.value)

    def Alert(self, content):
        if self._isSlice:
            self._c.log("[" + LogLevel.Alert.name + "]:" + content, style=LogLevel.Alert.value)
