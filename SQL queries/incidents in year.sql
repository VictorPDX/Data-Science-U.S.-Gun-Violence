SELECT notes, n_killed, n_injured, latitude, longitude
FROM "Gun Violence"
WHERE (n_killed + n_injured) > 0 AND date LIKE "%2017%"