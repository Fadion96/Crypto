import secrets
import subprocess

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a,b)])

def main():
    #PARAMS
    key = secrets.randbits(256)
    iv = secrets.randbits(128)
    #QUERY
    # message = secrets.randbits(128)
    # m = message.to_bytes(16,byteorder='big')
    m = secrets.token_bytes(16)
    echo = subprocess.Popen(["echo", "-n", m], stdout=subprocess.PIPE)
    crypto_m = subprocess.check_output(["openssl", "enc", "-aes-256-cbc", "-nosalt", "-K", f"{key}", "-iv", f"{iv.to_bytes(16,byteorder='big').hex()}"], stderr=subprocess.DEVNULL, stdin=echo.stdout)
    #CHALLENGE
    iv_1 = iv + 1
    # m_1 = secrets.randbits(128).to_bytes(16,byteorder='big')
    m_1 = secrets.token_bytes(16)
    m_2 = xor(xor(m,iv.to_bytes(16,byteorder='big')) ,iv_1.to_bytes(16,byteorder='big'))
    m_challenge = secrets.choice((m_1, m_2))
    echo = subprocess.Popen(["echo", "-n", m_challenge], stdout=subprocess.PIPE)
    crypto_challenge = subprocess.check_output(["openssl", "enc", "-aes-256-cbc", "-nosalt", "-K", f"{key}", "-iv", f"{iv_1.to_bytes(16,byteorder='big').hex()}"], stderr=subprocess.DEVNULL, stdin=echo.stdout)
    if crypto_m == crypto_challenge:
        print("m_2 message")
    else:
        print("m_1 message")

if __name__ == '__main__':
    main()
