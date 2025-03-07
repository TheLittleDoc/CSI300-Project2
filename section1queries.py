import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#dotenv support
from dotenv import dotenv_values

# Load environment variables
env_path = '.env'
env = dotenv_values(env_path)

import warnings
warnings.filterwarnings('ignore')

def plot_bar_graph(data, x_axis, y_axis, x_label, y_label, title, visible_x=True, ymin=None, ymax=None):
    """Function to plot a bar graph

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :param visible_x: Whether to display the x_axis label (bool, default True)
    :param ymin: If included, the minimum value for the y-axis (float, default None)
    :param ymax: If included, the maximum value for the y-axis (float, default None)
    :return: None, directly displays with matplotlib
    """
    plt.figure(figsize=(10, 6))

    # Generate colors based on the number of bars
    colors = cm.viridis(np.linspace(0, 1, len(data[x_axis])))

    plt.bar(data[x_axis], data[y_axis], color = colors)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)

    # Set y-axis limits if necessary
    if ymin is not None and ymax is not None:
        plt.ylim(ymin, ymax)


    # Hide x-axis labels if necessary
    if not visible_x:
        plt.xticks(ticks=range(len(data[x_axis])), labels=['']*len(data[x_axis]))
        
    plt.tight_layout()
    plt.show()


def plot_box_graph(data, x_axis, y_axis, x_label, y_label, title):
    """Function to plot a box plot

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :return: None, directly displays with matplotlib
    """
    plt.figure(figsize=(10, 6))

    plt.boxplot(data[y_axis])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(ticks=range(len(data[x_axis])), labels=data[x_axis], rotation=45)
    plt.tight_layout()
    plt.show()


def plot_line_graph(data, x_axis, y_axis, x_label, y_label, title, ymin=None, ymax=None):
    """Function to plot a line graph

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :param ymin: If included, the minimum value for the y-axis (float, default None)
    :param ymax: If included, the maximum value for the y-axis (float, default None)
    :return: None, directly displays with matplotlib
    """
    plt.figure(figsize=(10, 6))

    plt.plot(data[x_axis], data[y_axis])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Set y-axis limits if necessary
    if ymin is not None and ymax is not None:
        plt.ylim(ymin, ymax)

    plt.tight_layout()
    plt.show()


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=env.get("PASSWORD"),
        database="sakila"
    )

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
    SELECT c.name AS category_name, AVG(f.rental_rate) AS avg_rental_rate 
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
    LIMIT 5;
    """

    return pd.read_sql(query, conn, params=(selected_category_name,))


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


if __name__ == "__main__":
    conn = create_connection()

    if conn.is_connected():
        print("Database connection established.")


    # Eddie's section
    rental_counts = query_customer_rental_counts(conn)
    print(rental_counts.head())
    plot_bar_graph(rental_counts, 'first_name', 'purchase_count', 'Customers', 'Rental Count', 'Customer Rental Counts', False)

    avg_rental_duration = query_avg_rental_duration(conn)
    print(avg_rental_duration.head())
    plot_bar_graph(avg_rental_duration, 'first_name', 'avg_hours_rented', 'Customers', 'Avg Hours Rented', 'Avg Hours Rented per Customer', False)

    june_movie_counts = query_june_movie_counts(conn)
    print(june_movie_counts.head())
    plot_bar_graph(june_movie_counts, 'event_type', 'count', 'Event Type', 'Movie Count', 'Movie Rental Counts in June')

    # Joseph's section
    category_rental_counts = query_category_rental_counts(conn)
    print(category_rental_counts.head())

    avg_category_rental_rate = query_avg_category_rental_rate(conn)
    print(avg_category_rental_rate)

    film_category_ranking = query_film_category_ranking(conn, "Comedy")
    print(film_category_ranking)

    # Ely's section
    total_revenue_per_store = query_total_revenue_per_store(conn)
    print(total_revenue_per_store)
    # zoom in on y axis to show the difference in revenue
    # min is 5% below the lowest value and max is 5% above the highest value
    ymin = total_revenue_per_store['total_revenue'].min() * 0.95
    ymax = total_revenue_per_store['total_revenue'].max() * 1.05
    plot_bar_graph(total_revenue_per_store, 'city', 'total_revenue', 'City', 'Total Revenue', 'Total Revenue per Store', True, ymin, ymax)

    average_payment_per_transaction = query_average_payment_per_transaction(conn)
    print(average_payment_per_transaction)
    #plot_box_graph(average_payment_per_transaction, 'avg_payment', 'avg_payment', 'Average Payment', 'Average Payment per Transaction', 'Average Payment per Transaction')

    monthly_revenue = query_monthly_revenue(conn)
    print(monthly_revenue)
    ymin = 0
    ymax = monthly_revenue['total_revenue'].max() * 1.5
    plot_line_graph(monthly_revenue, 'month', 'total_revenue', 'Month', 'Total Revenue', 'Total Revenue per Month', ymin, ymax)

    conn.close()