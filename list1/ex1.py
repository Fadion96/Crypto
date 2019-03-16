from functools import reduce
from math import gcd

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

class Cracker(object):

	def __init__(self, states):
		self.states = states

	def find_unknown_increment(self, modulus, multiplier):
		increment = (self.states[1] - self.states[0] * multiplier) % modulus
		return increment

	def find_unknown_multiplier(self, modulus):
		multiplier = (((self.states[2] - self.states[1]) % modulus) * modinv( (self.states[1] - self.states[0]) % modulus, modulus)) % modulus
		return multiplier

	def find_unknown_modulus(self):
		diffs = [s1 - s0 for s0, s1 in zip(self.states, self.states[1:])]
		mod_zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
		modulus = abs(reduce(gcd, mod_zeroes))
		return modulus

	def crack_lcg(self):
		modulus = self.find_unknown_modulus()
		multiplier = self.find_unknown_multiplier(modulus)
		increment = self.find_unknown_increment(modulus, multiplier)
		return modulus, multiplier, increment

	def predict_next(self, modulus, multiplier, increment):
		next = (self.states[-1] * multiplier + increment) % modulus
		self.states.append(next)
		print(next)

def test():
	gen = LCG(123)
	# states = [1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492, 596516649, 1189641421]

	states = [1103527590, 377401575, 662824084, 1147902781, 2035015474, 368800899, 1508029952, 486256185, 1062517886, 267834847]
	# for i in range(10):
	    # states.append(next(gen))
	print(states)
	cracker = Cracker(states)
	a,b,c = cracker.crack_lcg()
	print(a,b,c)
	cracker.predict_next(a,b,c)
	# print(next(gen))



if __name__ == '__main__':
	test()
