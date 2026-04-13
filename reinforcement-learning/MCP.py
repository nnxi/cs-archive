import numpy as np
np.set_printoptions(linewidth=np.inf, precision=3, suppress=True)

# 배열 중 (i, j)가 있을 때, 상태 i에서 상태 j로 가는 행동을 뜻한다.

# 초기 정책. s9는 종료 상태
policy = np.array([
    [0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0],
    [0.4, 0, 0.3, 0, 0, 0, 0, 0, 0.3, 0],
    [0, 0, 0, 0.8, 0, 0.2, 0, 0, 0, 0],
    [0.6, 0, 0, 0, 0.4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0.4, 0.3, 0.3, 0],
    [0, 0, 0, 0, 0.2, 0, 0, 0.4, 0, 0.4],
    [0, 0, 0, 0, 0, 0, 0.2, 0, 0, 0.8],
    [0, 0, 0, 0, 0, 0, 0, 0.6, 0.4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# 각 행동에 따른 보상
rewardList = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, -1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, -1, -2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# 감가율
discountingRate = 0.9

# 각 상태의 가치함수를 저장할 배열
V = np.zeros(10)
visitTimes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Returns = np.zeros(10)

def generateEp():
    ep = []
    current = 0

    # S0부터 출발
    firstStep = [0, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ep.append((current, rewardList[0, 0]))

    count = 1
    while current != 9:
        # 각 행의 확률에 맞게 다음 상태 랜덤으로 지정
        candidates = np.arange(len(policy[current]))
        next = np.random.choice(candidates, 1, p=policy[current])[0]

        ep.append((next, rewardList[current, next]))

        if firstStep[next] == -1:
            firstStep[next] = count

        current = next

        # 사이클에 갇혔을 경우 탈출하고 재시도
        count += 1
        if count > 100000:
            return None, None

    return ep, firstStep

for t in range(1, 1000001):
    # 에피소드 생성
    ep, firstStep = generateEp()

    if ep is None:
        continue

    G = 0
    curStep = len(ep) - 1

    nextReward = ep[-1][1]
    
    # 마지막 종료 상태를 슬라이스 하고 역으로 for문 실행
    for i in reversed(ep[:-1]):
        G = G * discountingRate + nextReward
        curStep -= 1

        # 첫 번째 방문일 때만 가치함수에 적용
        if curStep == firstStep[i[0]]:
            Returns[i[0]] += G
            visitTimes[i[0]] += 1
            V[i[0]] = Returns[i[0]] / visitTimes[i[0]]

        nextReward = i[1]

    # 아래로 과정, 결과 출력문
    if t == 100:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 500:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 1000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 5000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 10000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 50000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 100000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 500000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)
    elif t == 1000000:
        print('\n', str(t), '번째 예측된 가치함수:')
        print(V)