
import sys
import types
import math
import pytest

# Stub millersAlgorithm for import
m = types.ModuleType("millersAlgorithm")
def is_prime_mc(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    i = 3
    while i*i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
m.is_prime_mc = is_prime_mc
sys.modules["millersAlgorithm"] = m

from RSAEncryption import RSA

@pytest.fixture
def rsa():
    return RSA()

def write_small_keys(tmp_path, p=3557, q=2579, e=65537):
    rsa = RSA()
    n = p*q
    phi = (p-1)*(q-1)
    assert math.gcd(e, phi) == 1
    d = rsa.inverse(e, phi)
    (tmp_path/"public.txt").write_text(f"{n}\n{e}\n", encoding="utf-8")
    (tmp_path/"private.txt").write_text(f"{n}\n{d}\n", encoding="utf-8")
    return n,e,d

def fits_into_n(rsa, text, n):
    return rsa.convert_str_to_base10(text, rsa.alphabet2) < n

# convert_base26_to_base10
def test_base26_single_a_is_zero(rsa): assert rsa.convert_base26_to_base10("a")==0
def test_base26_single_z_is_25(rsa): assert rsa.convert_base26_to_base10("z")==25
def test_base26_two_chars_ba_is_26(rsa): assert rsa.convert_base26_to_base10("ba")==26
def test_base26_three_chars_abc(rsa): assert rsa.convert_base26_to_base10("abc")==28
def test_base26_leading_a_no_change(rsa):
    assert rsa.convert_base26_to_base10("a")==rsa.convert_base26_to_base10("aa")

# is_prime behavior
def test_is_prime_below_2(rsa): assert not rsa.is_prime(0) and not rsa.is_prime(1)
def test_is_prime_even_including_2_is_false(rsa):
    assert rsa.is_prime(2) is False and rsa.is_prime(10) is False
def test_is_prime_odd_primes(rsa): assert rsa.is_prime(3) and rsa.is_prime(5) and rsa.is_prime(97)
def test_is_prime_odd_composites(rsa): assert not rsa.is_prime(9) and not rsa.is_prime(21)

# gcd
def test_gcd_basic_pairs(rsa):
    assert rsa.gcd(14,21)==7 and rsa.gcd(21,14)==7
def test_gcd_with_zero(rsa):
    assert rsa.gcd(0,10)==10 and rsa.gcd(10,0)==10
def test_gcd_coprimes(rsa): assert rsa.gcd(35,64)==1

# inverse
def test_inverse_simple_case(rsa):
    inv=rsa.inverse(3,11); assert (3*inv)%11==1
def test_inverse_larger_case(rsa):
    inv=rsa.inverse(17,3120); assert (17*inv)%3120==1
def test_inverse_raises_not_invertible(rsa):
    with pytest.raises(Exception): rsa.inverse(6,9)

# base-N conversions
def test_baseN_roundtrip_simple(rsa):
    s="Hello"; n=rsa.convert_str_to_base10(s,rsa.alphabet2)
    assert rsa.convert_base10_to_str(n,rsa.alphabet2)==s
def test_baseN_roundtrip_with_whitespace(rsa):
    s="line1\nline2\tend"; n=rsa.convert_str_to_base10(s,rsa.alphabet2)
    assert rsa.convert_base10_to_str(n,rsa.alphabet2)==s
def test_baseN_len_and_known_values(rsa):
    assert len(rsa.alphabet2)==70
    assert rsa.convert_base10_to_str(69,rsa.alphabet2)==rsa.alphabet2[-1]
    assert rsa.convert_base10_to_str(70,rsa.alphabet2)==rsa.alphabet2[1]+rsa.alphabet2[0]
    assert rsa.convert_str_to_base10(rsa.alphabet2[1]+rsa.alphabet2[0],rsa.alphabet2)==70
def test_baseN_zero_digit_behavior(rsa):
    a0=rsa.alphabet2[0]
    assert rsa.convert_str_to_base10(a0,rsa.alphabet2)==0
    assert rsa.convert_str_to_base10(a0*2,rsa.alphabet2)==0
    assert rsa.convert_base10_to_str(0,rsa.alphabet2)==a0
def test_convert_str_to_base10_raises_on_unknown_char(rsa):
    with pytest.raises(ValueError):
        rsa.convert_str_to_base10("bad€char", rsa.alphabet2)

# generate_prime uses stub
def test_generate_prime_stubbed(rsa):
    assert rsa.generate_prime(17)==17
    assert rsa.generate_prime(14)==17

# Encrypt/Decrypt integration (numeric equality)
def test_encrypt_decrypt_empty_file(tmp_path, monkeypatch):
    write_small_keys(tmp_path)
    (tmp_path/"input.txt").write_text("", encoding="utf-8")
    rsa=RSA(); monkeypatch.chdir(tmp_path)
    rsa.Encrypt("input.txt","encrypted.txt"); rsa.Decrypt("encrypted.txt","output.txt")
    assert (tmp_path/"output.txt").read_text(encoding="utf-8")==""

def test_encrypt_decrypt_single_char(tmp_path, monkeypatch):
    n,e,d=write_small_keys(tmp_path); plaintext="A"
    rsa=RSA(); assert fits_into_n(rsa, plaintext, n)
    (tmp_path/"input.txt").write_text(plaintext, encoding="utf-8")
    monkeypatch.chdir(tmp_path); rsa.Encrypt("input.txt","encrypted.txt"); rsa.Decrypt("encrypted.txt","output.txt")
    out=(tmp_path/"output.txt").read_text(encoding="utf-8")
    assert RSA().convert_str_to_base10(out, RSA().alphabet2)==RSA().convert_str_to_base10(plaintext,RSA().alphabet2)

def test_encrypt_decrypt_two_chars(tmp_path, monkeypatch):
    n,e,d=write_small_keys(tmp_path); plaintext="Hi"
    rsa=RSA(); assert fits_into_n(rsa, plaintext, n)
    (tmp_path/"input.txt").write_text(plaintext, encoding="utf-8")
    monkeypatch.chdir(tmp_path); rsa.Encrypt("input.txt","encrypted.txt"); rsa.Decrypt("encrypted.txt","output.txt")
    out=(tmp_path/"output.txt").read_text(encoding="utf-8")
    assert RSA().convert_str_to_base10(out, RSA().alphabet2)==RSA().convert_str_to_base10(plaintext,RSA().alphabet2)

def test_encrypt_decrypt_three_chars(tmp_path, monkeypatch):
    n,e,d=write_small_keys(tmp_path); plaintext="Cat"
    rsa=RSA(); assert fits_into_n(rsa, plaintext, n)
    (tmp_path/"input.txt").write_text(plaintext, encoding="utf-8")
    monkeypatch.chdir(tmp_path); rsa.Encrypt("input.txt","encrypted.txt"); rsa.Decrypt("encrypted.txt","output.txt")
    out=(tmp_path/"output.txt").read_text(encoding="utf-8")
    assert RSA().convert_str_to_base10(out, RSA().alphabet2)==RSA().convert_str_to_base10(plaintext,RSA().alphabet2)

def test_encrypt_decrypt_with_newline_and_dot(tmp_path, monkeypatch):
    write_small_keys(tmp_path); plaintext=".\n"
    (tmp_path/"input.txt").write_text(plaintext, encoding="utf-8")
    rsa=RSA(); monkeypatch.chdir(tmp_path)
    rsa.Encrypt("input.txt","encrypted.txt"); rsa.Decrypt("encrypted.txt","output.txt")
    out=(tmp_path/"output.txt").read_text(encoding="utf-8")
    # Leading zero-digit (.) may be dropped; numeric value must match.
    assert RSA().convert_str_to_base10(out, RSA().alphabet2)==RSA().convert_str_to_base10(plaintext,RSA().alphabet2)

def test_encrypt_raises_on_unsupported_char(tmp_path, monkeypatch):
    write_small_keys(tmp_path)
    (tmp_path/"input.txt").write_text("€", encoding="utf-8")
    rsa=RSA(); monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError):
        rsa.Encrypt("input.txt","encrypted.txt")

# Additional property checks
@pytest.mark.parametrize("a,b", [(1,1),(12,18),(100,10),(121,44),(391,17)])
def test_gcd_commutativity_and_divides(rsa, a, b):
    g1=rsa.gcd(a,b); g2=rsa.gcd(b,a)
    assert g1==g2 and a%g1==0 and b%g1==0

@pytest.mark.parametrize("a,n", [(3,10),(7,26),(11,100),(17,3120),(65537, 3120*7+1)])
def test_inverse_correctness_when_coprime(rsa, a, n):
    if math.gcd(a,n)!=1: pytest.skip("not coprime")
    inv=rsa.inverse(a,n); assert (a*inv)%n==1

def test_convert_base10_to_str_then_back_idempotent_on_canonical(rsa):
    for num in [0,1,69,70,71,10**5+1234]:
        s=rsa.convert_base10_to_str(num, rsa.alphabet2)
        back=rsa.convert_str_to_base10(s, rsa.alphabet2)
        assert back==num
