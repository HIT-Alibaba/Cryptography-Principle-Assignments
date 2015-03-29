import random

from DESConstant import s


LINEAR_EXAMPLE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
RANDOM_EXAMPLE = [15, 7, 4, 6, 12, 10, 3, 15, 4, 9, 2, 12, 2, 13, 11, 6, 4, 10, 15, 0, 4, 8, 13, 13, 3, 15, 8, 5, 0, 5, 15, 13, 9, 14, 8, 2, 9, 12, 1, 13, 8, 3, 3, 4, 9, 13, 0, 11, 5, 0, 15, 0, 2, 0, 13, 15, 5, 12, 11, 10, 4, 4, 2, 11]


"""S_BOX_LINEAR = []
S_BOX_RANDOM = []
for i in range(64):
    S_BOX_LINEAR.append(i % 16)
    S_BOX_RANDOM.append(random.randint(0, 15))

print(S_BOX_LINEAR)
print(S_BOX_RANDOM)
"""

def do_s_box(index, _s_box):
    b = [0] * 6
    n = index
    for i in range(6):
        b[5 - i] = n % 2
        n //= 2
    return _s_box[(b[0] * 2 + b[5]) * 16 + b[1] * 8 + b[2] * 4 + b[3] * 2 + b[4]]


def calculate_diff(_s_box):
    diff_table = [[0 for col in range(16)] for row in range(64)]
    for i in range(64):
        for j in range(64):
            in_diff = i ^ j
            out_diff = do_s_box(i, _s_box) ^ do_s_box(j, _s_box)
            diff_table[in_diff][out_diff] += 1
    return diff_table


def main():
    diff_table = calculate_diff(LINEAR_EXAMPLE)
    for i in range(len(diff_table)):
        print(i, diff_table[i])

if __name__ == '__main__':
    main()