import sys
import os
import matplotlib.pyplot as plt

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




def plot_memory(sizes_bytes, mem_peaks, stream_peaks, filename="bench_memory.png"):
    """Строит график пиковой памяти in-memory vs stream от объёма данных."""
    plt.figure(figsize=(10, 6))

    plt.plot(sizes_bytes, mem_peaks, marker="o", label="in-memory")
    plt.plot(sizes_bytes, stream_peaks, marker="s", label="stream")

    plt.xscale("log", base=2)      # по X — данные растут ×2
    plt.yscale("log", base=10)     # по Y — stream=2 и in-memory=2n, разница огромная

    plt.xlabel("Объём данных (байты)")
    plt.ylabel("Пиковая память (элементов)")
    plt.title("Вариант 40: пиковая память при слиянии")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)

    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"График сохранён в {filename}")




def main():
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]

    print(f"{'n':>8} | {'in-memory peak':>15} | {'stream peak':>12}")
    print("-" * 42)

    sizes_bytes = []
    mem_peaks = []
    stream_peaks = []

    for n in sizes:
        a = make_sorted_source(n, seed=1)
        b = make_sorted_source(n, seed=2)

        mc_mem = MemoryCounter()
        result = merge_in_memory_counted(a, b, mc_mem)

        mc_str = MemoryCounter()
        count = 0
        for _ in merge_stream_counted(a, b, mc_str):
            count += 1

        print(f"{n:>8} | {mc_mem.peak:>15} | {mc_str.peak:>12}")

        assert len(result) == 2 * n
        assert count == 2 * n
        assert mc_mem.peak == 2 * n
        assert mc_str.peak == 2

        sizes_bytes.append(n * 8)
        mem_peaks.append(mc_mem.peak)
        stream_peaks.append(mc_str.peak)

    plot_memory(sizes_bytes, mem_peaks, stream_peaks)
    estimate_memory_limit(ram_gb=8)      # ← вызвали, но она объявлена СНАРУЖИ


def estimate_memory_limit(ram_gb=16):      # ← ВНЕ main, на верхнем уровне
    """Оценка: при каком n in-memory перестанет влезать в RAM."""
    bytes_per_element = 36
    elements_alive = 4
    usable_gb = ram_gb * 0.75

    n_max = usable_gb * 1024 ** 3 / (elements_alive * bytes_per_element)

    print(f"\n=== Оценка предела in-memory ===")
    print(f"RAM: {ram_gb} ГБ, доступно ~{usable_gb} ГБ")
    print(f"Предел: n ≈ {int(n_max):,}\n")

    for n in [10 ** 6, 10 ** 7, 10 ** 8]:
        gb = 4 * n * bytes_per_element / 1024 ** 3
        status = "OK" if gb < usable_gb else "не влезет"
        print(f"  n = {n:>12,} → {gb:>6.2f} ГБ — {status}")



if __name__ == "__main__":
    main()