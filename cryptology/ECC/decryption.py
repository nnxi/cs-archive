def Decrypt(cypherText, d):

    # 평문이 담길 문자열 선언
    plainText = ''

    # c1, c2 두 개씩 뽑아서 P 계산
    for i in range(0, len(cypherText), 2):
        c1 = cypherText[i]
        c2 = cypherText[i + 1]

        p = c2.sub(c1.mul(d))

        # 확률적 인코딩 기법을 썼기 때문에 100으로 나눈 정수를 취함
        ascii_code = p.x // 100 

        # 아스키코드를 문자로 변환 후 문자열에 더함
        plainText += chr(ascii_code)

    return plainText