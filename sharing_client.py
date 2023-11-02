import requests
from verifier import Verifier


def verify_and_open(verifier, challenges, url):
    r = requests.post(url + "get-commit", json={"challenges": challenges})
    res = r.json()

    verifier.verify_g(res['h'], res['g'], res['q_array'])

    verifier.verify_zkp(res['l'], res['pairs'], res['ys'], res['W'])

    r2 = requests.get(url + "open")
    res2 = r2.json()

    v = verifier.compute_v(res['l'], res2['v_prime'])
    m = verifier.open_message(res['l'], res['S'])
    return m


def verify_and_force_open(verifier, challenges, url):
    r = requests.post(url + "get-commit", {"challenges": challenges})
    res = r.json()

    verifier.verify_g(res['h'], res['g'], res['q_array'])

    verifier.verify_zkp(res['l'], res['pairs'], res['ys'], res['W'])

    verifier.forced_compute_v(res['l'])


def main():
    res_a = requests.get("http://127.0.0.1:5000/get-N")
    a_N = res_a.json()["N"]
    res_b = requests.get("http://127.0.0.1:5001/get-N")
    b_N = res_b.json()["N"]

    verifier_a = Verifier(40, b_N, 16)
    verifier_b = Verifier(40, a_N, 16)

    # to send to committer b
    challenges_a = verifier_a.gen_challenges(verifier_a.k)

    # to send to committer a
    challenges_b = verifier_b.gen_challenges(verifier_b.k)

    opened_a_share = verify_and_open(
        verifier_b, challenges_b, "http://127.0.0.1:5000/")
    opened_b_share = verify_and_open(
        verifier_a, challenges_a, "http://127.0.0.1:5001/")

    answer_a = int("".join(str(bit) for bit in opened_b_share), 2) + 23123
    answer_b = int("".join(str(bit) for bit in opened_a_share), 2) + 23123

    assert (answer_a == answer_b)


main()
