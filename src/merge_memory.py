def merge_in_memory(a, b):
    result = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i = i + 1
        else:
            result.append(b[j])
            j = j + 1

    while i < len(a):
        result.append(a[i])
        i = i + 1

    while j < len(b):
        result.append(b[j])
        j = j + 1

    return result