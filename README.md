# ysocial-ingestion

Unified ingestion pipeline for Y-Social. Starts with **Reddit**, then generalizes to **Bluesky**, **Mastodon**, and **X**.
Outputs a consistent JSONL schema validated against `src/schema/unified_post_schema.json`.

## Quick start (Reddit)

1. Create a Reddit app (script) to get `client_id`, `client_secret`, and a throwaway `username`/`password` (or use OAuth installed app).  
2. Copy `.env.example` to `.env` and fill in values.
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   python -m nltk.downloader vader_lexicon
   ```
4. Run a test search on a topic:
   ```bash
   python src/collectors/reddit_collector.py --query "ai safety" --limit 50 --out data/reddit/ai_safety.jsonl
   ```
5. Validate:
   ```bash
   python src/schema/validate.py --file data/reddit/ai_safety.jsonl
   ```
