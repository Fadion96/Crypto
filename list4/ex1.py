# import pdb
import secrets
import math
import binascii

secretsGenerator = secrets.SystemRandom()
def generate_superincreasing_sequence(number_of_elements):
    sequence = []
    for i in range(number_of_elements):
        start = (((2**i)-1)*2**number_of_elements) + 1
        end = (2**i)*(2**number_of_elements)
        sequence.append(secretsGenerator.randint(start,end))
    # sequence = [secretsGenerator.randint((((2**i)-1)*2**number_of_elements) + 1, (((2**i))*2**number_of_elements)) for i in range(number_of_elements)]
    return sequence

def generate_modulo(sequence):
    seq_sum = sum(sequence)
    modulo = secretsGenerator.randint(seq_sum + 1, 2**(2*(len(sequence)+1)) - 1)
    return modulo

def gen_coprime(modulo):
    coprime = 0
    while not math.gcd(coprime, modulo) == 1:
        coprime = secretsGenerator.randint(2, modulo - 2)
    return coprime

def egcd(a, b):
	if a == 0:
		return b, 0, 1
	else:
		g, x, y = egcd(b % a, a)
		return g, y - (b // a) * x, x


def modinv(b, n):
	g, x, _ = egcd(b, n)
	if g == 1:
		return x % n

def generate_keys(number_of_bits):
    sequence = generate_superincreasing_sequence(number_of_bits)
    modulo = generate_modulo(sequence)
    coprime = gen_coprime(modulo)
    pub_key = [(element * coprime) % modulo for element in sequence]
    return (sequence,modulo,coprime), pub_key

def encrypt(pub_key, message):
    b = ''.join('{0:08b}'.format(ord(char), 'b') for char in message)
    cipher = sum([x if y == '1' else 0 for x,y in zip(pub_key,b)])
    return cipher

def decrypt(priv_key, cipher):
    inverse = modinv(priv_key[2], priv_key[1])
    prim = (cipher*inverse) % priv_key[1]
    message = ''
    for i in priv_key[0][::-1]:
        if prim >= i:
            message = '1' + message
            prim -= i
        else:
            message = '0' + message
    chunks = [message[i:i + 8] for i in range(0, len(message), 8)]
    bits = ''.join([chr(int(b,2)) for b in chunks])
    return bits


def main():
    a = input()
    b = ''.join('{0:08b}'.format(ord(char), 'b') for char in a)
    # print(b)
    priv_key, pub_key = generate_keys(len(b))
    # print("Priv:", priv_key, "\nPub:", pub_key)
    cipher = encrypt(pub_key, a)
    print("Cipher:", cipher)
    message = decrypt(priv_key,cipher)
    print(message)


if __name__ == '__main__':
    main()
    # pdb.set_trace()
