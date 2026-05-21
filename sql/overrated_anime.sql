SELECT title_english, score, members 
FROM anime
WHERE members > 100000 AND score < 7
ORDER BY score DESC;
