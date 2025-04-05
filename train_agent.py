import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.utils import set_random_seed
from cyber_env import CyberEnv
import json
from datetime import datetime
from utils.threat_to_env import convert_threat_to_env_input

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

def train_agent(
    total_timesteps: int = 100_000,
    learning_rate: float = 0.0003,
    n_steps: int = 2048,
    save_path: str = "models/cyber_agent"
):
    """
    Train a PPO agent on the CyberEnv environment.
    
    Args:
        total_timesteps: Total number of timesteps to train for
        learning_rate: Learning rate for the PPO algorithm
        n_steps: Number of steps to run for each update
        save_path: Path to save the trained model
    """
    # Create output directory
    os.makedirs(save_path, exist_ok=True)
    
    # Create and wrap the environment
    env = DummyVecEnv([make_env("CyberEnv-v0", i) for i in range(1)])
    env = VecMonitor(env, filename=os.path.join(save_path, "monitor.csv"))
    
    # Create evaluation environment
    eval_env = DummyVecEnv([make_env("CyberEnv-v0", 0)])
    eval_env = VecMonitor(eval_env, filename=os.path.join(save_path, "eval_monitor.csv"))
    
    # Create the agent
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=learning_rate,
        n_steps=n_steps,
        verbose=1,
        tensorboard_log=os.path.join(save_path, "tensorboard")
    )
    
    # Create evaluation callback
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=os.path.join(save_path, "best_model"),
        log_path=os.path.join(save_path, "logs"),
        eval_freq=10000,
        deterministic=True,
        render=False
    )
    
    # Load threat intelligence data
    try:
        with open('intel_data.json') as f:
            threats = json.load(f)
        print(f"Loaded {len(threats)} threats from intel_data.json")
    except FileNotFoundError:
        print("Warning: intel_data.json not found. Using simulated data.")
        threats = []
    
    # Training loop
    print("Starting training...")
    timesteps_so_far = 0
    
    while timesteps_so_far < total_timesteps:
        # If we have threat data, use it
        if threats:
            # Shuffle threats to avoid overfitting to a specific order
            np.random.shuffle(threats)
            
            # Process each threat
            for threat in threats:
                # Convert threat to environment state
                state = convert_threat_to_env_input(threat)
                
                # Step the environment with the converted state
                obs, reward, done, info = env.step([state])
                
                # Update timesteps
                timesteps_so_far += 1
                
                # If we've reached the total timesteps, break
                if timesteps_so_far >= total_timesteps:
                    break
                
                # If the episode is done, reset the environment
                if done:
                    env.reset()
        else:
            # If no threat data, use the default environment behavior
            model.learn(
                total_timesteps=min(1000, total_timesteps - timesteps_so_far),
                callback=eval_callback,
                reset_num_timesteps=False
            )
            timesteps_so_far += 1000
        
        # Save model periodically
        if timesteps_so_far % 10000 == 0:
            model.save(os.path.join(save_path, f"model_{timesteps_so_far}"))
            print(f"Saved model at {timesteps_so_far} timesteps")
    
    # Save final model
    model.save(os.path.join(save_path, "final_model"))
    
    # Close environments
    env.close()
    eval_env.close()
    
    return model

