# -*- encoding: utf-8 -*-
def ObjectToDict(obj):
    memberlist = [m for m in dir(obj)]
    _dict = {}
    for m in memberlist:
        if m[0] != "_" and not callable(m):
            _dict[m] = getattr(obj,m)

    return _dict

def DictToObj(dict, obj):
    memberlist = [m for m in dir(obj)]
    for m in memberlist:
        if m[0] != "_" and not callable(m):
            setattr(obj,m,dict[m])
    return obj