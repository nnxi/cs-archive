import numpy as np
# np.set_printoptions(threshold=np.inf)

# ---------- 상태, 정책 초기화 ----------

# 상태 0~99
num_states = 100

policy = np.zeros((num_states, num_states))
rewardList = np.zeros((num_states, num_states))

# 0-based 
ladders = {3: 13, 8: 30, 19: 37, 27: 83, 39: 58, 50: 66, 62: 80}
snakes = {16: 6, 88: 25, 63: 59, 94: 74, 98: 77}

# 99는 종료 상태이므로 98까지만 검사
for i in range(99):
    for dice in range(1, 7):
        dest = i + dice
        
        # 99 초과 시 뒤로 튕김
        if dest > 99:
            dest = 99 - (dest - 99)
        
        policy[i][dest] += 1/6

validPaths = policy > 0

print('policy: ')
print(policy)
print('\n')
print('rewardList: ')
print(rewardList)
print('\n')
print('validPaths: ')
print(validPaths)
print('\n')


# 감가율
discountingRate = 0.9

count = 0

while (True) :

    # ---------- 정책 평가 ----------

    # 가치 함수 배열
    V =  np.zeros(num_states)

    while (True):
        delta = 0

        for i in range(num_states - 1):
            v = V[i]
            V[i] = 0.0

            for j in range(num_states):
                if (policy[i][j] > 0):
                    final_dest = j
                    reward = 0

                    if j in ladders: 
                        final_dest = ladders[j]
                        reward = final_dest - j
                    elif j in snakes:
                        final_dest = snakes[j]
                        reward = final_dest - j
                    elif j == 99:
                        final_dest = 99
                        reward = 100
                        
                    V[i] += policy[i][j] * (reward + discountingRate * V[final_dest])

            delta = max(delta, abs(v - V[i]))
        
        if (delta < 0.01):
            break

    print(str(count) + ' 번째 정책으로 나온 가치함수')
    print(V[:99])
    print('\n')

    count += 1

    # ---------- 정책 발전 ----------

    policyStable = True

    for i in range(num_states - 1):
        old_action = policy[i].copy()

        argmax = 0
        maxval = -100000

        for j in range(num_states):
            if (validPaths[i][j]):
                final_dest = j
                reward = 0

                # 뱀이나 사다리가 데려다줄 다음 상태와 그에 따른 보상 계산
                if j in ladders: 
                    final_dest = ladders[j]
                    reward = final_dest - j
                elif j in snakes:
                    final_dest = snakes[j]
                    reward = final_dest - j
                elif j == 99:
                        final_dest = 99
                        reward = 100

                # 각 행동의 큐함수를 통해 새로운 정책이 될 행동을 구함
                q_val = reward + discountingRate * V[final_dest]

                if (q_val > maxval):
                    maxval = q_val
                    argmax = j
                
        for j in range(num_states):
            if (argmax == j):
                policy[i][j] = 1.0
            else:
                policy[i][j] = 0.0

        if np.array_equal(old_action, policy[i]) is False:
            policyStable = False

    if (policyStable is True):
        break


    # ---------- 결과 출력 ----------

final_policy = np.full(num_states, '0')

for i in range(num_states - 1):
    # 사다리나 뱀의 출발 상태는 L과 S를 사용해 표현
    if (i in ladders):
        final_policy[i] = 'L'
    elif (i in snakes):
        final_policy[i] = 'S'
    else:
        for j in range(num_states):
            if policy[i][j] == 1:
                if j > i:
                    final_policy[i] = str(j - i)
                else:
                    final_policy[i] = str((99 - i) + (99 - j)) # 뒤로 튕겨서 나온 결과값 보정

board = final_policy.reshape(10, 10)

print('계산된 최적 정책 :')
for row in board:
    print(' '.join(row))