def evaluate_agent(
    model_path: str,
    n_eval_episodes: int = 10
):
    """
    Evaluate a trained agent.
    
    Args:
        model_path: Path to the trained model
        n_eval_episodes: Number of episodes to evaluate
    """
    # Create environment
    env = CyberEnv(max_steps=1000, threat_probability=0.2)
    
    # Load model
    model = PPO.load(model_path)
    
    # Initialize metrics
    episode_rewards = []
    episode_lengths = []
    correct_blocks = []
    false_positives = []
    missed_threats = []
    correct_logs = []
    
    # Load threat intelligence data
    try:
        with open('intel_data.json') as f:
            threats = json.load(f)
        print(f"Loaded {len(threats)} threats for evaluation")
    except FileNotFoundError:
        print("Warning: intel_data.json not found. Using simulated data.")
        threats = []
    
    # Run evaluation episodes
    for episode in range(n_eval_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0
        episode_length = 0
        
        # If we have threat data, use it
        if threats:
            # Shuffle threats to avoid overfitting to a specific order
            np.random.shuffle(threats)
            
            # Process each threat
            for threat in threats:
                # Convert threat to environment state
                state = convert_threat_to_env_input(threat)
                
                # Get action from model
                action, _ = model.predict(obs, deterministic=True)
                
                # Step environment
                obs, reward, done, info = env.step(action)
                
                # Update metrics
                episode_reward += reward
                episode_length += 1
                
                # If the episode is done, break
                if done:
                    break
        else:
            # If no threat data, use the default environment behavior
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                episode_reward += reward
                episode_length += 1
        
        # Record metrics
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        correct_blocks.append(info.get("correct_blocks", 0))
        false_positives.append(info.get("false_positives", 0))
        missed_threats.append(info.get("missed_threats", 0))
        correct_logs.append(info.get("correct_logs", 0))
        
        print(f"\nEpisode {episode + 1}:")
        print(f"Reward: {episode_reward:.2f}")
        print(f"Length: {episode_length}")
        print(f"Correct Blocks: {info.get('correct_blocks', 0)}")
        print(f"False Positives: {info.get('false_positives', 0)}")
        print(f"Missed Threats: {info.get('missed_threats', 0)}")
        print(f"Correct Logs: {info.get('correct_logs', 0)}")
    
    # Calculate mean metrics
    mean_reward = np.mean(episode_rewards)
    mean_length = np.mean(episode_lengths)
    mean_correct_blocks = np.mean(correct_blocks)
    mean_false_positives = np.mean(false_positives)
    mean_missed_threats = np.mean(missed_threats)
    mean_correct_logs = np.mean(correct_logs)
    
    print("\nEvaluation Results:")
    print("-" * 50)
    print(f"Mean Reward: {mean_reward:.2f}")
    print(f"Mean Episode Length: {mean_length:.2f}")
    print(f"Mean Correct Blocks: {mean_correct_blocks:.2f}")
    print(f"Mean False Positives: {mean_false_positives:.2f}")
    print(f"Mean Missed Threats: {mean_missed_threats:.2f}")
    print(f"Mean Correct Logs: {mean_correct_logs:.2f}")
    
    return {
        "mean_reward": mean_reward,
        "mean_length": mean_length,
        "mean_correct_blocks": mean_correct_blocks,
        "mean_false_positives": mean_false_positives,
        "mean_missed_threats": mean_missed_threats,
        "mean_correct_logs": mean_correct_logs
    }

def plot_training_results(log_path: str, save_path: str = None):
    """
    Plot training results from a log file.
    
    Args:
        log_path: Path to the log file
        save_path: Path to save the plot (if None, the plot is displayed)
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # Read log file
    log_data = pd.read_csv(log_path)
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot mean reward
    axes[0, 0].plot(log_data["r"])
    axes[0, 0].set_title("Mean Reward")
    axes[0, 0].set_xlabel("Timesteps")
    axes[0, 0].set_ylabel("Reward")
    
    # Plot mean episode length
    axes[0, 1].plot(log_data["l"])
    axes[0, 1].set_title("Mean Episode Length")
    axes[0, 1].set_xlabel("Timesteps")
    axes[0, 1].set_ylabel("Length")
    
    # Plot learning rate
    axes[1, 0].plot(log_data["lr"])
    axes[1, 0].set_title("Learning Rate")
    axes[1, 0].set_xlabel("Timesteps")
    axes[1, 0].set_ylabel("Learning Rate")
    
    # Plot value loss
    axes[1, 1].plot(log_data["v_loss"])
    axes[1, 1].set_title("Value Loss")
    axes[1, 1].set_xlabel("Timesteps")
    axes[1, 1].set_ylabel("Loss")
    
    # Adjust layout
    plt.tight_layout()
    
    # Save or display plot
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

if __name__ == "__main__":
    # Train agent
    model = train_agent(
        total_timesteps=100_000,
        learning_rate=0.0003,
        n_steps=2048,
        save_path="models/cyber_agent"
    )
    
    # Evaluate agent
    metrics = evaluate_agent(
        model_path="models/cyber_agent/final_model.zip",
        n_eval_episodes=10
    )
    
    # Plot training results
    plot_training_results(
        log_path="models/cyber_agent/monitor.csv",
        save_path="models/cyber_agent/training_curves.png"
    ) 