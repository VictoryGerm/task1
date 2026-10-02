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


class ListStream:
    def __init__(self, data):
        self.data = data
        self.position = 0
    def __iter__(self): 
        return self
    def __next__(self):
        if self.position >= len(self.data):
            raise StopIteration
        value = self.data[self.position]
        self.position = self.position + 1
        return value