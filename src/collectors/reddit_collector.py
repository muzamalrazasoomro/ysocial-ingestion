import argparse, os, hashlib, json
from datetime import datetime, timezone
from typing import Dict
from dotenv import load_dotenv
import praw
from tqdm import tqdm

from src.processors.clean_text import clean
from src.processors.sentiment import score as sentiment_score

def hash_id(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]

def to_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

def make_post(record: Dict, platform='reddit', source='reddit_collector/0.1') -> Dict:
    text = clean(record.get('text') or '')
    sent = sentiment_score(text)
    base_id = record.get('external_id') or text
    return {
        'post_id': hash_id(f"{platform}:{base_id}"),
        'external_id': record.get('external_id'),
        'author_id': hash_id(record.get('author_id','anon')) if record.get('author_id') else None,
        'created_at': record.get('created_at'),
        'text': text,
        'platform': platform,
        'ingestion_source': source,
        'lang': record.get('lang','en'),
        'engagement': {
            'likes': record.get('score', 0),
            'replies': record.get('num_comments', 0),
            'reposts': 0,
            'quotes': 0
        },
        'topic': record.get('topic'),
        'topic_keywords': record.get('topic_keywords', []),
        'sentiment': sent,
        'toxicity': None,
        'raw': {
            'subreddit': record.get('subreddit'),
            'permalink': record.get('permalink')
        }
    }

def main():
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument('--query', required=True, help='search query text')
    ap.add_argument('--limit', type=int, default=50)
    ap.add_argument('--out', required=True, help='output JSONL path')
    args = ap.parse_args()

    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME') or None,
        password=os.getenv('REDDIT_PASSWORD') or None,
    )

    outdir = os.path.dirname(args.out)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    n = 0
    with open(args.out, 'w', encoding='utf-8') as f:
        for submission in tqdm(reddit.subreddit('all').search(args.query, limit=args.limit, sort='new')):
            rec = {
                'external_id': submission.id,
                'author_id': str(submission.author) if submission.author else 'deleted',
                'created_at': to_iso(getattr(submission, 'created_utc', 0.0)),
                'text': f"{submission.title or ''} {submission.selftext or ''}".strip(),
                'score': int(submission.score or 0),
                'num_comments': int(submission.num_comments or 0),
                'subreddit': str(submission.subreddit),
                'permalink': 'https://reddit.com' + submission.permalink,
                'topic': None,
                'topic_keywords': [],
                'lang': 'en'
            }
            obj = make_post(rec)
            f.write(json.dumps(obj, ensure_ascii=False) + '\\n')
            n += 1

    print(f'Wrote {n} items to {args.out}')

if __name__ == '__main__':
    main()
