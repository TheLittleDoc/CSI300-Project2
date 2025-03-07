import pandas as pd


def query_customer_rental_counts(conn):
    """Queries overall customer rental counts.

    Written by Eddie
    """
    query = """
    SELECT b.first_name, COUNT(a.customer_id) AS purchase_count
    FROM sakila.rental AS a
    JOIN sakila.customer AS b ON a.customer_id = b.customer_id
    GROUP BY first_name
    ORDER BY first_name;
    """
    return pd.read_sql(query, conn)


def query_avg_rental_duration(conn):
    """Queries average rental duration per customer.

    Written by Eddie
    """
    query = """
    SELECT b.first_name,
           AVG(TIMESTAMPDIFF(HOUR, a.rental_date, a.return_date)) AS avg_hours_rented
    FROM sakila.rental AS a
    JOIN sakila.customer AS b ON a.customer_id = b.customer_id
    GROUP BY first_name
    ORDER BY first_name;
    """
    return pd.read_sql(query, conn)


def query_june_movie_counts(conn):
    """Queries movie rental and return counts in June.

    Written by Eddie
    """
    query = """
    SELECT 'movies_rented' AS event_type, COUNT(*) AS count
    FROM sakila.rental
    WHERE MONTH(rental_date) = 6
    UNION ALL
    SELECT 'movies_returned' AS event_type, COUNT(*) AS count
    FROM sakila.rental
    WHERE MONTH(return_date) = 6;
    """
    return pd.read_sql(query, conn)
