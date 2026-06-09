import sys
import gymnasium as gym
import pylab
import numpy as np
import tensorflow as tf
from keras.layers import Dense, Input
from keras.models import Model
from keras.optimizers import Adam

EPISODES = 1000


class A2CAgent:
    def __init__(self, state_size, action_size):
        self.render = False

        self.state_size = state_size
        self.action_size = action_size
        self.value_size = 1

        # 하이퍼파라미터
        self.discount_factor = 0.99
        self.actor_lr = 0.0001
        self.critic_lr = 0.001

        # 정책신경망과 가치신경망 생성
        self.actor = self.build_actor()
        self.critic = self.build_critic()

        self.actor_optimizer = Adam(learning_rate=self.actor_lr)
        self.critic_optimizer = Adam(learning_rate=self.critic_lr)

        # On-policy 배치 학습을 위한 메모리 버퍼
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
        self.dones = []

    # actor: 연속적 행동을 위한 mu와 sigma 출력 구조 유지
    def build_actor(self):
        state_input = Input(shape=(self.state_size,))
        h1 = Dense(64, activation='relu', kernel_initializer='he_uniform')(state_input)
        h2 = Dense(64, activation='relu', kernel_initializer='he_uniform')(h1)

        mu = Dense(self.action_size, activation='tanh', kernel_initializer='he_uniform')(h2)
        mu = mu * 2.0

        sigma = Dense(self.action_size, activation='softplus', kernel_initializer='he_uniform')(h2)
        sigma = sigma + 1e-5

        actor = Model(inputs=state_input, outputs=[mu, sigma])
        actor.summary()
        return actor

    # critic: 상태 가치 V(s) 예측망 구조 유지
    def build_critic(self):
        state_input = Input(shape=(self.state_size,))
        h1 = Dense(64, activation='relu', kernel_initializer='he_uniform')(state_input)
        h2 = Dense(64, activation='relu', kernel_initializer='he_uniform')(h1)
        value = Dense(self.value_size, activation='linear', kernel_initializer='he_uniform')(h2)

        critic = Model(inputs=state_input, outputs=value)
        critic.summary()
        return critic

    # 정규분포 기반 액션 샘플링 및 클리핑
    def get_action(self, state):
        mu, sigma = self.actor(state)
        mu = mu.numpy()[0][0]
        sigma = sigma.numpy()[0][0]

        action = np.random.normal(mu, sigma, 1)
        action = np.clip(action, -2.0, 2.0)
        return action

    # 스텝별 데이터를 임시 저장하는 함수
    def store_transition(self, state, action, reward, next_state, done):
        self.states.append(state[0])
        self.actions.append(action)
        self.rewards.append([reward])
        self.next_states.append(next_state[0])
        self.dones.append([float(done)])

    # @tf.function 데코레이터로 C++ 내부 정적 연산 그래프로 JIT 컴파일 가속화
    @tf.function
    def train_batch(self, states, actions, targets, advantages):
        # 1. Actor 업데이트 연산
        with tf.GradientTape() as tape:
            mu, sigma = self.actor(states)
            variance = tf.square(sigma)

            # 가우시안 로그 확률 밀도 함수 계산
            log_prob = -0.5 * tf.math.log(2 * np.pi * variance) - tf.square(actions - mu) / (2 * variance)
            log_prob = tf.reduce_sum(log_prob, axis=-1)

            entropy = 0.5 * tf.math.log(2 * np.pi * np.e * variance)
            entropy = tf.reduce_sum(entropy, axis=-1)

            actor_loss = -tf.reduce_mean(log_prob * advantages + 0.01 * entropy)

        actor_grads = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor_optimizer.apply_gradients(zip(actor_grads, self.actor.trainable_variables))

        # 2. Critic 업데이트 연산
        with tf.GradientTape() as tape:
            value_pred = self.critic(states)
            critic_loss = tf.reduce_mean(tf.square(targets - value_pred))

        critic_grads = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic_optimizer.apply_gradients(zip(critic_grads, self.critic.trainable_variables))

    # 에피소드 종료 후 수집한 200스텝의 데이터를 한 번에 일괄 학습
    def train_model(self):
        states = tf.convert_to_tensor(np.array(self.states), dtype=tf.float32)
        actions = tf.convert_to_tensor(np.array(self.actions), dtype=tf.float32)
        rewards = tf.convert_to_tensor(np.array(self.rewards), dtype=tf.float32)
        next_states = tf.convert_to_tensor(np.array(self.next_states), dtype=tf.float32)
        dones = tf.convert_to_tensor(np.array(self.dones), dtype=tf.float32)

        # 배치 전체에 대한 예측 가치 추출
        values = self.critic(states)
        next_values = self.critic(next_states)

        # 일괄 TD Target 및 Advantage 계산
        targets = rewards + self.discount_factor * next_values * (1.0 - dones)
        advantages = targets - values

        # 컴파일된 가속 함수 호출
        self.train_batch(states, actions, targets, advantages)

        # 다음 에피소드를 위해 메모리 버퍼 클리어
        self.states, self.actions, self.rewards, self.next_states, self.dones = [], [], [], [], []


if __name__ == "__main__":
    env = gym.make('Pendulum-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.shape[0]

    agent = A2CAgent(state_size, action_size)
    scores, episodes = [], []

    for e in range(EPISODES):
        done = False
        score = 0

        state, info = env.reset()
        state = np.reshape(state, [1, state_size])

        while not done:
            action = agent.get_action(state)

            next_state, reward, terminated, truncated, info = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])

            done = terminated or truncated
            scaled_reward = reward / 10.0

            # 실시간 업데이트 대신 메모리 버퍼에 데이터 누적
            agent.store_transition(state, action, scaled_reward, next_state, done)

            score += reward
            state = next_state

        # 에피소드가 완전히 완료(200스텝 도달)된 후 배치 단위 고속 업데이트 수행
        agent.train_model()

        # 출력 및 시각화용 로그 기록
        scores.append(score)
        episodes.append(e)

        # 10 에피소드마다 터미널에 중간 진척도 모니터링 출력
        if (e + 1) % 10 == 0:
            pylab.plot(episodes, scores, 'b')
            pylab.savefig("./pendulum_a2c.png")
            print(f"episode: {e + 1:4d} | score: {score:.2f}")