SELECT state AS State, MAX(n_killed) as Dead
FROM "Gun Violence"
GROUP BY state
ORDER BY n_killed DESC





