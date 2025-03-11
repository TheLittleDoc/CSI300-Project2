import pandas as pd


def query_category_rental_counts(conn):
    """Queries aggregated rental counts for each film category.

    Written by Joseph
    """
    query = """
    SELECT c.name AS category_name, COUNT(r.rental_id) AS total_rentals
    FROM sakila.category c
    JOIN sakila.film_category fc ON c.category_id = fc.category_id
    JOIN sakila.film f ON fc.film_id = f.film_id
    JOIN sakila.inventory i ON f.film_id = i.film_id
    JOIN sakila.rental r ON i.inventory_id = r.inventory_id
    GROUP BY c.name
    ORDER BY total_rentals DESC;
    """

    return pd.read_sql(query, conn)


def query_avg_category_rental_rate(conn):
    """Queries the average rental rate grouped by category

    Written by Joseph
    """
    query = """
    SELECT c.name AS category_name, AVG(f.rental_rate / f.rental_duration) AS avg_rental_rate 
    FROM sakila.category c 
    JOIN sakila.film_category fc ON c.category_id = fc.category_id 
    JOIN sakila.film f ON fc.film_id = f.film_id 
    GROUP BY c.name 
    ORDER BY avg_rental_rate DESC;
    """

    return pd.read_sql(query, conn)


def query_film_category_ranking(conn, selected_category_name):
    """Queries ranking of films by rental count within a chosen category

    Written by Joseph
    """
    query = """
    SELECT f.title, COUNT(r.rental_id) AS rental_count
    FROM sakila.film f 
    JOIN sakila.film_category fc ON f.film_id = fc.film_id 
    JOIN sakila.category c ON fc.category_id = c.category_id 
    JOIN sakila.inventory i ON f.film_id = i.film_id 
    JOIN sakila.rental r ON i.inventory_id = r.inventory_id 
    WHERE c.name = %s
    GROUP BY f.title 
    ORDER BY rental_count DESC 
    LIMIT 90;
    """

    return pd.read_sql(query, conn, params=(selected_category_name,))