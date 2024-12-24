from contex_managers import DatabaseConnect
import json


db_info = {
    'host': 'localhost',
    'database': 'nt',
    'user': 'postgres',
    'password': 'Muzaffar080403',
    'port': 5432
}

class Person:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age

    @staticmethod
    def get_all_persons():
        """
        this function get all persons
        :return:
        """
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM person;")
                return cur.fetchall()

    @staticmethod
    def get_one_person(person_id):
        """
        this function get one person
        :param person_id:
        :return:
        """
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM person WHERE id = %s;", (person_id,))
                return cur.fetchone()

    def save(self):
        """
        this function saves the person to the database
        :return:
        """
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO person (full_name, age) VALUES (%s, %s);",
                    (self.full_name, self.age)
                )
                conn.commit()
                print("Person successfully saved.")

    @staticmethod
    def update_person(person_id, full_name=None, age=None):
        """
        this function updates the person given by person_id
        :param person_id:
        :param full_name:
        :param age:
        :return:
        """
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                if full_name and age:
                    cur.execute(
                        "UPDATE person SET full_name = %s, age = %s WHERE id = %s;",
                        (full_name, age, person_id)
                    )
                elif full_name:
                    cur.execute(
                        "UPDATE person SET full_name = %s WHERE id = %s;",
                        (full_name, person_id)
                    )
                elif age:
                    cur.execute(
                        "UPDATE person SET age = %s WHERE id = %s;",
                        (age, person_id)
                    )
                conn.commit()
                print(f"Person with ID {person_id} successfully updated.")

    @staticmethod
    def delete_person(person_id):
        """
        this function deletes the person given by person_id
        :param person_id:
        :return:
        """
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM person WHERE id = %s;", (person_id,))
                conn.commit()
                print(f"Person with ID {person_id} successfully deleted.")

    @staticmethod
    def search_person(name):
        """
        this function search person by name
        :param name:
        :return:
        """
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM person WHERE full_name ILIKE %s;", (f"%{name}%",))
                return cur.fetchall()

    @staticmethod
    def export_to_json(filename):
        """
        this function exports json file to json file
        :param filename:
        :return:
        """
        data = Person.get_all_persons()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            print(f"Data exported to {filename}")

    @staticmethod
    def import_from_json(filename):
        """
        this function imports data from json file
        :param filename:
        :return:
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            with DatabaseConnect(**db_info) as conn:
                with conn.cursor() as cur:
                    for person in data:
                        cur.execute(
                            "INSERT INTO person (id, full_name, age) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                            (person[0], person[1], person[2])
                        )
                    conn.commit()
                    print(f"Data imported from {filename}")

# Statistika funksiyasi
def get_statistics():
    """
    this function get statistics from database
    :return:
    """
    with DatabaseConnect(**db_info) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(age) AS average_age, COUNT(*) AS total_persons FROM person;")
            return cur.fetchone()


if __name__ == '__main__':
    sherali = Person('Sherali Olimov', 25)
    sherali.save()

    print(Person.get_all_persons())

    print(Person.get_one_person(1))

    Person.update_person(1, full_name="Sherali Olimov", age=30)

    print(Person.search_person("Sherali"))

    # Person.delete_person(1)

    Person.export_to_json('persons.json')

    Person.import_from_json('persons.json')

    print(get_statistics())
