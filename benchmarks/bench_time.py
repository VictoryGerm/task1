import sys
import os
import time
import statistics
import matplotlib.pyplot as plt

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



# Строит график времени in-memory and stream от объема данных (в байтах)
def plot_results(sizes_bytes, mem_times, stream_times, filename="benchmark.png"):
    plt.figure(figsize=(10,6))
    plt.plot(sizes_bytes, mem_times, marker="o", label="in-memory")
    plt.plot(sizes_bytes, stream_times, marker="s", label="stream")
    # Логарифмическая шкала по X, потому что размеры растут ×2
    plt.xscale("log", base=2)

    plt.xlabel("Объём данных (байты)")
    plt.ylabel("Время (наносекунды)")
    plt.title("Вариант 40: слияние двух отсортированных источников")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)

    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"График сохранён в {filename}")


def main():
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]

    print(f"{'n':>8} | {'in-memory, ns':>15} | {'stream, ns':>15}")
    print("-" * 46)
    """Для графика"""
    sizes_bytes = []
    mem_times=[]
    stream_times = []

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

        sizes_bytes.append(n * 8)
        mem_times.append(t_mem)
        stream_times.append(t_str)
    """после цикла строим график"""
    plot_results(sizes_bytes, mem_times, stream_times)


if __name__ == "__main__":
    main()