from typing import Iterator, List
import random


def make_sorted_source(length: int, seed: int = 0,
                       max_step: int = 10) -> List[int]:
    rng = random.Random(seed)
    data = []
    cur = 0
    for _ in range(length):
        cur += rng.randint(0, max_step)
        data.append(cur)
    return data


def stream_source(data: List[int]) -> Iterator[int]:
    for x in data:
        yield x