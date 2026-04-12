from point import Point
import random


def Encrypt(plainText, a, b, p, e1, e2):
    # 평문에 대응되는 점 찾기
    # 확률적 인코딩 기법 사용, 아스키코드가 기준

    # 각 평문에 대응되는 점이 담길 배열 (127개)
    arr = []

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

    # 암호화

    # 암호문이 담길 배열 선언
    cypherText = []

    for t in plainText:

        # 무작위 정수 r 선택
        r = random.randint(1, 115792089237316195423570985008687907852837564279074904382605163141518161494337)

        c1 = e1.mul(r)
        c2 = arr[ord(t)].add(e2.mul(r))

        # 암호문 배열에 추가
        cypherText.append(c1)
        cypherText.append(c2)

    return cypherText