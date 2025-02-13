import tkinter as tk
from tkinter import ttk, messagebox
import cx_Oracle

# Database connection
dsn = cx_Oracle.makedsn(
    host="oracle.scs.ryerson.ca",
    port=1521,
    sid="orcl"
)

conn = cx_Oracle.connect(
    user="",
    password="",
    dsn=dsn
)
cur = conn.cursor()

# SQL Statements


# List of queries
queries = [
    # count the number of Books written by a specific Author ('Agatha Christie')
    """
    SELECT Author_name AS "Author", COUNT(Book.book_id) AS "Number of Books"
    FROM Author
    JOIN Book_Author ON Author.author_id = Book_Author.author_id
    JOIN Book ON Book_Author.book_id = Book.book_id
    WHERE Author_name = 'Agatha Christie'
    GROUP BY Author_name;
    """,
    
    # get categories ordered by name:
    """
    SELECT *
    FROM Category
    ORDER BY category_name;
    """,
    
    # get publisher details by publisher_id
    """
    SELECT *
    FROM Publisher
    WHERE publisher_id = 1;
    """,
    
    # get patrons with a specific email:
    """
    SELECT *
    FROM Patron
    WHERE patron_email = 'example@example.com';
    """,
    
    # list all books in the Science Fiction category
    """
    SELECT Book.title AS "Book Title"
    FROM Book
    JOIN Category ON Book.category_id = Category.category_id
    WHERE category_name = 'Science Fiction';
    """,
    
    # get books written by a specific author:
    """
    SELECT *
    FROM Book_author
    WHERE author_id = 3;   
    """,
    
    # get all book copies published by a specific publisher:
    """
    SELECT *
    FROM Book_Copy
    WHERE publisher_id = 4;
    """,
    
    # list all patron id checkouts that are returned
    """
    SELECT patron_id
    FROM CHECKOUT
    WHERE is_returned = 'Y';
    """,
    
    # get all holds that end before a certain date:
    """
    SELECT *
    FROM Hold
    WHERE end_time < TO_DATE('2024-12-31', 'YYYY-MM-DD');
    """,
    
    # get all waitlisted patrons for a specific book:
    """
    SELECT *
    FROM Waitlist
    WHERE book_id = 2;
    """,
    
    # list all notifications sent to a specific patron ('Jane Smith')
    """
    SELECT Notification.notification_type AS "Notification Type", Notification.time_sent AS "Time Sent"
    FROM Notification
    JOIN Patron ON Notification.patron_id = Patron.patron_id
    WHERE Patron.patron_name = 'Jane' AND Patron.patron_surname = 'Smith';
    """,
    
    # List all books that have at least 2 copies in the library
    """
    SELECT Book.title AS "Book Title"
    FROM Book
    JOIN Book_Copy ON Book.book_id = Book_Copy.book_id
    GROUP BY Book.title
    HAVING COUNT(Book_Copy.copy_id) >= 2;
    """,
    
    # List all patrons who have checked out a book and received a notification for that book 
    """
    SELECT DISTINCT p.patron_name || ' ' || p.patron_surname AS "Patron Name"
    FROM Patron p
    JOIN Checkout c ON p.patron_id = c.patron_id
    WHERE EXISTS (
        SELECT *
        FROM Notification n
        WHERE n.patron_id = p.patron_id
        AND n.notification_type = 'end_date_notification'
        AND n.patron_id = c.patron_id
        );
    """,
    
    # List all books that are in the "Science Fiction" or "History" category
    """
    SELECT b.title AS "Book Title"
    FROM Book b
    JOIN Category c ON b.category_id = c.category_id
    WHERE c.category_name = 'Science Fiction'

    UNION

    SELECT b.title AS "Book Title"
    FROM Book b
    JOIN Category c ON b.category_id = c.category_id
    WHERE c.category_name = 'History';
    """,
    
    # Creates view table for checked out items that are not returned
    """
    CREATE VIEW Checkedout(checkout_id, book_id, copy_id, patron_id) 
    AS(SELECT checkout_id, book_id, copy_id, patron_id
    FROM CHECKOUT
    WHERE IS_RETURNED = 'N');
    """,
    
    # calculate the average number of books checked out per patron
    """
    SELECT AVG(Checkout_Count) AS "Average Checkouts Per Patron"
    FROM (
        SELECT patron.patron_id, COUNT(checkout.checkout_id) AS Checkout_Count
        FROM Patron
        LEFT JOIN Checkout ON patron.patron_id = checkout.patron_id  --Ensures that patrons with no checkouts are included in the calculation (with a count of 0).
        GROUP BY patron.patron_id
    );
    """
]
drop_table_statements = [
    "DROP TABLE Waitlist;"
    "DROP TABLE Notification;"
    "DROP TABLE Hold;"
    "DROP TABLE Checkout;"
    "DROP TABLE Book_Copy;"
    "DROP TABLE Book_Author;"
    "DROP TABLE Book;"
    "DROP TABLE Patron;"
    "DROP TABLE Publisher;"
    "DROP TABLE Category;"
    "DROP TABLE Author;"
    "DROP VIEW Checkedout;"
    "DROP VIEW List_Science_Fiction;"
    "DROP VIEW COUNT_COPIES;"
]

