import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.utils import set_random_seed
from multi_agent_cyber_env import MultiAgentCyberEnv
import json
from datetime import datetime

def make_env(env_id: str, rank: int, seed: int = 0):
    """
    Utility function for multiprocessed env.
    
    Args:
        env_id: Environment ID
        rank: Index of the subprocess
        seed: Random seed
    """
    def _init():
        env = MultiAgentCyberEnv(max_steps=1000, threat_probability=0.2)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

def train_agents(
    total_timesteps: int = 100_000,
    learning_rate: float = 0.0003,
    save_path: str = "models/multi_agent"
):
    """
    Train both blocker and analyzer agents.
    
    Args:
        total_timesteps: Total number of timesteps to train for
        learning_rate: Learning rate for the PPO algorithm
        save_path: Path to save the trained models
    """
    # Create output directory
    os.makedirs(save_path, exist_ok=True)
    
    # Create and wrap the environment
    env = DummyVecEnv([make_env("MultiAgentCyberEnv-v0", i) for i in range(1)])
    env = VecMonitor(env, filename=os.path.join(save_path, "monitor.csv"))
    
    # Create evaluation environment
    eval_env = DummyVecEnv([make_env("MultiAgentCyberEnv-v0", 0)])
    eval_env = VecMonitor(eval_env, filename=os.path.join(save_path, "eval_monitor.csv"))
    
    # Create the agents
    blocker = PPO(
        "MlpPolicy",
        env,
        learning_rate=learning_rate,
        verbose=1,
        tensorboard_log=os.path.join(save_path, "blocker_tensorboard")
    )
    
    analyzer = PPO(
        "MlpPolicy",
        env,
        learning_rate=learning_rate,
        verbose=1,
        tensorboard_log=os.path.join(save_path, "analyzer_tensorboard")
    )
    
    # Create evaluation callbacks
    blocker_callback = EvalCallback(
        eval_env,
        best_model_save_path=os.path.join(save_path, "best_blocker"),
        log_path=os.path.join(save_path, "blocker_logs"),
        eval_freq=10000,
        deterministic=True,
        render=False
    )
    
    analyzer_callback = EvalCallback(
        eval_env,
        best_model_save_path=os.path.join(save_path, "best_analyzer"),
        log_path=os.path.join(save_path, "analyzer_logs"),
        eval_freq=10000,
        deterministic=True,
        render=False
    )
    
    # Training loop
    print("Starting training...")
    for i in range(total_timesteps // 1000):  # Train in episodes of 1000 steps
        # Train blocker
        blocker.learn(
            total_timesteps=1000,
            callback=blocker_callback,
            reset_num_timesteps=False
        )
        
        # Train analyzer
        analyzer.learn(
            total_timesteps=1000,
            callback=analyzer_callback,
            reset_num_timesteps=False
        )
        
        # Save models periodically
        if (i + 1) % 10 == 0:
            blocker.save(os.path.join(save_path, f"blocker_{i+1}k"))
            analyzer.save(os.path.join(save_path, f"analyzer_{i+1}k"))
            
            # Save training metrics
            metrics = {
                "blocker": {
                    "mean_reward": np.mean(env.get_attr("stats")[0]["blocker_rewards"]),
                    "correct_blocks": env.get_attr("stats")[0]["correct_blocks"],
                    "false_positives": env.get_attr("stats")[0]["false_positives"],
                    "missed_threats": env.get_attr("stats")[0]["missed_threats"]
                },
                "analyzer": {
                    "mean_reward": np.mean(env.get_attr("stats")[0]["analyzer_rewards"]),
                    "correct_logs": env.get_attr("stats")[0]["correct_logs"]
                }
            }
            
            with open(os.path.join(save_path, f"metrics_{i+1}k.json"), "w") as f:
                json.dump(metrics, f, indent=2)
    
    # Save final models
    blocker.save(os.path.join(save_path, "final_blocker"))
    analyzer.save(os.path.join(save_path, "final_analyzer"))
    
    # Close environments
    env.close()
    eval_env.close()
    
    return blocker, analyzer

def evaluate_agents(
    blocker_path: str,
    analyzer_path: str,
    n_eval_episodes: int = 10
):
    """
    Evaluate trained agents.
    
    Args:
        blocker_path: Path to the trained blocker model
        analyzer_path: Path to the trained analyzer model
        n_eval_episodes: Number of episodes to evaluate
    """
    # Create environment
    env = MultiAgentCyberEnv(max_steps=1000, threat_probability=0.2)
    
    # Load models
    blocker = PPO.load(blocker_path)
    analyzer = PPO.load(analyzer_path)
    
    # Initialize metrics
    metrics = {
        "blocker": {
            "rewards": [],
            "correct_blocks": [],
            "false_positives": [],
            "missed_threats": []
        },
        "analyzer": {
            "rewards": [],
            "correct_logs": []
        }
    }
    
    # Run evaluation episodes
    for episode in range(n_eval_episodes):
        obs = env.reset()
        done = False
        episode_rewards = {"blocker": 0, "analyzer": 0}
        
        while not done:
            # Get actions from both agents
            blocker_action, _ = blocker.predict(obs["blocker"], deterministic=True)
            analyzer_action, _ = analyzer.predict(obs["analyzer"], deterministic=True)
            
            # Step environment
            next_obs, rewards, done, info = env.step({
                "blocker": blocker_action,
                "analyzer": analyzer_action
            })
            
            # Update episode rewards
            episode_rewards["blocker"] += rewards["blocker"]
            episode_rewards["analyzer"] += rewards["analyzer"]
            
            obs = next_obs
        
        # Record metrics
        metrics["blocker"]["rewards"].append(episode_rewards["blocker"])
        metrics["blocker"]["correct_blocks"].append(info["correct_blocks"])
        metrics["blocker"]["false_positives"].append(info["false_positives"])
        metrics["blocker"]["missed_threats"].append(info["missed_threats"])
        
        metrics["analyzer"]["rewards"].append(episode_rewards["analyzer"])
        metrics["analyzer"]["correct_logs"].append(info["correct_logs"])
        
        print(f"\nEpisode {episode + 1}:")
        print(f"Blocker Reward: {episode_rewards['blocker']:.2f}")
        print(f"Analyzer Reward: {episode_rewards['analyzer']:.2f}")
        print(f"Correct Blocks: {info['correct_blocks']}")
        print(f"False Positives: {info['false_positives']}")
        print(f"Missed Threats: {info['missed_threats']}")
        print(f"Correct Logs: {info['correct_logs']}")
    
    # Calculate mean metrics
    mean_metrics = {
        "blocker": {
            "mean_reward": np.mean(metrics["blocker"]["rewards"]),
            "mean_correct_blocks": np.mean(metrics["blocker"]["correct_blocks"]),
            "mean_false_positives": np.mean(metrics["blocker"]["false_positives"]),
            "mean_missed_threats": np.mean(metrics["blocker"]["missed_threats"])
        },
        "analyzer": {
            "mean_reward": np.mean(metrics["analyzer"]["rewards"]),
            "mean_correct_logs": np.mean(metrics["analyzer"]["correct_logs"])
        }
    }
    
    print("\nEvaluation Results:")
    print("-" * 50)
    for agent, agent_metrics in mean_metrics.items():
        print(f"\n{agent.capitalize()} Metrics:")
        for metric, value in agent_metrics.items():
            print(f"{metric}: {value:.2f}")
    
    return metrics, mean_metrics

if __name__ == "__main__":
    # Train agents
    blocker, analyzer = train_agents(
        total_timesteps=100_000,
        learning_rate=0.0003,
        save_path="models/multi_agent"
    )
    
    # Evaluate agents
    metrics, mean_metrics = evaluate_agents(
        blocker_path="models/multi_agent/final_blocker.zip",
        analyzer_path="models/multi_agent/final_analyzer.zip",
        n_eval_episodes=10
    )
    
    # Save evaluation results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"evaluation_results_{timestamp}.json", "w") as f:
        json.dump({
            "metrics": metrics,
            "mean_metrics": mean_metrics
        }, f, indent=2) 