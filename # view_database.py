# view_database.py
import sqlite3

def view_database():
    connection = sqlite3.connect('keywords_database.db')
    cursor = connection.cursor()

    # Get column information
    cursor.execute('PRAGMA table_info(keywords)')
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    
    # Get rows and calculate maximum column widths
    cursor.execute('SELECT * FROM keywords')
    rows = cursor.fetchall()
    max_widths = [max([len(str(row[i])) for row in rows] + [len(column_names[i])]) for i in range(len(column_names))]

    # Create a formatting string to align the columns nicely
    format_str = "| " + " | ".join(["{:<" + str(max_widths[i]) + "}" for i in range(len(max_widths))]) + " |"

    # Print header
    header_str = format_str.format(*column_names)
    print("+" + "-" * (len(header_str) - 2) + "+")
    print(header_str)
    print("+" + "-" * (len(header_str) - 2) + "+")

    # Print rows
    for row in rows:
        print(format_str.format(*row))

    print("+" + "-" * (len(header_str) - 2) + "+")
    
    connection.close()

if __name__ == "__main__":
    view_database()
