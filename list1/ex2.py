import subprocess

class Cracker(object):

	def __init__(self, data):
		self.data = [None] * 344
		self.data += self.create_possible_rvalues(data)
		self.first_value = data[0]

	def create_possible_rvalues(self, data):
		r_values = [[value * 2, value * 2 + 1] for value in data]
		return r_values

	def find_possible_seeds(self):
		for i in range(12):
			for j in range(372 - (31 * i), (339 - (28 * i) -1 ), -3):
				if self.data[j] is None:
					self.data[j] = subtract_r(self.data[j + 31], self.data[j + 28])

		return [value % 2**31 for value in self.data[31]]

	def find_seed(self, possible_seeds):
		for seed in possible_seeds:
			possible_first = call_generator(1, seed)
			if possible_first[0] == self.first_value:
				print(f"Found seed: {seed}")
				ret = call_generator(60, seed)
				print(ret)

def load_data():
	data = []
	with open("generated.txt", 'r') as file:
		for line in file:
			data.append(int(line.strip()))
	return data

def subtract_r(previous, latter):
	possible_r_values = []

	for p in previous:
		for l in latter:
			value = p - l
			possible_r_values.append(value)

	return list(set(possible_r_values))


def call_generator(size, seed):
	proc = subprocess.Popen(
		['./random', str(size), str(seed)], stdout=subprocess.PIPE)
	out, _ = proc.communicate()
	return [int(num) for num in out.decode('utf-8').split('\n') if num]


def main():
	data = load_data()
	cracker = Cracker(data)
	possible_seeds = cracker.find_possible_seeds()
	cracker.find_seed(possible_seeds)

if __name__ == "__main__":
	main()
