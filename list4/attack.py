import lll
import knapsack
import string
import time
from secrets import choice
import numpy as np



def crack_ciphertext(public_key, ciphertext):
    matrix = lll.create_matrix_from_knapsack(public_key, ciphertext)
    reduced_basis = lll.lll_reduction(matrix)
    guess = lll.best_vect_knapsack(reduced_basis)

    if 1 in guess:
        guess = ''.join(str(e) for e in guess)
        chunks = [guess[i:i + 8] for i in range(0, len(guess), 8)]
        message = ''.join([chr(int(b,2)) for b in chunks])
        return message


def test_attack(text):
    message =''.join('{0:08b}'.format(ord(char), 'b') for char in text)
    n = len(message)
    private_key, public_key = knapsack.generate_keys(n)
    cipher = knapsack.encrypt(public_key, text)
    cracked = crack_ciphertext(public_key, cipher)
    # crack_ciphertext(public_key,cipher)
    print(cracked, text)
    success = cracked == text
    return success

def main():
    # text = "a"
    # test_attack(text)
    # num_tests = 100
    # accuracy = {}
    # runtime = {}
    chars = string.ascii_letters + string.digits + string.punctuation
    # for l in range(2, 11):
    #     correct = 0
    #     start = time.time()
    #     for i in range(num_tests):
    random_text = ""
    for _ in range(10):
        random_text += choice(chars)
        test_attack(random_text)
            # if test_attack(random_text):
    #             correct += 1
    #     end = time.time()
    #     accuracy[l] = correct / float(num_tests)
    #     runtime[l] = end - start
    #     print (accuracy[l])
    #     print (runtime[l])


if __name__ == '__main__':
    main()
