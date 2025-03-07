import pandas as pd

def query_total_rental_per_actor(conn):
    """Queries the total number of rentals associated with each actor

    Written by Elysium
    :param conn: Feed in the existing connection
    :return: DataFrame with total rental counts per actor
    """

    query="""
    SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name, COUNT(r.rental_id) AS rental_count
    FROM sakila.rental r 
    JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
    JOIN sakila.film_actor fa ON i.film_id = fa.film_id
    JOIN sakila.actor a ON fa.actor_id = a.actor_id
    GROUP BY actor_name
    ORDER BY rental_count DESC
    LIMIT 50;
    
    """
    return pd.read_sql(query, conn)


def query_actor_performance_on_category(conn, category_name):
    """Analyze actor performance in a specific category

    :param conn: Feed in the existing connection
    :param category_name: The category name (string) to filter by
    :return: DataFrame with actor performance in the specified category
    """

    query="""
    SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name, COUNT(r.rental_id) AS rental_count
    FROM sakila.rental r
    JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
    JOIN sakila.film_actor fa ON i.film_id = fa.film_id
    JOIN sakila.actor a ON fa.actor_id = a.actor_id
    JOIN sakila.film_category fc ON i.film_id = fc.film_id
    JOIN sakila.category c ON fc.category_id = c.category_id
    WHERE c.name = %s
    GROUP BY actor_name
    ORDER BY rental_count DESC
    LIMIT 50;
    """

    return pd.read_sql(query, conn, params=(category_name,))


def query_top_ten_actors(conn):
    """Queries the top ten actors by rental count

    Written by Elysium
    :param conn: Feed in the existing connection
    :return: DataFrame with the top ten actors by rental count
    """

    query="""
    SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor_name, COUNT(r.rental_id) AS rental_count
    FROM sakila.rental r 
    JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
    JOIN sakila.film_actor fa ON i.film_id = fa.film_id
    JOIN sakila.actor a ON fa.actor_id = a.actor_id
    GROUP BY actor_name
    ORDER BY rental_count DESC
    LIMIT 10;
    """
    return pd.read_sql(query, conn)