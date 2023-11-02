from flask import Flask, request
from committer import Committer
import argparse

app_a = Flask(__name__)
app_b = Flask(__name__)

committer_a = Committer(23123, 16)
committer_b = Committer(23123, 16)


@app_a.route('/get-N', methods=['GET'])
def committer_a_N():
    N = {"N": committer_a.N}
    return N


@app_b.route('/get-N', methods=['GET'])
def committer_b_N():
    N = {"N": committer_b.N}
    return N

# get l, pairs, ys, and W, S from committer_a


@app_a.route('/get-commit', methods=['POST'])
def committer_a_vals():
    h, g = committer_a.compute_g()
    q = committer_a.q_array
    W = committer_a.compute_W()
    u = W[-1]
    assert (u == committer_a.compute_u())

    S = committer_a.compute_rando_seq()

    pairs = committer_a.compute_pairs()
    ys = committer_a.compute_ys(request.get_json()['challenges'])

    values = {'l': committer_a.l, 'pairs': pairs, 'ys': ys,
              'W': W, 'S': S, 'h': h, "g": g, "q_array": q}
    return values


@app_b.route('/get-commit', methods=['POST'])
def committer_b_vals():
    h, g = committer_b.compute_g()
    q = committer_b.q_array
    W = committer_b.compute_W()
    u = W[-1]
    assert (u == committer_b.compute_u())

    S = committer_b.compute_rando_seq()

    pairs = committer_b.compute_pairs()
    ys = committer_b.compute_ys(request.get_json()['challenges'])

    values = {'l': committer_b.l, 'pairs': pairs, 'ys': ys,
              'W': W, 'S': S, 'h': h, "g": g, "q_array": q}
    return values


# get v from committer_a
@app_a.route('/open', methods=['GET'])
def get_committer_a_vprime():
    return {'v_prime': committer_a.compute_vprime()}

# get v_prime from committer_b


@app_b.route('/open', methods=['GET'])
def get_committer_b_vprime():
    return {'v_prime': committer_b.compute_vprime()}


def run_app_a():
    app_a.run(port=5000, debug=True)


def run_app_b():
    app_b.run(port=5001, debug=True)


def main():
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-a", "--runA", default="1")
    args = parser.parse_args()

    if args.runA == "1":
        run_app_a()
    else:
        run_app_b()


main()
