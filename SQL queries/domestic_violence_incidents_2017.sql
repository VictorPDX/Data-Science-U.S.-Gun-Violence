SELECT state, count(*) AS incidents
FROM "Gun Violence"
WHERE incident_characteristics LIKE '%Domestic Violence%'
	AND date < 2018 AND date >= 2017
GROUP BY state;






