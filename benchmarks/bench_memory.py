import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sources import make_sorted_source


class MemoryCounter:
    def __init__(self):
        self.alive = 0      # сколько сейчас живых
        self.peak = 0       # максимум за всё время
        self.total = 0      # всего выделено

    def alloc(self, k=1):
        self.alive += k
        self.total += k
        if self.alive > self.peak:
            self.peak = self.alive

    def free(self, k=1):
        self.alive -= k


def merge_in_memory_counted(a, b, mc):
    result = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            mc.alloc()
            i = i + 1
        else:
            result.append(b[j])
            mc.alloc()
            j = j + 1

    while i < len(a):
        result.append(a[i])
        mc.alloc()
        i = i + 1

    while j < len(b):
        result.append(b[j])
        mc.alloc()
        j = j + 1

    return result


def merge_stream_counted(a, b, mc):
    it_a = iter(a)
    it_b = iter(b)

    value_a = next(it_a, None)
    mc.alloc()
    value_b = next(it_b, None)
    mc.alloc()

    while value_a is not None and value_b is not None:
        if value_a <= value_b:
            yield value_a
            mc.free()                  # отдали и забыли value_a
            value_a = next(it_a, None)
            if value_a is not None:
                mc.alloc()
        else:
            yield value_b
            mc.free()
            value_b = next(it_b, None)
            if value_b is not None:
                mc.alloc()

    while value_a is not None:
        yield value_a
        mc.free()
        value_a = next(it_a, None)
        if value_a is not None:
            mc.alloc()

    while value_b is not None:
        yield value_b
        mc.free()
        value_b = next(it_b, None)
        if value_b is not None:
            mc.alloc()


def main():
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]

    print(f"{'n':>8} | {'in-memory peak':>15} | {'stream peak':>12}")
    print("-" * 42)

    for n in sizes:
        a = make_sorted_source(n, seed=1)
        b = make_sorted_source(n, seed=2)

        # Замер in-memory
        mc_mem = MemoryCounter()
        result = merge_in_memory_counted(a, b, mc_mem)

        mc_str = MemoryCounter()
        count = 0
        for _ in merge_stream_counted(a, b, mc_str):
            count += 1

        print(f"{n:>8} | {mc_mem.peak:>15} | {mc_str.peak:>12}")

        # Проверки
        assert len(result) == 2 * n
        assert count == 2 * n
        assert mc_mem.peak == 2 * n
        assert mc_str.peak == 2

if __name__ == "__main__":
    main()