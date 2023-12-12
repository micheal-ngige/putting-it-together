import sqlite3

CONN = sqlite3.connect('lib/dogs.db')

CURSOR = CONN.cursor()

class Dog:

    pass

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Initialize id attribute

    @staticmethod
    def create_table():
        # Define the SQL statement to create the dogs table
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @staticmethod
    def drop_table():
        # Define the SQL statement to drop the dogs table if it exists
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        # Define the SQL statement to insert a new dog instance into the database
        sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid  # Set the id attribute

    @classmethod
    def create(cls, name, breed):
        # Create a new instance of Dog and save it to the database
        dog = cls(name, breed)
        dog.save()
        return dog

    @staticmethod
    def new_from_db(row):
        # Create a new dog instance from a database row
        id, name, breed = row
        dog = Dog(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        # Fetch all records from the database and return a list of dog instances
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        # Find a dog instance by name from the database
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        # Find a dog instance by id from the database
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        # Update the corresponding database record with new attribute values
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()