import pandas as pd
import pycountry
from pathlib import Path

# Data cleaning

raw_path = Path(r"D:\MY\2025-26-1\GISDATA\GE5230-2510\Spotify-Global-Streaming-Data-2024\Spotify_2024_Global_Streaming_Data.csv")
clean_path = raw_path.with_name("Cleaned_Spotify_2024_Global_Streaming_Data.csv")

df = pd.read_csv(raw_path)
print(df.head())

# Drop duplicates
df = df.drop_duplicates()

# Genre fix for there are evident mistakes
genre_fix = {
    'Taylor Swift': 'Pop',
    'Ed Sheeran': 'Pop',
    'Bad Bunny': 'Reggaeton',
    'The Weeknd': 'R&B',
    'Billie Eilish': 'Indie',
    'Ariana Grande': 'Pop',
    'Doja Cat': 'Pop',
    'Dua Lipa': 'Pop',
    'Post Malone': 'Hip Hop',
    'SZA': 'R&B',
    'BLACKPINK': 'K-pop',
    'BTS': 'K-pop',
    'Karol G': 'Reggaeton'
}
df['Genre'] = df['Artist'].map(genre_fix).fillna(df['Genre'])

df['Platform Type'] = df['Platform Type'].str.strip().str.title()

# Convert numeric columns to proper numeric types
num_cols = ['Monthly Listeners (Millions)', 'Total Streams (Millions)', 'Total Hours Streamed (Millions)',
            'Avg Stream Duration (Min)', 'Streams Last 30 Days (Millions)', 'Skip Rate (%)']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Reset index for clean dataset
df_clean = df.reset_index(drop=True)
print("清洗后记录数:", len(df_clean))
print(df_clean.head())

# Save cleaned data
df_clean.to_csv(clean_path, index=False)
print(f"清洗后的数据已保存到: {clean_path}")