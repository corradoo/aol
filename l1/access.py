'''
Dla listy jednokierunkowej zdefiniujmy operację Access(i) która przegląda listę od początku 
i sprawdza czy element i jest na liście, a w przypadku braku elementu na liście
wstawia go na końcu listy. Kosztem operacji Access(i) będzie liczba przejrzanych elementów
listy. Zbadaj średni koszt n operacji Access(X), gdzie X jest zmienną losową przyjmującą
wartości ze zbioru {1, . . . , 100}.
'''

from matplotlib import pyplot as plt
from numpy import random, mean
import random as rn


class Node:
    def __init__(self, val) -> None:
        self.cnt = 0
        self.val = val
        self.next = None

    def add_node(self, node) -> None:
        self.next = node


class LinkedList:
    def __init__(self, head, org='none') -> None:
        self.head = head
        self.s_org = org

    def get_len(self):
        cnt = 0
        curr = self.head
        while(curr != None):
            curr = curr.next
            cnt += 1
        return cnt

    def organize(self, prev2, prev, curr):
        if self.s_org == 'mtf' and prev != None:
            prev.next = curr.next
            curr.next = self.head
            self.head = curr

        if self.s_org == 'transpose' and prev != None:
            if prev == self.head:
                self.head = curr
            else:
                prev2.next = curr
            prev.next = curr.next
            curr.next = prev

        if self.s_org == 'count':
            prev = None
            curr = self.head
            # New head case
            if curr.next != None and curr.val < curr.next.val:  # at least 2 elements
                self.head = curr.next
                curr.next = self.head.next
                self.head.next = curr

            while(curr.next != None and curr.val >= curr.next.val):
                prev = curr
                curr = curr.next

            if curr.next != None:
                prev.next = curr.next
                curr.next = curr.next.next
                prev.next.next = curr

    def access(self, val) -> int:
        if self.head == None:
            self.head = Node(val)
            self.head.cnt = 1
            return 0
        prev = None
        prev2 = None
        curr = self.head
        cost = 1
        while(curr != None and curr.val != val):
            # print(f'Node({cost}) val({curr.val}) cnt({curr.cnt})')
            cost += 1
            if curr.next == None:
                curr.next = Node(val)
                # print('NEW!')
            prev2 = prev
            prev = curr
            curr = curr.next
        curr.cnt += 1
        self.organize(prev2, prev, curr)
        return cost


class LinkedListS:
    def __init__(self, head, org='none') -> None:
        self.s_org = org
        self.t = []

    def get_len(self):
        return len(self.t)

    def access(self, val):
        cost = 0
        for e in self.t:
            cost += 1
            if e[0] == val:
                self.t[cost-1] = (val, e[1]+1)
                return cost
        self.t.append((val, 1))
        self.organize()
        return cost
    
    def organize(self):
        if self.s_org == 'count':
            self.t.sort(key=lambda tup: tup[1], reverse=True)
    

ns = [100, 500, 1000, 5000, 10000, 50000, 100000]
orgs = ['none', 'transpose', 'mtf', 'count']
dists = ['u', 'h', 'h2', 'g']

outcome = {}
outcome2 = {}

for o in orgs:
    outcome[o] = {}
    for d in dists:
        outcome[o][d] = []

for d in dists:
    outcome2[d] = {}
    for o in orgs:
        outcome2[d][o] = []


for n in ns:
    for org in orgs:

        # Uniform distribution
        ll = LinkedList(None, org)
        if org == 'count':
            ll = LinkedListS(None, org)
        sum = 0
        for i in range(n):
            sum += ll.access(rn.randint(1, 100))

        print(f'E(uniform)={sum/n}')
        print(ll.get_len())
        outcome[org]['u'].append((n, sum/n))
        outcome2['u'][org].append((n, sum/n))

        # Harmonic distribution
        ll = LinkedList(None, org)
        if org == 'count':
            ll = LinkedListS(None, org)

        sum = 0

        h100 = 0
        for i in range(1, 100+1):
            h100 += 1/i

        harmonic = random.choice([i for i in range(1, 100+1)],
                                 p=[1/(i*h100) for i in range(1, 100+1)], size=(n))

        for i in harmonic:
            sum += ll.access(i)

        print(f'E(harmonic)={sum/n}')
        print(ll.get_len())
        outcome[org]['h'].append((n, sum/n))
        outcome2['h'][org].append((n, sum/n))
        # 2-Harmonic distribution
        ll = LinkedList(None, org)
        if org == 'count':
            ll = LinkedListS(None, org)
        sum = 0

        h100 = 0
        for i in range(1, 100+1):
            h100 += 1/i**2

        harmonic2 = random.choice([i for i in range(1, 100+1)],
                                  p=[1/(i**2*h100) for i in range(1, 100+1)], size=(n))

        for i in harmonic2:
            sum += ll.access(i)

        print(f'E(2-harmonic)={sum/n}')
        print(ll.get_len())
        outcome[org]['h2'].append((n, sum/n))
        outcome2['h2'][org].append((n, sum/n))

        # Geometric
        ll = LinkedList(None, org)
        if org == 'count':
            ll = LinkedListS(None, org)
        sum = 0

        geo = random.choice([i for i in range(1, 100+1)],
                            p=[1/2**i for i in range(1, 100)]+[1/2**99], size=(n))

        for i in geo:
            sum += ll.access(i)

        print(f'E(geometric)={sum/n}')
        print(ll.get_len())
        outcome[org]['g'].append((n, sum/n))
        outcome2['g'][org].append((n, sum/n))
        # if(org == 'count'):
        #     breakpoint()

print(outcome)


for o in orgs:
    plt.plot([n[0]for n in outcome[o]['u']], [e[1]
             for e in outcome[o]['u']], 'o', label="uniform")
    plt.plot([n[0]for n in outcome[o]['h']], [e[1]
             for e in outcome[o]['h']], 'o', label="harmonic")
    plt.plot([n[0]for n in outcome[o]['h2']], [e[1]
             for e in outcome[o]['h2']], 'o', label="two-harmonic")
    plt.plot([n[0]for n in outcome[o]['g']], [e[1]
             for e in outcome[o]['g']], 'o', label="geometric")
    plt.legend()
    plt.title(f"Organization: {o}")
    plt.xscale('log')
    plt.savefig(f'{o}.png')
    plt.clf()

for d in dists:
    plt.plot([n[0]for n in outcome2[d]['none']], [e[1]
             for e in outcome2[d]['none']], 'o', label="none")
    plt.plot([n[0]for n in outcome2[d]['mtf']], [e[1]
             for e in outcome2[d]['mtf']], 'o', label="move-to-front")
    plt.plot([n[0]for n in outcome2[d]['transpose']], [e[1]
             for e in outcome2[d]['transpose']], 'o', label="transpose")
    plt.plot([n[0]for n in outcome2[d]['count']], [e[1]
             for e in outcome2[d]['count']], 'o', label="count")
    plt.legend()
    plt.title(f"Distribution: {d}")
    plt.xscale('log')
    plt.grid()
    plt.ylabel("Average cost")
    plt.xlabel("Number of samples")
    plt.savefig(f'{d}.png')
    plt.clf()
