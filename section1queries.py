import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import warnings
warnings.filterwarnings('ignore')

def plot_bar_graph(data, x_axis, y_axis, x_label, y_label, title, visible_x=True):
    """Function to plot a bar graph

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :param visible_x: Whether to display the x_axis label (bool, default True)
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

    # Hide x-axis labels if necessary
    if not visible_x:
        plt.xticks(ticks=range(len(data[x_axis])), labels=['']*len(data[x_axis]))
        
    plt.tight_layout()
    plt.show()


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="park1city",
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

if __name__ == "__main__":
    conn = create_connection()

    if conn.is_connected():
        print("Database connection established.")

    data_1 = query_customer_rental_counts(conn)
    print(data_1.head())
    plot_bar_graph(data_1, 'first_name', 'purchase_count', 'Customers', 'Rental Count', 'Customer Rental Counts', False)

    data_2 = query_avg_rental_duration(conn)
    print(data_2.head())
    plot_bar_graph(data_2, 'first_name', 'avg_hours_rented', 'Customers', 'Avg Hours Rented', 'Avg Hours Rented per Customer', False)

    data_3 = query_june_movie_counts(conn)
    print(data_3.head())
    plot_bar_graph(data_3, 'event_type', 'count', 'Event Type', 'Movie Count', 'Movie Rental Counts in June')

    conn.close()