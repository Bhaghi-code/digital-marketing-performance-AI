-- Channel performance (last 30 days) — core marketing analytics view
SELECT
  channel,
  SUM(sessions) AS sessions,
  SUM(signups) AS signups,
  ROUND(1.0 * SUM(signups) / NULLIF(SUM(sessions), 0), 4) AS signup_rate,
  ROUND(AVG(bounce_rate), 3) AS avg_bounce_rate,
  ROUND(AVG(avg_session_duration_sec), 0) AS avg_session_duration_sec
FROM daily_web_traffic
WHERE date = '2025-12-01'
GROUP BY channel
ORDER BY signup_rate DESC;
