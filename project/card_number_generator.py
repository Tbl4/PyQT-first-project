def double(x):
    res = x * 2
    if res > 9:
        res = res - 9
    return res


def luhn_algorithm(card):
    odd = map(lambda x: double(int(x)), str(card)[::2])
    even = map(int, str(card)[1::2])
    return (sum(odd) + sum(even)) % 10 == 0


def process_data(number):
    if luhn_algorithm(number):
        return True
    else:
        pass