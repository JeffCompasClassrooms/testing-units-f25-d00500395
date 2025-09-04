import math
import random
from millersAlgorithm import is_prime_mc

class RSA:
    alphabet1 = "abcdefghijklmnopqrstuvwxyz"
    alphabet2 = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self):
        self.n = None
        self.e = None
        self.d = None

    def convert_base26_to_base10(self, text):
        result = 0
        for char in text:
            result = result * 26 + self.alphabet1.index(char)
        return result

    def is_prime(self, num):
        if num < 2:
            return False
        if num % 2 == 0:
            return False
        for i in range(3, int(math.isqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def inverse(self,a, n):
        t, newt = 0, 1
        r, newr = n, a
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        if r > 1:
            raise Exception("a is not invertible")
        if t < 0:
            t = t + n
        return t

    def generate_prime(self, num):
        if num % 2 == 0:
            num += 1
        while not is_prime_mc(num):
            num += 2
        return num

    def GenerateKeys(self, str1, str2):
        p = self.convert_base26_to_base10(str1)
        q = self.convert_base26_to_base10(str2)

        if p < 10**200 or q < 10**200:
            print("Error: Input strings are too short.")
            exit()

        p %= 10**200
        q %= 10**200

        p = self.generate_prime(p)
        q = self.generate_prime(q)

        n = p * q
        r = (p - 1) * (q - 1)

        e = 10**398 + 1
        while self.gcd(e, r) != 1:
            e += 2

        d = self.inverse(e, r)

        with open("public.txt", "w") as f:
            f.write(str(n) + "\n")
            f.write(str(e) + "\n")

        with open("private.txt", "w") as f:
            f.write(str(n) + "\n")
            f.write(str(d) + "\n")

    def convert_str_to_base10(self, text, alphabet):
        result = 0
        for char in text:
            result = result * len(alphabet) + alphabet.index(char)
        return result

    def convert_base10_to_str(self, num, alphabet):
        if num == 0:
            return alphabet[0]
        result = ""
        base = len(alphabet)
        while num > 0:
            result = alphabet[num % base] + result
            num //= base
        return result

    def Encrypt(self, inputfile, outputfile):
        with open("public.txt", "r") as f:
            n = int(f.readline().strip())
            e = int(f.readline().strip())

        with open(inputfile, "rb") as fin:
            PlainTextBinary = fin.read()
            PlainText = PlainTextBinary.decode("utf-8")

        blocks = [PlainText[i:i+216] for i in range(0, len(PlainText), 216)]
        for idx, block in enumerate(blocks):
            print(f"Encrypt Block {idx}: {len(block)} characters")

        encrypted_text = ""
        for block in blocks:
            number = self.convert_str_to_base10(block, self.alphabet2)
            cipher = pow(number, e, n)
            encoded = self.convert_base10_to_str(cipher, self.alphabet2)
            encrypted_text += encoded + "$"

        with open(outputfile, "wb") as fout:
            fout.write(encrypted_text.encode("utf-8"))

    def Decrypt(self, inputfile, outputfile):
        with open("private.txt", "r") as f:
            n = int(f.readline().strip())
            d = int(f.readline().strip())

        with open(inputfile, "rb") as fin:
            EncryptedTextBinary = fin.read()
            EncryptedText = EncryptedTextBinary.decode("utf-8")

        encrypted_blocks = EncryptedText.split("$")
        encrypted_blocks = encrypted_blocks[:-1]

        decrypted_text = ""
        for idx, block in enumerate(encrypted_blocks):
            number = self.convert_str_to_base10(block, self.alphabet2)
            plain = pow(number, d, n)
            decoded = self.convert_base10_to_str(plain, self.alphabet2)
            print(f"Decrypt Block {idx}: {len(decoded)} characters BEFORE padding")

            # (Optional) Padding logic here if needed
            decrypted_text += decoded

        with open(outputfile, "wb") as fout:
            fout.write(decrypted_text.encode("utf-8"))

def main():
    rsa = RSA()
    
    # Two very long strings for prime generation
    str1 = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    str2 = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

    rsa.GenerateKeys(str1, str2)

    # Create a test input file
    test_plaintext = ("Hello World! This is a test message designed to be very long..\n" * 20)
    with open("input.txt", "wb") as f:
        f.write(test_plaintext.encode("utf-8"))

    # Encrypt and Decrypt
    rsa.Encrypt("input.txt", "encrypted.txt")
    rsa.Decrypt("encrypted.txt", "output.txt")

    # Verify correctness
    with open("input.txt", "rb") as f1, open("output.txt", "rb") as f2:
        original = f1.read()
        decrypted = f2.read()
        if original == decrypted:
            print("Success: Decrypted text matches original!")
        else:
            print("Error: Decrypted text does not match.")

if __name__ == "__main__":
    main()
