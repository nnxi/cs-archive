import gymnasium as gym
import numpy as np
import tensorflow as tf
from keras.layers import Dense, Input
from keras.models import Model

class EvaluationAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.actor = self.build_actor()
        
        # 저장된 가중치 파일 로드
        self.actor.load_weights("./pendulum_actor.weights.h5")
        print("학습된 모델 가중치를 성공적으로 불러왔습니다.")

    def build_actor(self):
        state_input = Input(shape=(self.state_size,))
        h1 = Dense(128, activation='relu', kernel_initializer='he_uniform')(state_input)
        h2 = Dense(128, activation='relu', kernel_initializer='he_uniform')(h1)
        
        mu = Dense(self.action_size, activation='tanh', kernel_initializer='he_uniform')(h2)
        mu = mu * 2.0
        
        sigma = Dense(self.action_size, activation='softplus', kernel_initializer='he_uniform')(h2)
        sigma = sigma + 1e-5
        
        return Model(inputs=state_input, outputs=[mu, sigma])

    def get_action_determinstic(self, state):
        # 테스트 단계에서는 탐험(sigma)을 배제하고 학습된 최적의 평균(mu) 값만 사용
        mu, _ = self.actor(state)
        action = mu.numpy()[0]
        return action

if __name__ == "__main__":
    # 화면 렌더링 모드를 'human'으로 설정하여 그래픽 창 활성화
    env = gym.make('Pendulum-v1', render_mode='human')
    
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.shape[0]

    agent = EvaluationAgent(state_size, action_size)
    
    # 5번의 에피소드 동안 구동 화면 테스트
    for test_episode in range(5):
        state, info = env.reset()
        state = np.reshape(state, [1, state_size])
        done = False
        score = 0
        
        while not done:
            # 결정론적(Deterministic) 최적 액션 선택
            action = agent.get_action_determinstic(state)

            print(f"Current Torque: {action[0]:.5f}")
            
            next_state, reward, terminated, truncated, info = env.step(action)
            state = np.reshape(next_state, [1, state_size])
            
            done = terminated or truncated
            score += reward
            
        print(f"[Test] Episode: {test_episode + 1} | Score: {score:.2f}")
        
    env.close()