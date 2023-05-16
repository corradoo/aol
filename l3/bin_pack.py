import json
import math
import random

from numpy import mean
from dists import generate_distribution


def generate_input(d):
    dist = generate_distribution(d, 100, 10)
    # print(dist)

    input = []
    for k in dist:
        x = random.random()
        for _ in range(k):
            input.append(x)
        if len(input) >= 100:
            break

    input = input[:100]
    # print(input)
    return input


def next_fit(input):

    cap = 1.0
    bin = 1
    for i in input:
        if cap >= i:
            cap -= i
        else:
            bin += 1
            cap = 1-i
        # print(f'Element {i:.3f} \tbin: {bin} \tcap:{cap:.3f}')
    return bin


def first_fit(input):
    bins = [1.0]*100
    for i in input:
        for id, b in enumerate(bins):
            if b >= i:
                bins[id] -= i
                # print(f'Element {i:.3f} \tbin: {id} \tcap:{b:.3f}')
                break
    c = 100
    for id, b in enumerate(bins):
        if b == 1:  # First empty bin
            c = id
            break
    return c


def best_fit(input):
    bins = [1.0]*100
    for i in input:
        for id, b in enumerate(bins):
            if b >= i:
                bins[id] -= i
                # print(f'Element {i:.3f} \tbin: {id} \tcap:{b:.3f}')
                bins.sort()
                break
    c = 100
    for id, b in enumerate(bins):
        if b == 1:  # First empty bin
            c = id
            break
    return c


def worst_fit(input):
    bins = [1.0]
    for i in input:
        # breakpoint()
        for id, b in enumerate(bins):
            if b >= i:
                bins[id] -= i
                # print(f'Element {i:.3f} \tbin: {id} \tcap:{b:.3f}')
                bins.sort(reverse=True)
                break
            if id == len(bins)-1:
                bins.append(1-i)
                bins.sort(reverse=True)
                break

    return len(bins)


def random_fit(input):
    bins = [1.0]
    for i in input:
        random.shuffle(bins)
        for id, b in enumerate(bins):
            if b >= i:
                bins[id] -= i
                break
            if id == len(bins)-1:
                bins.append(1-i)
                break
    return len(bins)


funs = [next_fit, first_fit, best_fit, worst_fit, random_fit]
dists = ['g', 'u', 'h', 'h2']

dict2 = {}
for f in funs:
    dict2[f.__name__] = {}
    for d in dists:
        dict2[f.__name__][d] = 0

for d in dists:
    print(f'{d} ')
    o = {}
    for f in funs:
        o[f.__name__] = []

    for _ in range(10000):
        input = generate_input(d)
        opt = math.ceil(sum(input))

        for f in funs:
            out = f(input)
            o[f.__name__].append(out/opt)
            # print(f'\t{f.__name__} -> {o} c={o/opt}')

    for f in o:
        print(f'\t{f} \t-> c={mean(o[f]):.4f}')
        dict2[f][d] = mean(o[f])

print(dict2)
with open("outcome.json", "w") as outfile:
    json.dump(dict2, outfile, indent=4)
# ff = first_fit(input)
# nf = next_fit(input)
# bf = best_fit(input)
# wf = worst_fit(input)
# rf = random_fit(input)
