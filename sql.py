import pandas as pd
import sqlite3

# Read CSV
df = pd.read_parquet("data/anime_processed.parquet")

# Connect to SQLite database
conn = sqlite3.connect("sql/anime.db")

# Automatically create table + columns
df.to_sql("anime", conn, if_exists="replace", index=False)

conn.close()

