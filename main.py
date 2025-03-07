import mysql.connector

#dotenv support
from dotenv import dotenv_values

from eddie import query_customer_rental_counts, query_avg_rental_duration, query_june_movie_counts
from ely import query_total_revenue_per_store, query_average_payment_per_transaction, query_monthly_revenue
from graph_utilities import plot_bar_graph, plot_line_graph
from joe import query_category_rental_counts, query_avg_category_rental_rate, query_film_category_ranking

# Load environment variables
env_path = '.env'
env = dotenv_values(env_path)

import warnings
warnings.filterwarnings('ignore')


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        # make a new file called .env with the contents 'PASSWORD="yourpassword"'
        password=env.get("PASSWORD"),
        database="sakila"
    )


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