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
    plot_bar_graph(category_rental_counts, 'category_name', 'total_rentals', 'Category Name', 'Total Rentals', "Total rentals per category")

    avg_category_rental_rate = query_avg_category_rental_rate(conn)
    plot_bar_graph(avg_category_rental_rate, 'category_name', 'avg_rental_rate', 'Category Name', 'Average Rental Rate', 'Rental rate by category')
    print(avg_category_rental_rate)

    top_music_films = query_film_category_ranking(conn, "Music")
    print(top_music_films)
    plot_bar_graph(top_music_films, 'title', 'rental_count', 'Title', 'Rental Count', "Top rented music films")

    top_travel_films = query_film_category_ranking(conn, "Travel")
    print(top_travel_films)
    plot_bar_graph(top_travel_films, 'title', 'rental_count', 'Title', 'Rental Count', "Top rented Travel films")

    top_sport_films = query_film_category_ranking(conn, "Sports")
    print(top_sport_films)
    plot_bar_graph(top_sport_films, 'title', 'rental_count', 'Title', 'Rental Count', "Top rented Sports films")

    top_action_films = query_film_category_ranking(conn, "Action")
    print(top_action_films)
    plot_bar_graph(top_action_films, 'title', 'rental_count', 'Title', 'Rental Count', "Top rented Action films")


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
    plot_box_graph(all_payments, 'amount', 'amount', 'Payment Amount', 'Payment Amount', 'All Payments')

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