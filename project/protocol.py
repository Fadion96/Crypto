from charm.toolbox.integergroup import IntegerGroupQ, integer
import pdb
from secrets import choice
from functools import reduce

class Client:

    def __init__(self, G, g, id):
        self.id = id
        self.G = G
        self.g = g
        self.x = self.G.random()
        self.g_x = self.g**self.x
        self.proof_x = self.gen_proof(self.x)


    def gen_proof(self, x):
        v = self.G.random()
        g_v = self.g ** v
        h = self.G.hash(self.g, g_v, (self.g ** x), self.id)
        r = (v - x * h)
        return (g_v, r)

    def multiply(self, list):
        return reduce(lambda x, y: x * y, list, integer(1, self.G.p))

    def compute_g_y(self, g_xs):
        before = g_xs[:self.id]
        after = g_xs [self.id + 1:]
        # print(before, after)
        # pdb.set_trace()
        mult_before = self.multiply(before)
        mult_after = self.multiply(after)
        self.g_y = mult_before /  mult_after

    def answer(self):
        self.r = self.G.random()
        if choice((True, False)):
        # if False:
            self.g_c_y = self.g_y ** self.r
            self.proof_c = self.gen_proof(self.r)
        else:
            self.g_c_y = self.g_y ** self.x
            self.proof_c = self.gen_proof(self.x)
        return self.G.hash(self.g_c_y)



def main():
    nr_of_clients = 200
    G = IntegerGroupQ()
    G.paramgen(1024)
    g = G.randomG()
    clients_list = [Client(G, g, i) for i in range(nr_of_clients)]
    for client in clients_list:
        g_v , r = client.proof_x
        g_x, id = client.g_x, client.id
        hash = G.hash(g, g_v, g_x, id)
        assert g_v == (g**r) * (g_x **hash)
    g_xs = [client.g_x for client in clients_list]
    hashes = []
    for client in clients_list:
        client.compute_g_y(g_xs)
        hashes.append(client.answer())
    # print(hashes)
    answers = []
    for client in clients_list:
        assert G.hash(client.g_c_y) == hashes[client.id]
        answers.append(client.g_c_y)
    print(reduce(lambda x, y: x * y, answers, integer(1, G.p)) % G.p)



if __name__ == '__main__':
    main()
