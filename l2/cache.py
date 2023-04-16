from random import randint
from numpy import mean

n = 100
k = 10

class Cache:
    def __init__(self, n,k) -> None:
        self.cache = []
        self.pages = []
        self.n = 100
        self.k = 10

    def request_page(self,p) -> int:
        return 1
    
class CacheFIFO(Cache):
    
    def request_page(self,p):
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.pop(0)
            self.cache.append(p)
            return 1
        
class CacheFWF(Cache):
    
    def request_page(self,p):
        if p in self.cache:
            return 0
        else:
            self.cache.append(p)
            if len(self.cache) == self.k:
                self.cache = []
            return 1
        
class CacheLRU(Cache):
    
    lru = None

    def request_page(self,p):
        if p in self.cache:
            self.lru = p
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.remove(self.lru)
            self.cache.append(p)
            self.lru = p
            return 1
        
class CacheLFU(Cache):

    def __init__(self, n,k) -> None:
        Cache.__init__(self, n,k)
        self.num_accesses = [0]*(n+1)

    def find_min(self) -> int:
        id = self.cache[0]
        min = self.num_accesses[id]
        for c in self.cache:
            if self.num_accesses[c] < min:
                min = self.num_accesses[c]
                id = c
        return id

    def request_page(self,p):
        self.num_accesses[p] += 1
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.remove(self.find_min())
            self.cache.append(p)
            return 1

class CacheRandom(Cache):

    def request_page(self,p):
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.pop(randint(0,self.k-1))
            self.cache.append(p)
            return 1

class CacheRMA(Cache):

    def __init__(self, n,k) -> None:
        Cache.__init__(self, n,k)
        self.marked = [False]*(k)
        self.num_marked = 0

    def reset_marks(self):
        self.marked = [False]*(self.k)
        self.num_marked = 0

    def request_page(self,p):
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.pop(randint(0,self.k-1))
            self.cache.append(p)
            return 1
'''
class CacheFIFO:
    
    def __init__(self, val) -> None:
        self.cache = []
        self.pages = []
        self.n = 100
        self.k = 10

    def request_page(self,p):
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == k:
                self.cache.pop(0)
            self.cache.append(p)
            return 1
'''
        
o= []
for i in range(100000):
    uniform = [randint(1, n) for _ in range(n)]
    
    o.append([])
    cache = CacheFIFO(n,k)
    cnt = 0
    for u in uniform:
        cnt+=cache.request_page(u)
    o[0].append(cnt)

    o.append([])
    cache = CacheFWF(n,k)
    cnt = 0
    for u in uniform:
        cnt+=cache.request_page(u)
    o[1].append(cnt)

    o.append([])
    cache = CacheLRU(n,k)
    cnt = 0
    for u in uniform:
        cnt+=cache.request_page(u)
    o[-1].append(cnt)

    o.append([])
    cache = CacheLFU(n,k)
    cnt = 0
    for u in uniform:
        cnt+=cache.request_page(u)
    o[-1].append(cnt)

    o.append([])
    cache = CacheRandom(n,k)
    cnt = 0
    for u in uniform:
        cnt+=cache.request_page(u)
    o[-1].append(cnt)
    

print(f'FIFO: {mean(o[0])}')
print(f'FWF:  {mean(o[1])}')
print(f'LRU:  {mean(o[2])}')
print(f'LFU:  {mean(o[3])}')
print(f'Rand: {mean(o[4])}')
#FIFO: 89.9244
#FIFO: 90.0743



