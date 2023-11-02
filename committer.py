import Crypto.Util.number
import Crypto.Random
import Crypto.Random.random
from Crypto.Util.number import getPrime
from sympy.ntheory.factor_ import totient
import random

from utils.helpers import bitfield, generatePrimes, findOrder


class Committer:
    def __init__(self, M, bits=16):
        # todo: clean
        # SETUP
        self.p1 = getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        while self.p1 % 4 != 3:
            self.p1 = getPrime(bits, randfunc=Crypto.Random.get_random_bytes)

        self.p2 = getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        while self.p2 % 4 != 3:
            self.p2 = getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        self.N = self.p1 * self.p2
        self.bits = bits
        self.k = 30  # TODO: be able to pass this in
        self.M = M
        self.M_bits = bitfield(self.M)
        self.l = len(self.M_bits)
        self.W = []  # squared powers of g
        self.h = random.randrange(0, self.N, 1)

    # STEP 1 COMMIT: create g to send to verifier
    def compute_g(self):
        # generate h in Z_N
        B = 128
        # generate set of all primes less than bound B
        self.q_array = generatePrimes(B)
        q_product = 1

        # compute g
        for q in self.q_array:
            q_product *= q**self.bits

        g = pow(self.h, q_product, self.N)
        self.g = g
        self.q = findOrder(self.g, self.p1, self.p2)

        return self.h, self.g

    def compute_W(self):
        curr_g_power = pow(self.g, 2, self.N)
        self.W.append(curr_g_power)

        # make more efficient
        for i in range(1, self.k + 1):
            a = pow(2, pow(2, i), int(totient(self.N)))
            curr_g_power = pow(self.g, a, self.N)
            self.W.append(curr_g_power)
        return self.W

    # STEP 2 COMMIT: compute u -- not actually used right now in BN_comm, redundant
    def compute_u(self):
        a = pow(2, pow(2, self.k), int(totient(self.N)))
        u = pow(self.g, a, self.N)
        self.u = u
        return self.u

    # STEP 3 COMMIT: compute the random sequence to send to verifier
    # Xor bits of M with the lsb of successive square roots of u mod N

    # todo: debug/check
    def compute_rando_seq(self):
        # convert M to bits, make sure M is a number input
        # TODO: fix, maybe just directly access the bits? instead of using bitfield
        lsbs = []
        u_sqrt = self.W[self.k]
        for i in range(self.l):
            a = pow(2, pow(2, self.k) - i - 1, int(totient(self.N)))
            u_sqrt = pow(self.g, a, self.N)
            u_sqrt_bits = bitfield(u_sqrt)
            u_lsb = u_sqrt_bits[-1]
            lsbs.append(u_lsb)

        S_bits = []

        for i, m_bit in enumerate(self.M_bits):
            S_bits.append(m_bit ^ lsbs[i])

        # self.S = int("".join(str(bit) for bit in S_bits))
        self.S = S_bits
        return self.S

    # redundant
    # STEP 4 COMMIT
    def get_commitment(self):
        return (self.h, self.g, self.W[-1], self.S)

    # STEP 2 ZKP:
    def compute_pairs(self):
        self.As = [random.randrange(0, self.q, 1) for _ in range(self.k + 1)]
        pairs = [(0, 0)]

        for i in range(1, self.k + 1):
            zi = pow(self.g, self.As[i], self.N)
            wi = pow(self.W[i - 1], self.As[i], self.N)
            pairs.append((zi, wi))
        return pairs

    # STEP 4 ZKP:
    def compute_ys(self, challenges):
        ys = [0]
        for i in range(1, self.k + 1):
            yi = (((challenges[i] % self.q) * pow(2, pow(2, i - 1, self.q),
                  self.q) % self.q) + (self.As[i] % self.q)) % self.q
            ys.append(yi)
        return ys

    # todo: might be redundant
    def compute_vprime(self):
        a = pow(2, pow(2, self.k) - self.l, int(totient(self.N)))
        return pow(self.h, a, self.N)
