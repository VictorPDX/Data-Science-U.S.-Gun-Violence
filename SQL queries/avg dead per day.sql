SELECT date AS Date, AVG(Deaths) as "Avg Dead per Day"
FROM (
        SELECT date, SUM(n_killed) as Deaths
        FROM "Gun Violence"
        GROUP BY date
    )
GROUP BY date
ORDER BY date ASC


