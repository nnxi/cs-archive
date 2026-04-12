from keyGenerator import keyGenerate
from encryption import Encrypt
from decryption import Decrypt




# 공개 키 역할 (with third party)
class publicKeys:
    def __init__(self, a, b, p, e1, e2):
        self.a = a
        self.b = b
        self.p = p
        self.e1 = e1
        self.e2 = e2




# ---- Bob의 키 생성
(a, b, e1, e2, d, p) = keyGenerate()

# 공개키 등록
# E(a, b), e1, e2는 공개, d는 개인 키
publicKey = publicKeys(a, b, p, e1, e2)




# ---- Alice의 암호화
plainText = input("평문을 입력하세요 : ")

# 공개 키를 이용해 암호화
cypherText = Encrypt(plainText, publicKey.a, publicKey.b, publicKey.p, publicKey.e1, publicKey.e2)




# ---- Bob의 복호화
# 개인 키를 사용하여 복호화
decryptedPlainText = Decrypt(cypherText, d)

print(decryptedPlainText)