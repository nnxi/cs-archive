import random




# ----------------------------------------------------Point class 및 기본 연산 선언
# Point class 선언
class Point:
    def __init__(self, x, y, a, b, p):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.p = p

        if self.x == None and self.y == None:
            return

    # 점끼리의 덧셈
    def add(self, other):

        # 두 점 중 하나가 무한 원점일 때
        if self.x is None: return other
        if other.x is None: return self

        # 자신과 자신의 역원을 더할 때
        if self.x == other.x and (self.y + other.y) % self.p == 0:
            return Point(None, None, self.a, self.b, self.p)
        
        # 기울기 계산
        # 1. 자신과 같은 점을 더할 때
        if self.x == other.x and self.y == other.y:
            slope = (3 * pow(self.x, 2, self.p) + self.a) * pow((2 * self.y), -1, self.p)

        # 2. 자신과 다른 점을 더할 때
        else :
            slope = ((other.y - self.y) % self.p) * pow(((other.x - self.x) % self.p), -1, self.p) 

        # 오버플로 방지
        slope %= self.p

        # 반환할 새로운 점 좌표 계산
        newX = (pow(slope, 2, self.p) - self.x - other.x) % self.p
        newY = (slope * (self.x - newX) - self.y) % self.p

        return Point(newX, newY, self.a, self.b, self.p)
    

    # 점끼리의 뺄셈
    def sub(self, other):
        # 먼저 other의 역원 구하기
        # 덧셈에 대한 역원이기 때문에 -1만 곱하기
        temp = Point(other.x, other.y * -1 + other.p, other.a, other.b, other.p)

        # 역원을 더하기
        return self.add(temp)
    
    
    # 점에 상수를 곱할 때 (고속 지수 연산 이용)
    def mul(self, n):

        # 곱하는 수를 이진수로 변환 후 반전
        binary = bin(n)[2:][::-1]

        # 연산에 필요한 변수 선언
        res = Point(None, None, self.a, self.b, self.p)
        temp = self

        # 이진수 문자열에서 0이면 x2, 1이면 x2 후 res에 덧셈
        for flag in binary:
            if flag == '1':
                res = res.add(temp)
            
            temp = temp.add(temp)

        return res
    


    

# ----------------------------------------------------키 생성 함수
# 타원 곡선은 secp256k1 곡선 사용
a = 0
b = 7
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663

# 공개 키와 개인 키 생성
def keyGenerate():
    print("-" * 60)
    print("[1] 키 생성(Key Generation) 시작...")

    # secp256k1에서 정해둔 점 e1의 좌표값
    e1_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    e1_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

    e1 = Point(e1_x, e1_y, a, b, p)
    print(f"  -> 기준점 e1 설정 완료")

    # 정수 d를 하나 랜덤하게 선택
    d = random.randint(1, 115792089237316195423570985008687907852837564279074904382605163141518161494337)
    print(f"  -> Bob의 개인키 d 생성 (Random): {d}")

    # e2를 계산
    e2 = e1.mul(d)
    print(f"  -> Bob의 공개키 e2 계산 완료 (d * e1): ({e2.x}, {e2.y})")
    print("[1] 키 생성 완료")

    return a, b, e1, e2, d, p





# ----------------------------------------------------암호화 함수
def Encrypt(plainText, a, b, p, e1, e2):
    print("\n" + "-" * 60)
    print(f"[2] 암호화(Encryption) 시작... 평문: \"{plainText}\"")

    # 평문에 대응되는 점 찾기
    # 확률적 인코딩 기법 사용, 아스키코드가 기준

    # 각 평문에 대응되는 점이 담길 배열 (127개)
    arr = []
    print("  -> 평문 인코딩 배열 생성 중...", end="")

    for i in range(128):

        # 확률적 인코딩을 위해 범위를 100으로 설정
        for x in range(i * 100, i * 100 + 100):

            w = (pow(x, 3, p) + a * x + b) % p

            # 정수 제곱근이 존재하는지 판별
            y = pow(w, ((p + 1) // 4), p)

            # 정수 제곱근이 존재한다면 점을 배열에 추가하고 반복문 탈출
            if (y * y) % p == w:
                arr.append(Point(x, y, a, b, p))
                break
    print(" 완료")

    # 암호화

    # 암호문이 담길 배열 선언
    cypherText = []
    
    print("  -> 글자별 암호화 진행:")
    count = 1
    for t in plainText:

        # 무작위 정수 r 선택
        r = random.randint(1, 115792089237316195423570985008687907852837564279074904382605163141518161494337)

        c1 = e1.mul(r)
        c2 = arr[ord(t)].add(e2.mul(r))

        # 암호문 배열에 추가
        cypherText.append(c1)
        cypherText.append(c2)

        print(f"    [{count}] 문자 '{t}' 암호화:")
        print(f"       난수 r: {r}")
        print(f"       C1 (r*e1): ({c1.x}, {c1.y})")
        print(f"       C2 (M+r*e2): ({c2.x}, {c2.y})")
        count += 1

    print("[2] 암호화 완료")
    return cypherText





# ----------------------------------------------------복호화 함수
def Decrypt(cypherText, d):
    print("\n" + "-" * 60)
    print("[3] 복호화(Decryption) 시작...")

    # 평문이 담길 문자열 선언
    plainText = ''

    # c1, c2 두 개씩 뽑아서 P 계산
    count = 1
    for i in range(0, len(cypherText), 2):
        c1 = cypherText[i]
        c2 = cypherText[i + 1]

        p = c2.sub(c1.mul(d))

        # 확률적 인코딩 기법을 썼기 때문에 100으로 나눈 정수를 취함
        ascii_code = p.x // 100 

        # 아스키코드를 문자로 변환 후 문자열에 더함
        char_val = chr(ascii_code)
        plainText += char_val

        print(f"    [{count}] 암호문 쌍 복호화 -> 복원된 점 P: ({p.x}, {p.y}) -> 문자: '{char_val}'")
        count += 1

    print("[3] 복호화 완료")
    return plainText


class publicKeys:
    def __init__(self, a, b, p, e1, e2):
        self.a = a
        self.b = b
        self.p = p
        self.e1 = e1
        self.e2 = e2





# ----------------------------------------------------main함수
# ---- Bob의 키 생성
(a, b, e1, e2, d, p) = keyGenerate()

# 공개키 등록
# E(a, b), e1, e2는 공개, d는 개인 키
publicKey = publicKeys(a, b, p, e1, e2)


# ---- Alice의 암호화
plainText = 'I love Cryptography! ^_^'

# 공개 키를 이용해 암호화
cypherText = Encrypt(plainText, publicKey.a, publicKey.b, publicKey.p, publicKey.e1, publicKey.e2)


# ---- Bob의 복호화
# 개인 키를 사용하여 복호화
decryptedPlainText = Decrypt(cypherText, d)

# ---- 결과 확인
print("\n" + "=" * 60)
print(f"최종 결과 확인:")
print(f"  원본 평문   : {plainText}")
print(f"  복호화된 평문: {decryptedPlainText}")