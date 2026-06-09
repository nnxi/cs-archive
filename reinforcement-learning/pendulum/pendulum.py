import sys
import gymnasium as gym
import pylab
import numpy as np
import tensorflow as tf
from keras.layers import Dense, Input
from keras.models import Model
from keras.optimizers import Adam

EPISODES = 5000

class A2CAgent:
    def __init__(self, state_size, action_size):
        self.render = False

        self.state_size = state_size
        self.action_size = action_size
        self.value_size = 1

        self.discount_factor = 0.99
        self.actor_lr = 0.0001
        self.critic_lr = 0.0002

        self.actor = self.build_actor()
        self.critic = self.build_critic()

        self.actor_optimizer = Adam(learning_rate=self.actor_lr)
        self.critic_optimizer = Adam(learning_rate=self.critic_lr)

        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
        self.dones = []

    def build_actor(self):
        state_input = Input(shape=(self.state_size,))
        h1 = Dense(128, activation='relu')(state_input)
        h2 = Dense(128, activation='relu')(h1)

        mu = Dense(self.action_size, activation='tanh')(h2)
        mu = mu * 2.0

        sigma = Dense(self.action_size, activation='softplus')(h2)

        actor = Model(inputs=state_input, outputs=[mu, sigma])
        actor.summary()
        return actor

    def build_critic(self):
        state_input = Input(shape=(self.state_size,))
        h1 = Dense(128, activation='relu')(state_input)
        h2 = Dense(128, activation='relu')(h1)
        value = Dense(self.value_size, activation='linear')(h2)

        critic = Model(inputs=state_input, outputs=value)
        critic.summary()
        return critic

    def get_action(self, state):
        mu, sigma = self.actor(state)

        mu = mu.numpy()[0][0]
        sigma = sigma.numpy()[0][0]

        # 탐험 변동성 제어를 위한 시그마 클리핑
        sigma = np.clip(sigma, 0.1, 1.0)

        action = np.random.normal(mu, sigma, 1)
        action = np.clip(action, -2.0, 2.0)

        return action.astype(np.float32)

    def store_transition(self, state, action, reward, next_state, done):
        self.states.append(state[0])
        self.actions.append(action)
        self.rewards.append([reward])
        self.next_states.append(next_state[0])
        self.dones.append([float(done)])

    @tf.function
    def train_batch(self, states, actions, targets, advantages):
        # 1. Actor 업데이트
        with tf.GradientTape() as tape:
            mu, sigma = self.actor(states)
            sigma = tf.clip_by_value(sigma, 0.1, 1.0)
            variance = tf.square(sigma)

            log_prob = -0.5 * tf.math.log(2 * np.pi * variance) - tf.square(actions - mu) / (2 * variance)
            log_prob = tf.reduce_sum(log_prob, axis=1)

            entropy = 0.5 * tf.math.log(2 * np.pi * np.e * variance)
            entropy = tf.reduce_sum(entropy, axis=1)

            # Critic 그라디언트 유입 차단 및 엔트로피 계수 설정
            actor_loss = -tf.reduce_mean(log_prob * tf.stop_gradient(advantages) + 0.001 * entropy)

        actor_grads = tape.gradient(actor_loss, self.actor.trainable_variables)
        
        # Actor 그라디언트 폭발 방지 클리핑
        actor_grads, _ = tf.clip_by_global_norm(actor_grads, 0.5)
        self.actor_optimizer.apply_gradients(zip(actor_grads, self.actor.trainable_variables))

        # 2. Critic 업데이트
        with tf.GradientTape() as tape:
            value_pred = self.critic(states)
            # 이상치에 덜 민감한 Huber Loss 적용
            critic_loss = tf.reduce_mean(tf.keras.losses.Huber()(targets, value_pred))

        critic_grads = tape.gradient(critic_loss, self.critic.trainable_variables)
        
        # Critic 그라디언트 폭발 방지 클리핑
        critic_grads, _ = tf.clip_by_global_norm(critic_grads, 0.5)
        self.critic_optimizer.apply_gradients(zip(critic_grads, self.critic.trainable_variables))

    def train_model(self):
        states = np.array(self.states, dtype=np.float32)
        actions = np.array(self.actions, dtype=np.float32)
        rewards = np.array(self.rewards, dtype=np.float32).flatten()
        dones = np.array(self.dones, dtype=np.float32).flatten()

        values = self.critic(states).numpy().flatten()
        next_value = 0.0

        # 에피소드가 끝나지 않고 20스텝이 찬 경우, 마지막 상태의 가치를 부트스트랩
        if dones[-1] == 0:
            next_state = np.array([self.next_states[-1]], dtype=np.float32)
            next_value = self.critic(next_state).numpy()[0, 0]

        targets = np.zeros_like(rewards)
        running_target = next_value

        # 역순으로 n-step Return 계산 (핵심 로직)
        for t in reversed(range(len(rewards))):
            running_target = rewards[t] + self.discount_factor * running_target * (1 - dones[t])
            targets[t] = running_target

        # Advantage 계산 및 정규화
        advantages = targets - values
        advantages = (advantages - np.mean(advantages)) / (np.std(advantages) + 1e-8)

        self.train_batch(
            tf.convert_to_tensor(states),
            tf.convert_to_tensor(actions),
            tf.convert_to_tensor(targets.reshape(-1, 1), dtype=tf.float32),
            tf.convert_to_tensor(advantages, dtype=tf.float32)
        )

        self.states.clear()
        self.actions.clear()
        self.rewards.clear()
        self.next_states.clear()
        self.dones.clear()


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

            # 순정 보상 스케일링 유지
            scaled_reward = reward / 10.0

            agent.store_transition(state, action, scaled_reward, next_state, done)

            score += reward
            state = next_state

            # 20스텝 도달 또는 에피소드 종료 시 학습
            if len(agent.states) >= 20 or done:
                agent.train_model()

        scores.append(score)
        episodes.append(e)

        if (e + 1) % 10 == 0:
            pylab.plot(episodes, scores, 'b')
            pylab.savefig("./pendulum_a2c.png")
            print(f"episode: {e + 1:4d} | score: {score:.2f}")

    agent.actor.save_weights("./pendulum_actor.weights.h5")
    print("모델 가중치 저장 완료: ./pendulum_actor.weights.h5")

    env.close()