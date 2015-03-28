import random

from DESCommon import DES, generate_keys
from DESUtil import add_pads_if_necessary

def main():
    keys = generate_keys("lqjxliang")

    plaintext_list = []
    ciphertext_list = []
    for i in range(256):
        t = [1]
        diff = random.randint(1, 63)
        for j in range(63):
            if j == diff:
                t.append(1)
            else:
                t.append(0)

        plaintext_list.append(t)

    for plaintext in plaintext_list:
        ciphertext_list.append(DES(plaintext, 0, 64, keys))

    # Do statistics
    count = []
    rate = []
    for i in range(64):
        t = 0
        for ciphertext in ciphertext_list:
            if ciphertext[i] == '0':
                t += 1
        count.append(t)
        rate.append(t / 256.0)
    print(count)
    print(rate)

if __name__ == "__main__":
    main()
