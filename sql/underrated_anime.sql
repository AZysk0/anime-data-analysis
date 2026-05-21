SELECT title_english, score, members 
FROM anime
WHERE members < 10000 AND score > 7.5
ORDER BY members ASC, score DESC;
