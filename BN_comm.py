import Crypto.Util.number, Crypto.Random, Crypto.Random.random
from committer import Committer
from verifier import Verifier
from utils.helpers import getOrderCorrect, bitfield

class BonehNaorCommitmentScheme:

    # M -- message
    # R -- security parameter
    # bits -- number of bits in primes p1 and p2
    # todo: restructure to get rid of M, and just have M in the committer
    def __init__(self, M, R, bits=16): 
        self.committer = Committer(M, bits)
        self.verifier = Verifier(R, self.committer.N, bits)
        # todo: get rid of this in the committer
        self.M_bits = bitfield(M)
        self.l = len(self.M_bits)
        self.S = []

    def commit(self): 
        # ----- STEP 1 -----
        # committer generate g 
        # todo: weird behaviour, sometimes g is 1, sometimes it works
        h, g = self.committer.compute_g()

        print("order", self.committer.q)
        # print(getOrderCorrect(g, self.committer.N))

        # verifier verify g
        assert(self.verifier.verify_g(h, g, self.committer.q_array))
        print("verified g!")

        # ----- STEP 2, STEP 3  -----
        self.W = self.committer.compute_W()
        u = self.W[-1]
        assert(u == self.committer.compute_u())
        print("computed W")

        self.S = self.committer.compute_rando_seq() 
        print("computed S")

        # ----- STEP 4 ----- ZKP
        challenges = self.verifier.gen_challenges(self.committer.k)
        print("challenges")
        pairs = self.committer.compute_pairs()
        print("pairs")
        ys = self.committer.compute_ys(challenges)

        assert(self.verifier.verify_zkp(self.committer.l, pairs, ys, self.W))
    
    def open(self): 
        v_prime = self.committer.compute_vprime()
        W_elem = self.W[len(self.W) - self.l]
        v = self.verifier.compute_v(self.l, v_prime)
        # check that verifier computed v == k - lth element of W
        M_seq = self.verifier.open_message(self.l, self.S)

        M = int("".join(str(bit) for bit in M_seq), 2)
        assert (M == self.committer.M)
    
    def forced_open(self):
        v = self.verifier.forced_compute_v(self.l)
        M_seq = self.verifier.open_message(self.l, self.S)
        M = int("".join(str(bit) for bit in M_seq), 2)
        assert (M == self.committer.M)
        
def main():
    # todo: set R
    scheme = BonehNaorCommitmentScheme(23123, 40)
    scheme.commit()
    scheme.open()
    scheme.forced_open()

main()
        


# class BonehNaorCommitmentScheme:
# 	def __init__(self, n=16):
# 		# generate p1 and p1, n bit primes
#         p1 = Crypto.Util.number.getPrime(n, randfunc=Crypto.Random.get_random_bytes)
# 		p2 = Crypto.Util.number.getPrime(n, randfunc=Crypto.Random.get_random_bytes)
#         self.N = p1 * p2
		
#     def generate_N(self, n=16): 
# 		continue 
	
	
# 	# Commit to a value
# 	def commit(x: int):
# 		# compute g
		
# 		continue

# 	# Open a commitment
# 	def open(comm):
# 		...

# 	# Force an opening
# 	def forced_open(comm):
# 		...