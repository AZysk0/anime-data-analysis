SELECT type, COUNT(*) AS count FROM anime
GROUP BY type
ORDER BY count DESC
