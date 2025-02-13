--CREATE TABLES WITH NO DEPENDANCIES---------------------------------------------
CREATE TABLE Author (
   author_id NUMBER PRIMARY KEY ,
   author_name VARCHAR2(255) NOT NULL
);

CREATE TABLE Category (
   category_id NUMBER PRIMARY KEY ,
   category_name VARCHAR2(255) NOT NULL
);

CREATE TABLE Publisher (
   publisher_id NUMBER PRIMARY KEY ,
   publisher_name VARCHAR2(255) NOT NULL
);

CREATE TABLE Patron (
   patron_id NUMBER PRIMARY KEY ,
   patron_name VARCHAR2(255) NOT NULL ,
   patron_surname VARCHAR2(255) NOT NULL ,
   patron_email VARCHAR2(255) UNIQUE
);
--CREATE TABLES WITH LOWER DEPENDANCIES-----------------------------------------
CREATE TABLE Book (
   book_id NUMBER PRIMARY KEY ,
   title VARCHAR2(255) NOT NULL ,
   category_id NUMBER NOT NULL ,
   FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

CREATE TABLE Book_author (
   book_id NUMBER NOT NULL,
   author_id NUMBER NOT NULL ,
   PRIMARY KEY(book_id , author_id) ,
   FOREIGN KEY (book_id) REFERENCES book(book_id),
   FOREIGN KEY (author_id) REFERENCES author(author_id)
);
--CREATE TABLES WITH HIGHER DEPENDANCIES----------------------------------------
CREATE TABLE Book_Copy (
   copy_id NUMBER PRIMARY KEY ,
   year_published NUMBER(4,0) NOT NULL,
   publisher_id NUMBER NOT NULL ,
   book_id NUMBER NOT NULL ,
   FOREIGN KEY (book_id) REFERENCES book(book_id),
   FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)
);

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

CREATE TABLE Hold (
   hold_id NUMBER PRIMARY KEY ,
   start_time DATE DEFAULT SYSDATE ,
   end_time DATE NOT NULL ,
   patron_id NUMBER NOT NULL ,
   copy_id NUMBER NOT NULL ,
   FOREIGN KEY (copy_id) REFERENCES book_copy(copy_id),
   FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
);

CREATE TABLE Waitlist (
   book_id NUMBER NOT NULL,
   patron_id NUMBER NOT NULL ,
   PRIMARY KEY (book_id, patron_id),
   FOREIGN KEY (book_id) REFERENCES book(book_id),
   FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
);

CREATE TABLE Notification (
   notification_id NUMBER PRIMARY KEY ,
   time_sent DATE DEFAULT SYSDATE ,
   notification_type VARCHAR2(50) NOT NULL ,
   patron_id NUMBER NOT NULL ,
   FOREIGN KEY (patron_id) REFERENCES patron(patron_id)
);

--Copy output and run to drop all tables
--select 'drop table ', table_name, 'cascade constraints;' from user_tables;

--Populating tables----------------------------------------------------

INSERT INTO Author (author_id, author_name) VALUES (1, 'J.D. Salinger');
INSERT INTO Author (author_id, author_name) VALUES (2, 'Isaac Asimov');
INSERT INTO Author (author_id, author_name) VALUES (3, 'Agatha Christie');
INSERT INTO Author (author_id, author_name) VALUES (4, 'David McCullough');

INSERT INTO Category (category_id, category_name) VALUES (1, 'Fiction');
INSERT INTO category (category_id, category_name) VALUES (2, 'Science Fiction');
INSERT INTO category (category_id, category_name) VALUES (3, 'Mystery');
INSERT INTO category (category_id, category_name) VALUES (4, 'History');

INSERT INTO Publisher (publisher_id, publisher_name) VALUES (1, 'Little, Brown and Company');
INSERT INTO publisher (publisher_id, publisher_name) VALUES (2, 'Random House');
INSERT INTO publisher (publisher_id, publisher_name) VALUES (3, 'Penguin Books');
SET DEFINE OFF;
-- allows for use of '&' character in the string, otherwise it is a substitution variable
INSERT INTO publisher (publisher_id, publisher_name) VALUES (4, 'Simon & Schuster');
SET DEFINE ON;

