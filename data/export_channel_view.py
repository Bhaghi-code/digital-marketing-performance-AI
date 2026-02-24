import sqlite3
import pandas as pd

DB_PATH = "data/marketing.db"

query = """
SELECT
  channel,
  SUM(sessions) AS sessions,
  SUM(signups) AS signups,
  ROUND(1.0 * SUM(signups) / NULLIF(SUM(sessions), 0), 4) AS signup_rate,
  ROUND(AVG(bounce_rate), 3) AS avg_bounce_rate,
  ROUND(AVG(avg_session_duration_sec), 0) AS avg_session_duration_sec
FROM daily_web_traffic
WHERE date >= '2025-12-01'
GROUP BY channel
ORDER BY signup_rate DESC;
"""

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query(query, conn)
conn.close()

df.to_csv("data/channel_last30.csv", index=False)

print("Exported data/channel_last30.csv")