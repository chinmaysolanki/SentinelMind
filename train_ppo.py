import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.utils import set_random_seed
from cyber_env import CyberEnv
import numpy as np

def make_env(env_id: str, rank: int, seed: int = 0):
    """
    Utility function for multiprocessed env.
    
    Args:
        env_id: Environment ID
        rank: Index of the subprocess
        seed: Random seed
    """
    def _init():
        env = CyberEnv(max_steps=1000, threat_probability=0.2)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

def evaluate_policy(model, env, n_eval_episodes=10):
    """
    Evaluate the policy for n_eval_episodes and return mean reward.
    
    Args:
        model: The trained model
        env: The environment
        n_eval_episodes: Number of episodes to evaluate
    """
    episode_rewards = []
    episode_lengths = []
    correct_blocks = []
    false_positives = []
    missed_threats = []
    correct_logs = []
    
    for _ in range(n_eval_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0
        episode_length = 0
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            episode_length += 1
        
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        correct_blocks.append(info["correct_blocks"])
        false_positives.append(info["false_positives"])
        missed_threats.append(info["missed_threats"])
        correct_logs.append(info["correct_logs"])
    
    # Calculate mean metrics
    mean_reward = np.mean(episode_rewards)
    mean_length = np.mean(episode_lengths)
    mean_correct_blocks = np.mean(correct_blocks)
    mean_false_positives = np.mean(false_positives)
    mean_missed_threats = np.mean(missed_threats)
    mean_correct_logs = np.mean(correct_logs)
    
    print("\nEvaluation Results:")
    print(f"Mean Reward: {mean_reward:.2f}")
    print(f"Mean Episode Length: {mean_length:.2f}")
    print(f"Mean Correct Blocks: {mean_correct_blocks:.2f}")
    print(f"Mean False Positives: {mean_false_positives:.2f}")
    print(f"Mean Missed Threats: {mean_missed_threats:.2f}")
    print(f"Mean Correct Logs: {mean_correct_logs:.2f}")
    
    return mean_reward

def main():
    # Create output directory
    os.makedirs("models", exist_ok=True)
    
    # Create and wrap the environment
    env = DummyVecEnv([make_env("CyberEnv-v0", i) for i in range(1)])
    env = VecMonitor(env, filename="models/monitor.csv")
    
    # Create evaluation environment
    eval_env = DummyVecEnv([make_env("CyberEnv-v0", 0)])
    eval_env = VecMonitor(eval_env, filename="models/eval_monitor.csv")
    
    # Create the model
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=0.0003,
        verbose=1
    )
    
    # Create evaluation callback
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path="models/best_model",
        log_path="models/logs",
        eval_freq=10000,
        deterministic=True,
        render=False
    )
    
    # Train the agent
    print("Starting training...")
    model.learn(
        total_timesteps=100_000,
        callback=eval_callback
    )
    
    # Save the final model
    model.save("models/ppo_defender")
    print("\nTraining completed. Model saved as 'models/ppo_defender.zip'")
    
    # Final evaluation
    print("\nPerforming final evaluation...")
    final_reward = evaluate_policy(model, eval_env)
    print(f"\nFinal evaluation mean reward: {final_reward:.2f}")
    
    # Close environments
    env.close()
    eval_env.close()

if __name__ == "__main__":
    main() 