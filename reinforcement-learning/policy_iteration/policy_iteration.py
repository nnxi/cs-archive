import numpy as np

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

validPaths = policy > 0

print('초기 정책')
print(policy)
print('\n')

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

count = 0

while (True) :

    # ---------- 정책 평가 ----------

    # 가치 함수 배열
    V =  np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    while (True) :
        delta = 0

        for i in range(9) :
            v = V[i]
            V[i] = np.sum(policy[i] * (rewardList[i] + discountingRate * V))
            delta = max(delta, abs(v - V[i]))
        
        if (delta < 0.01) :
            break

    print(str(count) + ' 번째 정책으로 나온 가치함수')
    print(V[:9])
    print('\n')

    count += 1

    # ---------- 정책 발전 ----------

    policyStable = True

    for i in range(9) :
        old_action = policy[i].copy()

        argmax = 0
        maxval = -100000

        for j in range(10) :
            if (validPaths[i][j]) :
                if (maxval < rewardList[i][j] + discountingRate * V[j]) :
                    maxval = rewardList[i][j] + discountingRate * V[j]
                    argmax = j
        
        for j in range(10) :
            if (argmax == j) :
                policy[i][j] = 1
            else :
                policy[i][j] = 0

        if np.array_equal(old_action, policy[i]) is False :
            policyStable = False

    if (policyStable is True) :
        break

    
    # ---------- 결과 출력 ----------
    
print('계산된 최적 정책 :')
print(policy)