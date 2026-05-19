-- break by bins in interval of 5 years
-- find avg score for each bin

SELECT
    (year / 5) * 5 AS year_bin,
    AVG(score) AS avg_score
FROM anime
WHERE year IS NOT NULL
  AND score IS NOT NULL
GROUP BY year_bin
ORDER BY avg_score DESC;
