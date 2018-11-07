#!/usr/bin/env python2.7


def merge_sort(array, n):
    sorted_array = []
    n = len(array)

    while True:
        if n == 1:
            return sorted_array
            break
        else:
            halves = divmod(n, 2)
            l1 = array[:halves[0]]
            l2 = array[halves[0]:]

        sorted_array.append(merge_sort(l1, n/2))
        sorted_array.append(merge_sort(l2, n/2))

        n /= 2

if __name__ == '__main__':
    print merge_sort([4, 2, 8, 9, 7, 10, 45, 1], 8)