INSERT INTO Patron (patron_id, patron_name, patron_surname, patron_email) VALUES (1, 'John', 'Doe', 'john.doe@example.com');
INSERT INTO patron (patron_id, patron_name, patron_surname, patron_email) VALUES (2, 'Jane', 'Smith', 'janesmith@example.com');
INSERT INTO patron (patron_id, patron_name, patron_surname, patron_email) VALUES (3, 'Alice', 'Johnson', 'alicejohnson@example.com');

INSERT INTO Book (book_id, title, category_id) VALUES (1, 'The Catcher in the Rye', 1);
INSERT INTO book (book_id, title, category_id) VALUES (2, 'Foundation', 2);
INSERT INTO book (book_id, title, category_id) VALUES (3, 'Murder on the Orient Express', 3);
INSERT INTO book (book_id, title, category_id) VALUES (4, '1776', 4);

INSERT INTO Book_author (book_id, author_id) VALUES (1, 1);
INSERT INTO book_author (book_id, author_id) VALUES (2, 2); -- Foundation by Isaac Asimov
INSERT INTO book_author (book_id, author_id) VALUES (3, 3); -- Murder on the Orient Express by Agatha Christie
INSERT INTO book_author (book_id, author_id) VALUES (4, 4); -- 1776 by David McCullough

INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (1, 1, 1, 1951);
INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (4, 1, 4, 2024);
INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (2, 2, 2, 1934);
INSERT INTO book_copy (copy_id, book_id, publisher_id, year_published) VALUES (3, 3, 3, 2005);

INSERT INTO Checkout (checkout_id, book_id, copy_id, patron_id, start_time, end_time ,is_returned) VALUES (1, 1, 1, 1, SYSDATE, SYSDATE + 14 , 'Y'); -- John Doe checks out "Foundation"
INSERT INTO Checkout (checkout_id, book_id, copy_id, patron_id, start_time, end_time , is_returned) VALUES (2, 2, 2, 2, SYSDATE, SYSDATE + 20 , 'N'); -- Jane Smith checks out "Murder on the Orient Express"
INSERT INTO Checkout (checkout_id, book_id, copy_id, patron_id, start_time, end_time , is_returned) VALUES (3, 3, 3, 3, SYSDATE, SYSDATE + 60, 'Y'); -- Alice Johnson checks out "1776"

INSERT INTO hold (hold_id, copy_id, patron_id, start_time, end_time) VALUES (1, 1, 2, SYSDATE, SYSDATE + 7); -- Jane Smith holds a copy of "Foundation"
INSERT INTO hold (hold_id, copy_id, patron_id, start_time, end_time) VALUES (2, 2, 3, SYSDATE, SYSDATE + 7); -- Alice Johnson holds a copy of "Murder on the Orient Express"
INSERT INTO hold (hold_id, copy_id, patron_id, start_time, end_time) VALUES (3, 3, 1, SYSDATE, SYSDATE + 7); -- John Doe holds a copy of "1776"

INSERT INTO waitlist (book_id, patron_id) VALUES (1, 1); -- John Doe is waitlisted for "Foundation"
INSERT INTO waitlist (book_id, patron_id) VALUES (2, 2); -- Jane Smith is waitlisted for "Murder on the Orient Express"
INSERT INTO waitlist (book_id, patron_id) VALUES (3, 3); -- Alice Johnson is waitlisted for "1776"

INSERT INTO notification (notification_id, patron_id, time_sent, notification_type) VALUES (1, 1, SYSDATE, 'availability_notification');
INSERT INTO notification (notification_id, patron_id, time_sent, notification_type) VALUES (2, 2, SYSDATE, 'end_date_notification');

--CREATING QUIERIES----------------------------------------------------------------
--Author - count the number of Books written by a specific Author ('Agatha Christie')
SELECT Author_name AS "Author", COUNT(Book.book_id) AS "Number of Books"
FROM Author
JOIN Book_Author ON Author.author_id = Book_Author.author_id
JOIN Book ON Book_Author.book_id = Book.book_id
WHERE Author_name = 'Agatha Christie'
GROUP BY Author_name;

--Category - get categories ordered by name:
SELECT * 
FROM Category
ORDER BY category_name;

--Publisher - get publisher details by publisher_id
SELECT * 
FROM Publisher
WHERE publisher_id = 1;

