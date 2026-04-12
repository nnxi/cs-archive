# a, b, p는 고정이라고 가정

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