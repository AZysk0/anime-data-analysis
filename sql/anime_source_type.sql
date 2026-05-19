SELECT 
    source,
    COUNT(*) AS count
FROM anime
GROUP BY source
ORDER BY count DESC;
