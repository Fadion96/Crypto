from functools import reduce
from math import gcd


class LCG(object):
	multi = 1103515245
	inc = 12345
	mod = 2**31

	def __init__(self, seed):
		self.state = seed

	def __iter__(self):
		return self

	def __next__(self):
		self.state = (self.state * self.multi + self.inc) % self.mod
		return self.state


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


def crack_unknown_increment(states, modulus, multiplier):
	increment = (states[1] - states[0] * multiplier) % modulus
	return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
	multiplier = (((states[2] - states[1]) % modulus) * modinv( (states[1] - states[0]) % modulus, modulus)) % modulus
	return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
	diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
	zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
	modulus = abs(reduce(gcd, zeroes))
	return crack_unknown_multiplier(states, modulus)


def test():
	gen = LCG(123)
	states = [1103527590, 377401575, 662824084, 1147902781, 2035015474, 368800899, 1508029952, 486256185, 1062517886, 267834847]
	# for i in range(10):
	#     states.append(next(gen))
	print(states)
	print(crack_unknown_modulus(states))


if __name__ == '__main__':
	test()
