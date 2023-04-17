from random import randint
from numpy import mean, random
from matplotlib import pyplot as plt
class Cache:
    def __init__(self, n, k) -> None:
        self.cache = []
        self.pages = []
        self.n = 100
        self.k = 10

    def request_page(self, p) -> int:
        return 1


class CacheFIFO(Cache):

    def request_page(self, p):
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.pop(0)
            self.cache.append(p)
            return 1


class CacheFWF(Cache):

    def request_page(self, p):
        if p in self.cache:
            return 0
        else:
            self.cache.append(p)
            if len(self.cache) == self.k:
                self.cache = []
            return 1


class CacheLRU(Cache):


    def request_page(self, p):
        # print(f'lru={self.lru}req:{p}\t len:{len(self.cache)} {self.cache}')
        if p in self.cache:
            self.cache.remove(p)
            self.cache.insert(0,p)
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.pop(-1)
            self.cache.insert(0,p)
            return 1


class CacheLFU(Cache):

    def __init__(self, n, k) -> None:
        Cache.__init__(self, n, k)
        self.num_accesses = [0]*(n+1)

    def find_min(self) -> int:
        id = self.cache[0]
        min = self.num_accesses[id]
        for c in self.cache:
            if self.num_accesses[c] < min:
                min = self.num_accesses[c]
                id = c
        return id

    def request_page(self, p):
        self.num_accesses[p] += 1
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.remove(self.find_min())
            self.cache.append(p)
            return 1


class CacheRandom(Cache):

    def request_page(self, p):
        if p in self.cache:
            return 0
        else:
            if len(self.cache) == self.k:
                self.cache.pop(randint(0, self.k-1))
            self.cache.append(p)
            return 1


class CacheRMA(Cache):

    def __init__(self, n, k) -> None:
        Cache.__init__(self, n, k)
        self.marked = [False]*(k)

    def reset_marks(self):
        # print(f"RESET-> {self.marked}")
        self.marked = [False]*(self.k)

    def replace_unmarked(self, p):
        ids = [i for i in range(self.k) if not self.marked[i]]
        id = randint(0, len(ids)-1)
        replace_id = ids[id]
        self.cache[replace_id] = p
        self.marked[replace_id] = True
        # breakpoint()

    def request_page(self, p):
        # print(f'req:{p}\t len:{len(self.cache)} {self.cache}')

        if p in self.cache:
            self.marked[self.cache.index(p)] = True
            return 0
        else:
            if sum(self.marked) == self.k:
                self.reset_marks()
            if len(self.cache) == self.k:
                self.replace_unmarked(p)
            else:
                self.cache.append(p)
                self.marked[self.cache.index(p)] = True
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


def generate_distribution(type, samples, pages):
    if type == 'u':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/pages for _ in range(1, pages+1)], size=(samples))
    if type == 'h':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/(i*get_h100()) for i in range(1, pages+1)],
                             size=(samples))
    if type == 'h2':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/(i**2*get_2h100()) for i in range(1, pages+1)], size=(samples))
    if type == 'g':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/2**i for i in range(1, pages)]+[1/2**(pages-1)], size=(samples))


def get_h100():
    h100 = 0
    for i in range(1, 100+1):
        h100 += 1/i
    return h100


def get_2h100():
    h100 = 0
    for i in range(1, 100+1):
        h100 += 1/i**2
    return h100

n = 100
k = 20

samples = [n,500, 1000]
iterations = 10**3
dists = ['g','u','h','h2']
orgs = ['fifo','fwf','lru','lfu','rand','rma']

outcome = {}


for d in dists:
    outcome[d] = {}
    for o in orgs:
        outcome[d][o] = []
for s in samples:
    for d in dists:
        o = []
        for i in range(iterations):
            pages_seq = generate_distribution(d,s,100)

            caches = [CacheFIFO(n, k),CacheFWF(n, k),CacheLRU(n, k),CacheLFU(n, k),CacheRandom(n, k), CacheRMA(n, k)]

            for c in caches:
                o.append([])
                cnt = 0
                for u in pages_seq:
                    cnt += c.request_page(u)
                o[-1].append(cnt)


        print(f'Distribution: {d}')
        print(f'Samples: {s}')
        print(f'FIFO: {mean(o[0])}')
        print(f'FWF:  {mean(o[1])}')
        print(f'LRU:  {mean(o[2])}')
        print(f'LFU:  {mean(o[3])}')
        print(f'Rand: {mean(o[4])}')
        print(f'RMA:  {mean(o[5])}')

        outcome[d]['fifo'].append((s,mean(o[0])))
        outcome[d]['fwf'].append((s,mean(o[1])))
        outcome[d]['lru'].append((s,mean(o[2])))
        outcome[d]['lfu'].append((s,mean(o[3])))
        outcome[d]['rand'].append((s,mean(o[4])))
        outcome[d]['rma'].append((s,mean(o[5])))


for d in dists:
    for o in orgs:
        plt.plot([n[0]for n in outcome[d][o]], [e[1]
            for e in outcome[d][o]], 'o', label=o)
    
    plt.legend()
    plt.title(f"Distribution: {d}")
    plt.xscale('log')
    plt.grid()
    plt.ylabel("Average cost")
    plt.xlabel("Number of samples")
    plt.savefig(f'{d}.png')
    plt.clf()

orgs2 = ['fifo','lru','rand','rma']
for d in dists:
    for o in orgs2:
        plt.plot([n[0]for n in outcome[d][o]], [e[1]
            for e in outcome[d][o]], 'o', label=o)
    
    plt.legend()
    plt.title(f"Distribution: {d}")
    plt.xscale('log')
    plt.grid()
    plt.ylabel("Average cost")
    plt.xlabel("Number of samples")
    plt.savefig(f'mid_{d}.png')
    plt.clf()