from Crypto.Cipher import AES
import secrets
import hashlib
import multiprocessing

class XSide:

    def __init__(self,number_of_puzzles, constant):
        self.n = number_of_puzzles
        self.c = constant
        self.key_1 = secrets.token_bytes(16)
        self.iv_1 =  hashlib.sha256(self.key_1).digest()[:16]
        self.key_2 = secrets.token_bytes(16)
        self.iv_2 = hashlib.sha256(self.key_2).digest()[:16]
        self.const = secrets.randbits(128).to_bytes(16,byteorder='big')

    def make_puzzles(self,chunk):
        puzzles = []
        for i in range((chunk - 1) * self.n // 4 + 1, chunk * self.n // 4 + 1):
            id = encrypt(self.key_1, self.iv_1, i.to_bytes(16, byteorder='big'))
            key = encrypt(self.key_2, self.iv_2, id)
            random_key = secrets.randbelow(self.c*self.n).to_bytes(16,byteorder='big')
            r_iv = hashlib.sha256(random_key).digest()[:16]
            message =  id + key + self.const
            puzzle = encrypt(random_key, r_iv, message)
            puzzles.append(puzzle)
        return puzzles


    def generate_puzzles(self):
        pool = multiprocessing.Pool(processes=4)
        puzzles = pool.map(self.make_puzzles, [1,2,3,4])
        flatten = lambda l: [item for sublist in l for item in sublist]
        self.puzzles = flatten(puzzles)

    def transmit(self):
        return self.puzzles, self.const

    def receive(self,id):
        self.id = id
        self.key = encrypt(self.key_2, self.iv_2, id)

class YSide:

    def __init__(self,number_of_puzzles, const):
        self.n = number_of_puzzles
        self.c = const

    def receive(self, puzzles, const):
        self.puzzles = puzzles
        self.const = const

    def solve(self):
        selectpuzzle = self.puzzles[secrets.randbelow(self.n)]
        for i in range(self.c * self.n):
            key = i.to_bytes(16,byteorder='big')
            iv = hashlib.sha256(key).digest()[:16]
            message = decrypt(key, iv, selectpuzzle)
            # id = message[:16]
            # k = message[16:32]
            con = message[32:]
            if con == self.const:
                self.id = message[:16]
                self.key = message[16:32]
                break

    def transmit(self):
        return self.id

def encrypt(key,iv, message):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(message)

def decrypt(key, iv, ciphertext):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(ciphertext)


def main():
    x = XSide(2**16,2)
    y = YSide(2**16,2)
    x.generate_puzzles()
    print("Generated")
    y.receive(*x.transmit())
    y.solve()
    x.receive(y.transmit())
    print(x.key)
    print(y.key)


if __name__ == '__main__':
    main()
