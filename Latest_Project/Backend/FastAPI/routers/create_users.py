import pyodbc
import bcrypt

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=YOUR_SERVER_NAME;"
    "Database=YOUR_DATABASE_NAME;"
    "Trusted_Connection=yes;"
)

def insert_user(username, plain_password, role):
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )
    conn.commit()
    conn.close()
    print(f"User {username} created with role {role}")

# Example usage
insert_user("alice", "alice123", "admin")
insert_user("bob", "bob456", "customer")