sql_create_statements = [
    """
    CREATE TABLE Author (
        author_id NUMBER PRIMARY KEY ,
        author_name VARCHAR2(255) NOT NULL
    );
   """,
   """
    CREATE TABLE Category (
        category_id NUMBER PRIMARY KEY ,
        category_name VARCHAR2(255) NOT NULL
    );
   """,
   """
    CREATE TABLE Publisher (
        publisher_id NUMBER PRIMARY KEY ,
        publisher_name VARCHAR2(255) NOT NULL
    );
   """,
   """
    CREATE TABLE Patron (
        patron_id NUMBER PRIMARY KEY ,
        patron_name VARCHAR2(255) NOT NULL ,
        patron_surname VARCHAR2(255) NOT NULL ,
        patron_email VARCHAR2(255) UNIQUE
    );
   """,
   """
    CREATE TABLE Book (
        book_id NUMBER PRIMARY KEY ,
        title VARCHAR2(255) NOT NULL ,
        category_id NUMBER NOT NULL ,
        FOREIGN KEY (category_id) REFERENCES Category(category_id)
    );

   """,
   """
    CREATE TABLE Book_author (
        book_id NUMBER NOT NULL,
        author_id NUMBER NOT NULL ,
        PRIMARY KEY(book_id , author_id) ,
        FOREIGN KEY (book_id) REFERENCES book(book_id),
        FOREIGN KEY (author_id) REFERENCES author(author_id)
    );
   """,
   """
    CREATE TABLE Book_Copy (
        copy_id NUMBER PRIMARY KEY ,
        year_published NUMBER(4,0) NOT NULL,
        publisher_id NUMBER NOT NULL ,
        book_id NUMBER NOT NULL ,
        FOREIGN KEY (book_id) REFERENCES book(book_id),
        FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
    );
   """,
   """
    CREATE TABLE Checkout (
        checkout_id NUMBER PRIMARY KEY ,
        start_time DATE DEFAULT SYSDATE ,
        end_time DATE NOT NULL ,
        book_id NUMBER NOT NULL,
        copy_id NUMBER NOT NULL ,
        patron_id NUMBER NOT NULL ,
        is_returned CHAR(1) CHECK (is_returned IN ('Y', 'N')) ,
        FOREIGN KEY (book_id) REFERENCES book(book_id),
        FOREIGN KEY (copy_id) REFERENCES book_copy(copy_id),
        FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
    );
   """,
    """
    CREATE TABLE Hold (
        hold_id NUMBER PRIMARY KEY ,
        start_time DATE DEFAULT SYSDATE ,
        end_time DATE NOT NULL ,
        patron_id NUMBER NOT NULL ,
        copy_id NUMBER NOT NULL ,
        FOREIGN KEY (copy_id) REFERENCES book_copy(copy_id),
        FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
    );
   """,
   """
    CREATE TABLE Waitlist (
        book_id NUMBER NOT NULL,
        patron_id NUMBER NOT NULL ,
        PRIMARY KEY (book_id, patron_id),
        FOREIGN KEY (book_id) REFERENCES book(book_id),
        FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
    );
   """,
    """
    CREATE TABLE Notification (
        notification_id NUMBER PRIMARY KEY ,
        time_sent DATE DEFAULT SYSDATE ,
        notification_type VARCHAR2(50) NOT NULL ,
        patron_id NUMBER NOT NULL ,
        FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
    );
   """


]

