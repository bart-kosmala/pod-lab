from Cryptodome.Random.random import getrandbits, randint


class BBS:
    @staticmethod
    def is_probably_prime(num: int, rounds: int) -> bool:
        """
        Implementation of the Miller-Rabin test.
        """
        if num in (2, 3):
            return True

        if num <= 3 or num % 2 == 0:
            return False

        r, d = 0, num - 1

        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(rounds):
            a = randint(2, num - 2)
            x = pow(a, d, num)

            if x in (1, num - 1):
                continue

            for _ in range(r - 1):
                x = pow(x, 2, num)

                if x == num - 1:
                    break
            else:
                return False

        return True

    @staticmethod
    def random_prime(bit_size: int, rounds: int = 40) -> int:
        """
        Generate a random prime number within given bit range.

        :param bit_size: maximum bit size of the prime number
        :param rounds: iterations of the prime probability test (Miller-Robin)
        :return: first probable prime number
        """
        while True:
            num = getrandbits(bit_size)

            if BBS.is_probably_prime(num, rounds):
                return num

    @staticmethod
    def is_congrugent(a: int, b: int, n: int) -> bool:
        return (a - b) % n == 0

    @staticmethod
    def valid_prime(bit_size: int) -> int:
        """
        Generate a prime number that is BBS algorithm valid.
        """
        while True:
            num = BBS.random_prime(bit_size)

            if BBS.is_congrugent(num, 3, 4):
                return num

    @staticmethod
    def greatest_common_divisor(a: int, b: int) -> int:
        """
        Euclides recursive algorithm for finding the greatest common divisor of two integers.
        """
        return a if b == 0 else BBS.greatest_common_divisor(b, a % b)

    @staticmethod
    def generate(length: int, bit_size: int = 512, preseed: int = None) -> list[bool]:
        """
        Generate random bit series using the BBS algorithm.

        :param length: length of the output series
        :param bit_size: maximum bit size of the prime numbers used to generate the Blum number
        :param preseed: preinitialize Blum number's value
        :return: generated series
        """

        blum_number = 0

        if preseed is not None:
            blum_number = preseed

        else:
            prime1 = BBS.valid_prime(bit_size)
            prime2 = BBS.valid_prime(bit_size)

            blum_number = prime1 * prime2

        x = 0

        while BBS.greatest_common_divisor(x, blum_number) != 1 and x != blum_number:
            x = randint(1, blum_number)

        result = []
        elem = pow(x, 2, blum_number)

        for _ in range(length):
            result += [bin(elem)[-1] == '1']

            elem = pow(elem, 2, blum_number)

        return result
