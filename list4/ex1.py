import knapsack

def main():
    a = input()
    b = ''.join('{0:08b}'.format(ord(char), 'b') for char in a)
    # print(b)
    priv_key, pub_key = knapsack.generate_keys(len(b))
    cipher = knapsack.encrypt(pub_key, a)
    print("Cipher:", cipher)
    message = knapsack.decrypt(priv_key,cipher)
    print(message)


if __name__ == '__main__':
    main()
    # pdb.set_trace()