sql_populate_statements = [
    """
    INSERT INTO Author (author_id, author_name) VALUES (1, 'J.D. Salinger');
    INSERT INTO Author (author_id, author_name) VALUES (2, 'Isaac Asimov');
    INSERT INTO Author (author_id, author_name) VALUES (3, 'Agatha Christie');
    INSERT INTO Author (author_id, author_name) VALUES (4, 'David McCullough');
    """,
    """
    INSERT INTO Category (category_id, category_name) VALUES (1, 'Fiction');
    INSERT INTO category (category_id, category_name) VALUES (2, 'Science Fiction');
    INSERT INTO category (category_id, category_name) VALUES (3, 'Mystery');
    INSERT INTO category (category_id, category_name) VALUES (4, 'History');
    """,
    """
    INSERT INTO Publisher (publisher_id, publisher_name) VALUES (1, 'Little, Brown and Company');
    INSERT INTO publisher (publisher_id, publisher_name) VALUES (2, 'Random House');
    INSERT INTO publisher (publisher_id, publisher_name) VALUES (3, 'Penguin Books');
    SET DEFINE OFF;
    """,
    """
    INSERT INTO publisher (publisher_id, publisher_name) VALUES (4, 'Simon & Schuster');
    SET DEFINE ON;
    """,
    """
    INSERT INTO Patron (patron_id, patron_name, patron_surname, patron_email) VALUES (1, 'John', 'Doe', 'john.doe@example.com');
    INSERT INTO patron (patron_id, patron_name, patron_surname, patron_email) VALUES (2, 'Jane', 'Smith', 'janesmith@example.com');
    INSERT INTO patron (patron_id, patron_name, patron_surname, patron_email) VALUES (3, 'Alice', 'Johnson', 'alicejohnson@example.com');
    """,
    """
    INSERT INTO Book (book_id, title, category_id) VALUES (1, 'The Catcher in the Rye', 1);
    INSERT INTO book (book_id, title, category_id) VALUES (2, 'Foundation', 2);
    INSERT INTO book (book_id, title, category_id) VALUES (3, 'Murder on the Orient Express', 3);
    INSERT INTO book (book_id, title, category_id) VALUES (4, '1776', 4);
    """,
    """
    INSERT INTO Book_author (book_id, author_id) VALUES (1, 1);
    INSERT INTO book_author (book_id, author_id) VALUES (2, 2); 
    INSERT INTO book_author (book_id, author_id) VALUES (3, 3); 
    INSERT INTO book_author (book_id, author_id) VALUES (4, 4);   
    """,
    """
    INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (1, 1, 1, 1951);
    INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (4, 1, 4, 2024);
    INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (2, 2, 2, 1934);
    INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (3, 3, 3, 2005);
    """,
    """
    INSERT INTO Checkout (checkout_id, book_id, copy_id, patron_id, start_time, end_time ,is_returned) VALUES (1, 1, 1, 1, SYSDATE, SYSDATE + 14 , 'Y');
    INSERT INTO Checkout (checkout_id, book_id, copy_id, patron_id, start_time, end_time , is_returned) VALUES (2, 2, 2, 2, SYSDATE, SYSDATE + 20 , 'N'); 
    INSERT INTO Checkout (checkout_id, book_id, copy_id, patron_id, start_time, end_time , is_returned) VALUES (3, 3, 3, 3, SYSDATE, SYSDATE + 60, 'Y'); 
    """,
    """
    INSERT INTO hold (hold_id, copy_id, patron_id, start_time, end_time) VALUES (1, 1, 2, SYSDATE, SYSDATE + 7); 
    INSERT INTO hold (hold_id, copy_id, patron_id, start_time, end_time) VALUES (2, 2, 3, SYSDATE, SYSDATE + 7);
    INSERT INTO hold (hold_id, copy_id, patron_id, start_time, end_time) VALUES (3, 3, 1, SYSDATE, SYSDATE + 7); 
    """,
    """
    INSERT INTO waitlist (book_id, patron_id) VALUES (1, 1);
    INSERT INTO waitlist (book_id, patron_id) VALUES (2, 2);
    INSERT INTO waitlist (book_id, patron_id) VALUES (3, 3); 
    """,
    """
    INSERT INTO notification (notification_id, patron_id, time_sent, notification_type) VALUES (1, 1, SYSDATE, 'availability_notification');
    INSERT INTO notification (notification_id, patron_id, time_sent, notification_type) VALUES (2, 2, SYSDATE, 'end_date_notification');
    """
]

