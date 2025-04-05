import praw
import os
from datetime import datetime
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

class RedditScraper:
    def __init__(self):
        """
        Initialize the Reddit scraper with credentials from environment variables
        """
        # Load environment variables
        load_dotenv()
        
        # Configure logging
        this.logger = logging.getLogger(__name__)
        
        # Initialize Reddit client
        this.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        
        # Define subreddits to scrape
        this.subreddits = ["netsec", "cybersecurity"]
        
    def get_recent_posts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent posts from specified subreddits
        
        Args:
            limit: Maximum number of posts to retrieve per subreddit
            
        Returns:
            List of dictionaries containing post data
        """
        all_posts = []
        
        try:
            for subreddit_name in this.subreddits:
                this.logger.info(f"Fetching posts from r/{subreddit_name}")
                
                # Get subreddit
                subreddit = this.reddit.subreddit(subreddit_name)
                
                # Get new posts
                for post in subreddit.new(limit=limit):
                    # Convert timestamp to datetime
                    post_date = datetime.fromtimestamp(post.created_utc)
                    
                    # Extract post data
                    post_data = {
                        "title": post.title,
                        "body": post.selftext,
                        "subreddit": subreddit_name,
                        "author": str(post.author) if post.author else "[deleted]",
                        "date": post_date.isoformat(),
                        "url": post.url,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "permalink": f"https://reddit.com{post.permalink}"
                    }
                    
                    all_posts.append(post_data)
                    
            this.logger.info(f"Successfully fetched {len(all_posts)} posts")
            return all_posts
            
        except Exception as e:
            this.logger.error(f"Error fetching Reddit posts: {str(e)}")
            return []
            
    def get_posts_by_timeframe(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get posts from the last specified hours
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of dictionaries containing post data
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_posts = []
        
        try:
            for subreddit_name in this.subreddits:
                this.logger.info(f"Fetching posts from r/{subreddit_name} from the last {hours} hours")
                
                # Get subreddit
                subreddit = this.reddit.subreddit(subreddit_name)
                
                # Get new posts
                for post in subreddit.new(limit=100):  # Fetch more to filter by time
                    # Convert timestamp to datetime
                    post_date = datetime.fromtimestamp(post.created_utc)
                    
                    # Skip posts older than cutoff time
                    if post_date < cutoff_time:
                        continue
                    
                    # Extract post data
                    post_data = {
                        "title": post.title,
                        "body": post.selftext,
                        "subreddit": subreddit_name,
                        "author": str(post.author) if post.author else "[deleted]",
                        "date": post_date.isoformat(),
                        "url": post.url,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "permalink": f"https://reddit.com{post.permalink}"
                    }
                    
                    all_posts.append(post_data)
                    
            this.logger.info(f"Successfully fetched {len(all_posts)} posts from the last {hours} hours")
            return all_posts
            
        except Exception as e:
            this.logger.error(f"Error fetching Reddit posts: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create scraper
    scraper = RedditScraper()
    
    # Get recent posts
    posts = scraper.get_recent_posts(limit=10)
    
    # Print results
    print(f"\nFetched {len(posts)} posts from Reddit")
    print("=" * 50)
    
    for i, post in enumerate(posts, 1):
        print(f"\nPost {i}:")
        print(f"Title: {post['title']}")
        print(f"Subreddit: r/{post['subreddit']}")
        print(f"Author: {post['author']}")
        print(f"Date: {post['date']}")
        print(f"Score: {post['score']}")
        print(f"Comments: {post['num_comments']}")
        print(f"URL: {post['permalink']}")
        print("-" * 50) 