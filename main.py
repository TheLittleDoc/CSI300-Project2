import mysql.connector

#dotenv support
from dotenv import dotenv_values

from eddie import query_customer_rental_counts, query_avg_rental_duration, query_june_movie_counts
from ely import query_total_revenue_per_store, query_average_payment_per_transaction, query_monthly_revenue, query_all_payments
from graph_utilities import plot_bar_graph, plot_line_graph, plot_box_graph
from joe import query_category_rental_counts, query_avg_category_rental_rate, query_film_category_ranking
from shared import query_total_rental_per_actor, query_actor_performance_on_category, query_top_ten_actors

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
    # plot_box_graph(avg_rental_duration, 'avg_hours_rented', 'avg_hours_rented', 'Average Hours Rented', 'Average Hours Rented per Customer', 'Average Hours Rented per Customer', False)

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
    all_payments = query_all_payments(conn)
    plot_box_graph(all_payments, 'payment_id', 'amount', 'Payment ID', 'Amount', 'All Payments', False)

    monthly_revenue = query_monthly_revenue(conn)
    print(monthly_revenue)
    ymin = 0
    ymax = monthly_revenue['total_revenue'].max() * 1.5
    plot_line_graph(monthly_revenue, 'month', 'total_revenue', 'Month', 'Total Revenue', 'Total Revenue per Month', ymin, ymax)

    # Shared sections
    rental_counts_per_actor = query_total_rental_per_actor(conn)
    print(rental_counts_per_actor.head())
    plot_bar_graph(rental_counts_per_actor, 'actor_name', 'rental_count', 'Actor', 'Total Rentals', 'Total Rentals per Actor', True)

    focused_actors = query_actor_performance_on_category(conn, "Comedy")
    print(focused_actors.head())
    plot_bar_graph(focused_actors, 'actor_name', 'rental_count', 'Actor', 'Total Rentals', 'Total Rentals per Actor in Comedy', True)

    top_ten = query_top_ten_actors(conn)
    print(top_ten.head())
    plot_bar_graph(top_ten, 'actor_name', 'rental_count', 'Actor', 'Total Rentals', 'Top Ten Actors by Rental Count', True)


    conn.close()