SELECT strftime("%Y", date) AS Year, SUM(n_killed+n_injured) AS Incidents
FROM "Gun Violence"
GROUP BY strftime("%Y", date)