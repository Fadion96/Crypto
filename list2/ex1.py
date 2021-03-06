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
		self.i = 0
		self.j = 0

	def KSA(self):
		s = [i for i in range(self.N)]
		j = 0
		for i in range(self.T + 1):
			j = (j + s[i % self.N] + self.key[i % self.key_length]) % self.N
			s[i % self.N], s[j % self.N] = s[j % self.N], s[i % self.N]
		return s

	def PRGA(self):
		while True:
			self.i = (self.i + 1) % self.N
			self.j = (self.j + self.S[self.i]) % self.N
			self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
			Z = self.S[(self.S[self.i] + self.S[self.j]) % self.N]
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
	parser.add_argument("--number", dest='number', type=int, default=100000000)

	return parser.parse_args()



def main():
	# arguments = parse_arg()
	N_values = [16, 64, 256]
	K_lengths = [40, 64, 128]
	drop_values = [0, 1, 2, 3]
	# N = arguments.N
	# T = N if not arguments.log else int(2 * N * math.log(N))
	# key = generate_key(arguments.key_length)
	# drop = arguments.drop
	# rc4 = RC4(key, N, T, drop)
	# file_name = f'test_{N}_{T}_{arguments.key_length}_{drop}.bin'
	for N in N_values:
		for log in [0,1]:
			for k_len in K_lengths:
				for drop in drop_values:
					T = N if not log else int(2 * N * math.log(N))
					key = generate_key(k_len)
					rc4 = RC4(key, N, T, drop)
					file_name = f'test_{N}_{T}_{k_len}_{drop}.bin'
					print("Doing", file_name)
					with open(file_name, 'wb') as file:
						frame = bytearray()
						for _ in range(10000000):
							test = next(rc4)
							frame.append(test)
						file.write(frame)

if __name__ == '__main__':
	main()