# Helper Function to Execute Queries
def execute_query(query):
    try:
        cur.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            result_window = tk.Toplevel(root)
            result_window.title("Query Results")
            tree = ttk.Treeview(result_window)
            tree.pack(expand=True, fill="both")

            # Get actual column names
            columns = [desc[0] for desc in cur.description]
            tree["columns"] = columns

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # Insert data
            for row in rows:
                tree.insert("", "end", values=row)

        else:
            conn.commit()
            if not query.strip().upper().startswith(("DROP", "CREATE", "INSERT")):
                messagebox.showinfo("Success", "Query executed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Functions for Menu Options
def drop_tables():
    try:
        for sql in drop_table_statements:
            execute_query(sql)
        messagebox.showinfo("Success", "All tables dropped successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_tables():
    try:
        for sql in sql_create_statements:
            execute_query(sql)
        messagebox.showinfo("Success", "All tables created successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def populate_tables():
    try:
        for sql in sql_populate_statements:
            execute_query(sql)
        messagebox.showinfo("Success", "All tables populated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def custom_query_window():
    query_window = tk.Toplevel(root)
    query_window.title("Custom Query")

    tk.Label(query_window, text="Enter SQL Query:").pack(pady=10)
    query_text = tk.Text(query_window, height=10, width=50)
    query_text.pack()

    def run_custom_query():
        query = query_text.get("1.0", tk.END).strip()
        execute_query(query)

    tk.Button(query_window, text="Execute", command=run_custom_query).pack(pady=10)

def predefined_queries_window():
    predefined_window = tk.Toplevel(root)
    predefined_window.title("Predefined Queries")

    tk.Label(predefined_window, text="Select a Predefined Query:").pack(pady=10)

    # Dropdown menu for predefined queries
    query_var = tk.StringVar(predefined_window)
    query_var.set("Select Query")
    query_dropdown = ttk.Combobox(predefined_window, textvariable=query_var, width=80)
    query_dropdown["values"] = queries
    query_dropdown.pack(pady=10)

    def run_predefined_query():
        selected_query = query_var.get()
        if selected_query and selected_query != "Select Query":
            execute_query(selected_query)
        else:
            messagebox.showwarning("Warning", "Please select a query.")

    tk.Button(predefined_window, text="Execute Query", command=run_predefined_query).pack(pady=10)

def on_close():
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error while closing resources: {e}")
    root.destroy()

# Main GUI Window
root = tk.Tk()
root.title("Database Management System")

tk.Label(root, text="Database Operations", font=("Helvetica", 16)).pack(pady=10)

tk.Button(root, text="Drop Tables", command=drop_tables).pack(pady=5)
tk.Button(root, text="Create Tables", command=create_tables).pack(pady=5)
tk.Button(root, text="Populate Tables", command=populate_tables).pack(pady=5)
tk.Button(root, text="Custom Query", command=custom_query_window).pack(pady=5)
tk.Button(root, text="Predefined Queries", command=predefined_queries_window).pack(pady=5)
tk.Button(root, text="Exit", command=on_close).pack(pady=10)

root.mainloop()

# Close database connection


root.protocol("WM_DELETE_WINDOW", on_close)
