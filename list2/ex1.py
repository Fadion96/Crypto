import random
import math
import argparse

class RC4(object):
	def __init__(self, key, N, T, D):
		self.key = key
		self.N = N
		self.T = T
		self.key_length = len(key)
		self.S = self.KSA()
		self.D = D

	def KSA(self):
		s = [i for i in range(self.N)]
		j = 0
		for i in range(self.T + 1):
			j = (j + s[i % self.N] + self.key[i % self.key_length]) % self.N
			s[i % self.N], s[j % self.N] = s[j % self.N], s[i % self.N]
		return s

	def PRGA(self):
		i = j = 0
		while True:
			i = (i + 1) % self.N
			j = (j + self.S[i]) % self.N
			self.S[i], self.S[j] = self.S[j], self.S[i]
			Z = self.S[(self.S[i] + self.S[j]) % self.N]
			yield Z

	def __iter__(self):
		return self

	def __next__(self):
		for _ in range(self.D):
			next(self.PRGA())
		return next(self.PRGA())

def generate_key(key_length):
	return [random.getrandbits(8) for _ in range(key_length)]

def parse_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument("--log", dest='log', action='store_true')
	parser.add_argument("--N", dest='N', type=int, default=16)
	parser.add_argument("--key-length", dest='key_length', type=int, default=40)
	parser.add_argument("--drop", dest='drop', type=int, default=0)
	parser.add_argument("--number", dest='number', type=int, default=10)

	return parser.parse_args()



def main():
	arguments = parse_arg()
	N = arguments.N
	T = N if not arguments.log else int(2 * N * math.log(N))
	key = generate_key(arguments.key_length)
	drop = arguments.drop
	rc4 = RC4(key, N, T, drop)
	for _ in range(arguments.number):
		print(next(rc4))

if __name__ == '__main__':
	main()
