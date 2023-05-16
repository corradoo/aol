from numpy import mean, random

def get_h(pages=100):
    h100 = 0
    for i in range(1, pages+1):
        h100 += 1/i
    return h100


def get_2h(pages=100):
    h100 = 0
    for i in range(1, pages+1):
        h100 += 1/i**2
    return h100

def generate_distribution(type: str, samples: int, pages: int):
    if type == 'u':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/pages for _ in range(1, pages+1)], size=(samples))
    if type == 'h':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/(i*get_h(pages)) for i in range(1, pages+1)],
                             size=(samples))
    if type == 'h2':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/(i**2*get_2h(pages)) for i in range(1, pages+1)], size=(samples))
    if type == 'g':
        return random.choice([i for i in range(1, pages+1)],
                             p=[1/2**i for i in range(1, pages)]+[1/2**(pages-1)], size=(samples))