import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import warnings
warnings.filterwarnings('ignore')

def plot_bar_graph(data, x_axis, y_axis, x_label, y_label, title, visible_x=True):
    #Function to plot a bar graph
    #Parameters:
    #data (dtype -> DataFrame)
    #column on x-axis (dytype -> string)
    #colum on y-axis (dtype -> string)
    #x-axis label (dtype -> string)
    #y-axis labal (dyype -> string)
    #title for the plot (dtype -> string)

    plt.figure(figsize=(10, 6))

    colors = cm.viridis(np.linspace(0, 1, len(data[x_axis]))) # Generate colors based on the number of bars

    plt.bar(data[x_axis], data[y_axis], color = colors)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)

    if not visible_x:
        # this line hides x axis labels which is important given how many customers
        # there are in the databases, can be enabled with a default parameter
        plt.xticks(ticks=range(len(data[x_axis])), labels=['']*len(data[x_axis]))
        
    plt.tight_layout()
    plt.show()

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "park1city",
    database = "sakila"
    )

if conn.is_connected():
    print("Established")

# Overall customer rental counts
query_1 = """
SELECT b.first_name, COUNT(a.customer_id) AS purchase_count
FROM sakila.rental AS a
JOIN sakila.customer AS b
ON a.customer_id = b.customer_id
GROUP BY first_name
ORDER BY first_name;
"""

# Computed average rental durations for each customer
query_2 = """
SELECT b.first_name,
AVG(TIMESTAMPDIFF(HOUR, a.rental_date, a.return_date)) AS avg_hours_rented
FROM sakila.rental AS a
JOIN sakila.customer AS b
ON a.customer_id = b.customer_id
GROUP BY first_name
ORDER BY first_name;
"""

# Total number of movies taken out
# and movies returned in a given month
# June in this example
query_3 = """
SELECT 'movies_rented' AS event_type, 
       COUNT(*) AS count
FROM sakila.rental
WHERE MONTH(rental_date) = 6
UNION ALL
SELECT 'movies_returned' AS event_type, 
       COUNT(*) AS count
FROM sakila.rental
WHERE MONTH(return_date) = 6;
SELECT * FROM sakila.rental
"""

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

data_1 = pd.read_sql(query_1, conn)
print(data_1.head())
plot_bar_graph(data_1, 'first_name', 'purchase_count', 'Customers', 'Rental Count', 'Customer Rental Counts', False)

data_2 = pd.read_sql(query_2, conn)
print(data_2.head())
plot_bar_graph(data_2, 'first_name', 'avg_hours_rented', 'Customers', 'Avg Hours Rented', 'Avg Hours Rented per Customer', False)

data_3 = pd.read_sql(query_3, conn)
print(data_3.head())
plot_bar_graph(data_3, 'event_type', 'count', 'Event Type', 'Movie Count', 'Movie Rental Counts in June')
