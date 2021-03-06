from math import gcd
from base64 import b64encode, b64decode

from Cryptodome.Util.number import getPrime as random_prime
from lab4.aes_tests import current_ms, duration_ms

from forbiddenfruit import curse

""" Int extenstion for zfilling.
"""
curse(int, 'zpad', lambda self, zeroes: str(self).zfill(zeroes))


def are_coprimes(prime_a: int, prime_b: int) -> bool:
    return gcd(prime_a, prime_b) == 1


def extended_gcd(a: int, b: int) -> (int, int, int):
    if a == 0: return b, 0, 1

    gcd, a_div_gcd, b_div_gcd = extended_gcd(b % a, a)
    return gcd, b_div_gcd - (b // a) * a_div_gcd, a_div_gcd


class RSA:
    @staticmethod
    def find_random_e(phi: int, bit_size: int = 64) -> int:
        while e := random_prime(bit_size):
            if are_coprimes(phi, e): return e

    @staticmethod
    def find_d(phi: int, e: int) -> int:
        g, x, y = extended_gcd(e, phi)
        return x % phi if g == 1 else None

    @staticmethod
    def generate_keys(extract_phi=False) -> ((int, int), (int, int)):
        p = random_prime(256)
        q = random_prime(256)

        n = p * q
        phi = (p - 1) * (q - 1)

        if extract_phi: return phi

        e = RSA.find_random_e(phi, 512)
        d = RSA.find_d(phi, e)

        return (e, n), (d, n)

    @staticmethod
    def encrypt(message: str, keys: (int, int)) -> bytes:
        e, n = keys

        encrypted = [pow(ord(c), e, n) for c in message]
        as_str = ' '.join([str(i) for i in encrypted])

        return b64encode(as_str.encode('utf8'))

    @staticmethod
    def decrypt(encrypted: bytes, keys: (int, int)) -> str:
        d, n = keys

        as_str = b64decode(encrypted).decode('utf8')
        numbers = [int(i) for i in as_str.split(' ')]

        return ''.join([chr(pow(c, d, n)) for c in numbers])

    @staticmethod
    def test():
        p, q, e = 31, 19, 7
        phi = (p - 1) * (q - 1)

        assert RSA.find_d(phi, e) == 463, "generated keys are invalid"


if __name__ == '__main__':
    start = current_ms()
    public, private = RSA.generate_keys()
    generation_time = duration_ms(start)

    e, n = public
    d, _ = private

    print(f"{generation_time=} [ms]\n{e=}\n{n=}\n{d=}")

    text = "Typowy testowy tekst z polskim znakiem ń."

    encrypted = RSA.encrypt(text, public)
    print(f"[{len(encrypted).zpad(5)} B] {encrypted=}")

    decrypted = RSA.decrypt(encrypted, private)
    print(f"[{len(decrypted).zpad(5)} B] {decrypted=}")
