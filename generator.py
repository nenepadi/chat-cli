#!/user/bin/env python2.7


def generator(num):
    sum = 0
    while  num > 0:
        sum += num
        num -= 1

    return sum


if __name__ == '__main__':
    assert generator(5) == 15
    assert generator(10) == 55
