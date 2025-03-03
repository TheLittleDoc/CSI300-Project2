-- Overall customer rental counts
SELECT b.first_name, COUNT(a.customer_id) AS purchase_count
FROM sakila.rental AS a
JOIN sakila.customer AS b
ON a.customer_id = b.customer_id
GROUP BY first_name
ORDER BY first_name;

-- Computed average rental durations
-- for each customer
SELECT b.first_name,
AVG(TIMESTAMPDIFF(HOUR, a.rental_date, a.return_date)) AS avg_hours_rented
FROM sakila.rental AS a
JOIN sakila.customer AS b
ON a.customer_id = b.customer_id
GROUP BY first_name
ORDER BY first_name;

-- Total computed average rental durations
SELECT AVG(TIMESTAMPDIFF(HOUR, rental_date, return_date)) AS avg_hours_rented
FROM sakila.rental;

-- All rental data of rentals taken out
-- in a given month
-- June in this example
SELECT * FROM sakila.rental
WHERE MONTH(rental_date) = 6;

-- Total number of movies taken out
-- and movies returned in a given month
-- June in this example
SELECT COUNT(CASE WHEN MONTH(rental_date) = 6 THEN 1 END) AS movies_rented,
COUNT(CASE WHEN MONTH(return_date) = 6 THEN 1 END) AS movies_returned
FROM sakila.rental;




