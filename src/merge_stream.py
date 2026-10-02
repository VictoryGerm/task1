from sources import stream_source


def merge_stream(a, b):
    stream_a = stream_source(a)
    stream_b = stream_source(b)

    value_a = next(stream_a, None)
    value_b = next(stream_b, None)

    while value_a is not None and value_b is not None:
        if value_a <= value_b:
            yield value_a
            value_a = next(stream_a, None)
        else:
            yield value_b
            value_b = next(stream_b, None)

    while value_a is not None:
        yield value_a
        value_a = next(stream_a, None)

    while value_b is not None:
        yield value_b
        value_b = next(stream_b, None)