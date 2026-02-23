import pandas as pd
import os

# Well-known and trusted benign URLs to add to the dataset
TRUSTED_BENIGN_URLS = [
    # Search Engines
    "https://google.com", "https://www.google.com", "https://google.co.in",
    "https://bing.com", "https://www.bing.com",
    "https://yahoo.com", "https://www.yahoo.com",
    "https://duckduckgo.com",
    "https://baidu.com",

    # Social Media
    "https://facebook.com", "https://www.facebook.com",
    "https://instagram.com", "https://www.instagram.com",
    "https://twitter.com", "https://www.twitter.com",
    "https://linkedin.com", "https://www.linkedin.com",
    "https://reddit.com", "https://www.reddit.com",
    "https://tiktok.com", "https://www.tiktok.com",
    "https://snapchat.com", "https://www.snapchat.com",
    "https://pinterest.com", "https://www.pinterest.com",
    "https://tumblr.com",

    # Video / Entertainment
    "https://youtube.com", "https://www.youtube.com",
    "https://netflix.com", "https://www.netflix.com",
    "https://twitch.tv", "https://www.twitch.tv",
    "https://vimeo.com",
    "https://dailymotion.com",
    "https://spotify.com", "https://www.spotify.com",

    # E-commerce
    "https://amazon.com", "https://www.amazon.com",
    "https://amazon.in", "https://www.amazon.in",
    "https://ebay.com", "https://www.ebay.com",
    "https://flipkart.com", "https://www.flipkart.com",
    "https://walmart.com", "https://www.walmart.com",
    "https://etsy.com", "https://www.etsy.com",
    "https://shopify.com",
    "https://aliexpress.com",

    # Tech / Developer
    "https://github.com", "https://www.github.com",
    "https://stackoverflow.com", "https://www.stackoverflow.com",
    "https://microsoft.com", "https://www.microsoft.com",
    "https://apple.com", "https://www.apple.com",
    "https://developer.apple.com",
    "https://docs.microsoft.com",
    "https://azure.microsoft.com",
    "https://cloud.google.com",
    "https://aws.amazon.com",
    "https://medium.com", "https://www.medium.com",
    "https://dev.to",
    "https://gitlab.com",
    "https://bitbucket.org",
    "https://npmjs.com",
    "https://pypi.org",
    "https://hub.docker.com",
    "https://kaggle.com",
    "https://colab.research.google.com",
    "https://jupyter.org",

    # News
    "https://cnn.com", "https://www.cnn.com",
    "https://bbc.com", "https://www.bbc.com",
    "https://nytimes.com", "https://www.nytimes.com",
    "https://theguardian.com",
    "https://reuters.com",
    "https://bloomberg.com",
    "https://ndtv.com", "https://www.ndtv.com",
    "https://thehindu.com",
    "https://timesofindia.indiatimes.com",

    # Education
    "https://wikipedia.org", "https://en.wikipedia.org",
    "https://coursera.org",
    "https://udemy.com",
    "https://edx.org",
    "https://khanacademy.org",
    "https://w3schools.com",
    "https://geeksforgeeks.org",

    # Finance / Banks
    "https://paypal.com", "https://www.paypal.com",
    "https://stripe.com",
    "https://visa.com",
    "https://mastercard.com",

    # Government / Trusted
    "https://gov.in",
    "https://nasa.gov",
    "https://who.int",
    "https://un.org",

    # Cloud / SaaS
    "https://zoom.us",
    "https://slack.com",
    "https://notion.so",
    "https://drive.google.com",
    "https://docs.google.com",
    "https://mail.google.com",
    "https://outlook.com", "https://www.outlook.com",
    "https://dropbox.com",
    "https://box.com",
]

# Load existing dataset
print("📂 Loading existing dataset...")
df = pd.read_csv("benign_vs_defacement_urls.csv", encoding='latin1', on_bad_lines='skip')
print(f"   Original rows: {len(df)}")

# Create new benign rows
new_rows = pd.DataFrame({
    'url': TRUSTED_BENIGN_URLS,
    'type': 'benign'
})

# Add any missing columns with empty defaults
for col in df.columns:
    if col not in new_rows.columns:
        new_rows[col] = ''

# Reorder to match original column order
new_rows = new_rows[df.columns]

# Append to original data
df_updated = pd.concat([df, new_rows], ignore_index=True)
print(f"   Rows after adding benign URLs: {len(df_updated)}")

# Save as new CSV (keep original as backup)
df_updated.to_csv("benign_vs_defacement_urls.csv", index=False, encoding='latin1')
print("✅ Dataset updated and saved!")
print(f"   Added {len(TRUSTED_BENIGN_URLS)} trusted benign URLs.")
