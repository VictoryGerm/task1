import random
def make_sorted_list(n, seed=0, max_step=10):
    generator = random.Random(seed)
    result = []
    current = 0
    for i in range(n):
        step = generator.randint(0, max_step)
        current = current + step
        result.append(current)
    return result 