# coding: utf-8


class WsBaseError(Exception):
    def __init__(self, line=0, col=0):
        self.value = "error"
        self.line = line
        self.col = col

    def __str__(self):
        if self.line and self.col:
            return "\n%s: %s. %s, %s\n" % (self.__class__.__name__, self.value, self.line, self.col)
        return "\n%s: %s.\n" % (self.__class__.__name__, self.value)


class WsSyntaxError(WsBaseError):
    def __init__(self, *args, **kwargs):
        super(WsSyntaxError, self).__init__(*args, **kwargs)
        self.value = "invalid syntax"


class StackEmptyError(WsBaseError):
    def __init__(self, *args, **kwargs):
        super(StackEmptyError, self).__init__(*args, **kwargs)
        self.value = "stack empty, can't pop"


class HeapIndexError(WsBaseError):
    def __init__(self, *args, **kwargs):
        super(HeapIndexError, self).__init__(*args, **kwargs)
        self.value = "index out of range"


class StackIndexError(HeapIndexError):
    pass


class NoExistLabelError(WsBaseError):
    def __init__(self, label, *args, **kwargs):
        super(NoExistLabelError, self).__init__(*args, **kwargs)
        self.label = label
        self.value = "can't find label "
