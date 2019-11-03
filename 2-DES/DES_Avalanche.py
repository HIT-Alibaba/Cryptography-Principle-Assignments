from DESCommon import DES, generate_keys
from DESUtil import add_pads_if_necessary


def get_bits(plaintext):
    text_bits = []
    for i in plaintext:
        text_bits.append(int(i))
    return text_bits


def main():
    keys = generate_keys("lqjxliang")

    plaintext = str(raw_input("Enter the first message to be encrypted\n"))

    text_bits = get_bits(plaintext)
    text_bits = add_pads_if_necessary(text_bits)

    CIPHERS1 = []
    for i in range(0, len(text_bits), 64):
        DES(text_bits, i, (i + 64), keys, CIPHERS1)

    text_bits = []
    plaintext = str(raw_input("Enter the second message to be encrypted\n"))

    text_bits = get_bits(plaintext)
    text_bits = add_pads_if_necessary(text_bits)

    CIPHERS2 = []
    for i in range(0, len(text_bits), 64):
        DES(text_bits, i, (i + 64), keys, CIPHERS2)

    print("for plaintext one:")
    for i in range(16):
        ans = ""
        for each in CIPHERS1[i]:
            ans += str(each)
        print("The cipher after " + str(i) + " rounds is " + ans)

    print("for plaintext two:")
    for i in range(16):
        ans = ""
        for each in CIPHERS2[i]:
            ans += str(each)
        print("The cipher after " + str(i) + " rounds is " + ans)

    for i in range(16):
        count = 0
        for j in range(64):
            if not CIPHERS2[i][j] == CIPHERS1[i][j]:
                count += 1
        print("After " + str(i) + " round differnt bits is: " + str(count))


if __name__ == "__main__":
    main()
