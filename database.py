import sqlite3
import bcrypt


def password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
class Database:
    def __init__(self, db_name="password_list.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Database created and connected")
        self.create_table()



    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS password_list (id INTEGER PRIMARY KEY AUTOINCREMENT, platform TEXT, username TEXT,password TEXT)")

        self.conn.commit()

    def show_all_passwords(self):
        self.cursor.execute("SELECT * FROM password")
        print(self.cursor.fetchall())
        return self.cursor.fetchall()
    def update_password(self, platform):
            platform = platform.lower()
            print(f"Updating username and password for {platform}...")
            self.cursor.execute("SELECT * FROM password WHERE platform =?", (platform,))
            changed_entry = self.cursor.fetchone()
            if changed_entry:
                self.cursor.execute("UPDATE password SET username=?, password=? WHERE platform=?",
                                (new_username, new_password, platform))
                print(f"Username and password updated successfully for {platform} ")
                self.conn.commit()
            else:
             print("Entry not updated")

    def add_password(self, platform, username, password):
        self.cursor.execute("SELECT * FROM password WHERE platform =?", (platform,))
        existing_entry = self.cursor.fetchone()
        if existing_entry:
                choice = input(f"{platform} already exists. Do you want to update the existing entry? (Y/N): ")
                if choice.lower() == "y":
                    self.update_password(platform)
        else:
            platform = platform.lower()
            hashed_password = password_hash(password)
            self.cursor.execute("INSERT INTO password (platform, username, password) VALUES (?,?,?)",
            (platform, username, hashed_password))
            self.conn.commit()

    def delete_password(self, platform):
        platform = platform.lower()
        self.cursor.execute("SELECT * FROM password WHERE platform =?", (platform,))
        existing_entry = self.cursor.fetchone()
        if existing_entry:
            self.cursor.execute("DELETE FROM password WHERE platform=?", (platform,))
            self.conn.commit()
            print("Platform deleted successfully")
        else: print("Platform not found")

    def quit_database(self):
        self.conn.close()
        print("Database connection closed")

db = Database()

while True:
    print("\nChoose an action:")
    print("1. Add a new password")
    print("2. Update an existing password")
    print("3. Delete a password")
    print("4. Show all passwords")
    print("5. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        platform = input("Enter platform: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        db.add_password(platform,username, password)
    elif choice == "2":
        platform = input("Enter the platform to update: ")
        db.update_password(platform)
        new_username = input("Enter new username: ")
        new_password = input("Enter new password: ")
    elif choice == "3":
        platform = input("Enter the platform to delete: ")
        db.delete_password(platform)
    elif choice == "4":
        db.show_all_passwords()
    elif choice == "5":
        db.quit_database()
        break
    else:
        print("Invalid choice. Please try again.")