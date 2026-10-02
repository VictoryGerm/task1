import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from merge_memory import merge_in_memory
from merge_stream import merge_stream


def test_happy_path():
    a = [1, 3, 5, 7]
    b = [2, 4, 6, 8]
    expected = [1, 2, 3, 4, 5, 6, 7, 8]
    assert merge_in_memory(a, b) == expected
    assert list(merge_stream(a, b)) == expected


def test_empty_first():
    assert merge_in_memory([], [1, 2]) == [1, 2]
    assert list(merge_stream([], [1, 2])) == [1, 2]


def test_empty_second():
    assert merge_in_memory([1, 2], []) == [1, 2]
    assert list(merge_stream([1, 2], [])) == [1, 2]


def test_both_empty():
    assert merge_in_memory([], []) == []
    assert list(merge_stream([], [])) == []


def test_duplicates():
    a = [1, 1, 2, 3]
    b = [1, 2, 2, 4]
    expected = [1, 1, 1, 2, 2, 2, 3, 4]
    assert merge_in_memory(a, b) == expected
    assert list(merge_stream(a, b)) == expected


def test_single_elements():
    assert merge_in_memory([5], [3]) == [3, 5]
    assert list(merge_stream([5], [3])) == [3, 5]