--Patron - get patrons with a specific email:
SELECT * 
FROM Patron
WHERE patron_email = 'example@example.com';

--Book - list all books in the Science Fiction category
SELECT Book.title AS "Book Title"
FROM Book
JOIN Category ON Book.category_id = Category.category_id
WHERE category_name = 'Science Fiction';

--Book_author - get books written by a specific author:
SELECT * 
FROM Book_author
WHERE author_id = 3;

--Book_Copy - get all book copies published by a specific publisher:
SELECT * 
FROM Book_Copy
WHERE publisher_id = 4;

--Checkout - list all patron id checkouts that are returned
SELECT patron_id
FROM CHECKOUT
WHERE is_returned = 'Y';

--Hold - get all holds that end before a certain date:
SELECT * 
FROM Hold
WHERE end_time < TO_DATE('2024-12-31', 'YYYY-MM-DD');

--Waitlist - get all waitlisted patrons for a specific book:
SELECT * 
FROM Waitlist
WHERE book_id = 2;

--list all notifications sent to a specific patron ('Jane Smith')
SELECT Notification.notification_type AS "Notification Type", Notification.time_sent AS "Time Sent"
FROM Notification
JOIN Patron ON Notification.patron_id = Patron.patron_id
WHERE Patron.patron_name = 'Jane' AND Patron.patron_surname = 'Smith';

--VIEW TABLES----------------------------------------
--CHECKEDOUT - Creates view table for checked out items that are not returned
CREATE VIEW Checkedout(checkout_id, book_id, copy_id, patron_id) 
AS(SELECT checkout_id, book_id, copy_id, patron_id
FROM CHECKOUT
WHERE IS_RETURNED = 'N');


drop view List_Science_Fiction;
----List_Science_Fiction - List all titles where the books are science fiction
CREATE VIEW List_Science_Fiction(book_title) 
AS(SELECT title
FROM BOOK
JOIN CATEGORY ON BOOK.category_id = CATEGORY.category_id
WHERE CATEGORY.category_name = 'science fiction');

--count the number of copies of a specific book
CREATE VIEW COUNT_COPIES(title, copy_id, book_id)
AS(SELECT title, BOOK_COPY.copy_id, BOOK_COPY.book_id
FROM BOOK
JOIN BOOK_COPY ON BOOK.book_id = BOOK_COPY.book_id
WHERE BOOK.title = 'The Catcher in the Rye');
SELECT COUNT(copy_id) AS Number_of_copies FROM COUNT_COPIES;

--5 NEW QUERIES (using set-based keywords and aggregate functions)----------------
--List all books that have at least 2 copies in the library
SELECT Book.title AS "Book Title"
FROM Book 
JOIN Book_Copy ON Book.book_id = Book_Copy.book_id
GROUP BY Book.title
HAVING COUNT(Book_Copy.copy_id) >= 2;

--List all patrons who have checked out a book and received a notification for that book 
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

--List all books that are in the "Science Fiction" or "History" category
SELECT b.title AS "Book Title"
FROM Book b
JOIN Category c ON b.category_id = c.category_id
WHERE c.category_name = 'Science Fiction'

UNION

SELECT b.title AS "Book Title"
FROM Book b
JOIN Category c ON b.category_id = c.category_id
WHERE c.category_name = 'History';

--List all books that are in the "Science Fiction" category and are currently checked out
SELECT book.title AS "Science Fiction Books"
FROM Book
JOIN Category ON book.category_id = category.category_id
where category.category_name = 'Science Fiction'

MINUS

SELECT book.title AS "Returned Science Fiction Books"
FROM Book
JOIN Category ON book.category_id = category.category_id
JOIN Book_Copy ON book.book_id = book_copy.book_id
JOIN Checkout ON book_copy.copy_id = checkout.copy_id
WHERE category.category_name = 'Science Fiction' AND checkout.is_returned = 'Y'

--calculate the average number of books checked out per patron
SELECT AVG(Checkout_Count) AS "Average Checkouts Per Patron"
FROM (
    SELECT patron.patron_id, COUNT(checkout.checkout_id) AS Checkout_Count
    FROM Patron 
    LEFT JOIN Checkout ON patron.patron_id = checkout.patron_id  --Ensures that patrons with no checkouts are included in the calculation (with a count of 0).
    GROUP BY patron.patron_id
   );
