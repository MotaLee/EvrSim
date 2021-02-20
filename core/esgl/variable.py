class AdpDict(dict):
    ''' {int AroID:[AroDarwpart adp,..],..}'''
    def __init__(self):
        self._cache=list()
        return

    def rmByAroid(self,aroid:int):
        self._cache.clear()
        item=self[aroid]
        del self[aroid]
        return item

    def clear(self) -> None:
        self._cache.clear()
        return super().clear()

    def clearCache(self):
        self._cache.clear()
        return

    def hasCache(self):
        if len(self._cache)!=0:return True
        else:return False

    def getAllAdp(self):
        if len(self._cache)!=0:
            return self._cache
        else:
            for adplist in self.values():
                self._cache+=adplist
        return self._cache
    pass

class TdpDict(dict):
    def __init__(self):
        self._cache=list()
        return

    def add(self,name:str,tdp):
        if not isinstance(tdp,list):tdp=[tdp]
        self._cache.clear()
        self[name]=tdp
        return

    def remove(self,name:str):
        self._cache.clear()
        item=self[name]
        del self[name]
        return item

    def getAll(self):
        if len(self._cache)!=0:
            return self._cache
        else:
            for tdplist in self.values():
                self._cache+=tdplist
        return self._cache
    pass
