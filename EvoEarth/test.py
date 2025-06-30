import sqlite3

def print_all_students():
    # Connect to the database
    mydb = sqlite3.connect('Student.db')
    cursor = mydb.cursor()

    # Fetch all rows from the table `t`
    cursor.execute("SELECT * FROM tb")
    rows = cursor.fetchall()

    # Print each row nicely
    print("All Student Records:\n")
    for row in rows:
        user_id, name, age, skillset = row
        print(f"User ID: {user_id}")
        print(f"Name   : {name}")
        print(f"Age    : {age}")
        print(f"Skills : {skillset}")
        print("-" * 30)

    # Close the connection
    mydb.close()

# Call the function
print_all_students()
