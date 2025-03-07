import pandas as pd


def query_total_revenue_per_store(conn, store_id=0):
    """Queries the total revenue for a given store

    Selects the city name for each store, the name of the manager, and totals the revenue for each store.

    Written by Ely
    """
    if store_id == 0:
        query = """
        SELECT c.city, CONCAT(s.first_name, ' ', s.last_name) AS manager_name, SUM(p.amount) AS total_revenue
        FROM sakila.payment p
        JOIN sakila.staff s ON p.staff_id = s.staff_id
        JOIN sakila.store st ON s.store_id = st.store_id
        JOIN sakila.address a ON st.address_id = a.address_id
        JOIN sakila.city c ON a.city_id = c.city_id
        GROUP BY c.city, manager_name
        LIMIT 2000;
        """
        return pd.read_sql(query, conn)
    else:
        query = """
        SELECT c.city, CONCAT(s.first_name, ' ', s.last_name) AS manager_name, SUM(p.amount) AS total_revenue
        FROM sakila.payment p
        JOIN sakila.staff s ON p.staff_id = s.staff_id
        JOIN sakila.store st ON s.store_id = st.store_id
        JOIN sakila.address a ON st.address_id = a.address_id
        JOIN sakila.city c ON a.city_id = c.city_id
        WHERE st.store_id = %s
        GROUP BY c.city, manager_name
        LIMIT 2000;
        
        """

        return pd.read_sql(query, conn, params=(store_id,))


def query_average_payment_per_transaction(conn):
    """Queries the average payment amount per transaction

    Written by Ely
    """
    query = """
    
    SELECT AVG(p.amount) as avg_payment
    FROM sakila.payment p;

    """

    return pd.read_sql(query, conn)


def query_all_payments(conn):
    """Queries all payments for a box plot

    Written by Ely
    """
    query = """
    SELECT p.amount
    FROM sakila.payment p
    LIMIT 2000;
    """


    return pd.read_sql(query, conn)


def query_monthly_revenue(conn):
    """Queries the monthly revenue each month

    Written by Ely
    :param conn: Feed in the existing connection
    :return: DataFrame with total monthly revenue over time
    """

    query="""
    SELECT DATE_FORMAT(p.payment_date, '%Y-%m') as month, SUM(p.amount) as total_revenue
    FROM sakila.payment p
    GROUP BY month
    ORDER BY month;
    
    """
    return pd.read_sql(query, conn)
