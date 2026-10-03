import sys
import os
import time
import statistics

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sources import make_sorted_source
from merge_memory import merge_in_memory
from merge_stream import merge_stream


def bench_one(func, *args, warmup=3, repeats=5):

    # Прогрев
    for _ in range(warmup):
        func(*args)

    # Замеры
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter_ns()
        result = func(*args)
        t1 = time.perf_counter_ns()
        times.append(t1 - t0)

    return statistics.median(times), result


def run_in_memory(a, b):
    return merge_in_memory(a, b)


def run_stream(a, b):
    count = 0
    for _ in merge_stream(a, b):
        count += 1
    return count


def main():
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]

    print(f"{'n':>8} | {'in-memory, ns':>15} | {'stream, ns':>15}")
    print("-" * 46)

    for n in sizes:
        # Подготовка данных — вне замера
        a = make_sorted_source(n, seed=1)
        b = make_sorted_source(n, seed=2)

        # Замер in-memory
        t_mem, r_mem = bench_one(run_in_memory, a, b)

        # Замер stream
        t_str, r_str = bench_one(run_stream, a, b)

        # Результат используется (печатается), чтобы оптимизатор не выбросил
        print(f"{n:>8} | {t_mem:>15} | {t_str:>15}")

        # Проверка корректности — оба способа должны дать одинаковую длину
        assert len(r_mem) == 2 * n, f"in-memory вернул {len(r_mem)}, ожидалось {2 * n}"
        assert r_str == 2 * n, f"stream вернул {r_str}, ожидалось {2*n}"


if __name__ == "__main__":
    main()