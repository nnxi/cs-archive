import random as rd
import numpy as np
import matplotlib.pyplot as plt


# ----- data set 생성 -----
dataSet = []
xSet = []
ySet = []
for _ in range(300):
    x = rd.uniform(0, 3)

    y = x**3 - 4.5*x**2 + 6 * x + 2 + rd.uniform(-0.5, 0.5)

    dataSet.append((x, y))
    xSet.append(x)
    ySet.append(y)

# numpy 행렬로 변환
X = np.array(xSet)
Y = np.array(ySet)


# ----- 경사하강 로직 -----
def linear_regression(X, y, x_current = 0, s_current = 0, m_current = 0, b_current = 0, epochs = 100000, learning_rate = 0.01):
    N = float(len(y))

    for i in range(epochs):
        y_current = (x_current * X**3) + (s_current * X**2) + (m_current * X) + b_current

        cost  = sum([data**2 for data in (y - y_current)]) / (2 * N)

        #계산된 미분식
        x_gradient = -(1/N) * np.sum(X**3 * (y - y_current))
        s_gradient = -(1/N) * np.sum(X**2 * (y - y_current))
        m_gradient = -(1/N) * np.sum(X * (y - y_current))
        b_gradient = -(1/N) * np.sum(y - y_current)

        x_current = x_current - (learning_rate * x_gradient)
        s_current = s_current - (learning_rate * s_gradient)
        m_current = m_current - (learning_rate * m_gradient)
        b_current = b_current - (learning_rate * b_gradient)
    
    return x_current, s_current, m_current, b_current, cost

# 파라미터, 오차율
x3, x2, x1, x0, cost = linear_regression(X, Y)

print('x3:', x3, 'x2:', x2, 'x1:', x1, 'x0:', x0, 'cost:', cost)


# ----- 그래프 생성 및 출력 -----
x_line = np.linspace(0, 3, 100)
y_line = x3 * x_line**3 + x2 * x_line**2 + x1 * x_line + x0

figure = plt.figure()
axes = figure.add_subplot(111)

# data set 그래프 생성
axes.scatter(xSet, ySet, s = 5)

# 계산된 3차 함수 그래프 생성
plt.plot(x_line, y_line, color='red')

plt.xlabel('x')
plt.ylabel('y')
plt.show()