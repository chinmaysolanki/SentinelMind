import json
from reddit_scraper import RedditScraper
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """
    Example usage of the RedditScraper class
    """
    # Create scraper instance
    scraper = RedditScraper()
    
    # Get recent posts (default limit is 50)
    logger.info("Fetching recent posts...")
    posts = scraper.get_recent_posts()
    
    # Print summary
    print(f"\nFetched {len(posts)} posts from Reddit")
    print("=" * 50)
    
    # Count posts by subreddit
    subreddit_counts = {}
    for post in posts:
        subreddit = post["subreddit"]
        subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
    
    print("\nPosts by subreddit:")
    for subreddit, count in subreddit_counts.items():
        print(f"- r/{subreddit}: {count}")
    
    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reddit_posts_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(posts)} posts to {filename}")
    
    # Print a few example posts
    print("\nExample posts:")
    for i, post in enumerate(posts[:3], 1):
        print(f"\nPost {i}:")
        print(f"Title: {post['title']}")
        print(f"Subreddit: r/{post['subreddit']}")
        print(f"Author: {post['author']}")
        print(f"Date: {post['date']}")
        print(f"Score: {post['score']}")
        print(f"Comments: {post['num_comments']}")
        print("-" * 50)

if __name__ == "__main__":
    main() 
 