from sqlmodel import Session
from database import engine
from models import Student

def create_db_and_data():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        if session.query(Student.first()):
            print("The database is already initialized.")
            return

        student1 = Student(name="Anna", age=20)
        student2 = Student(name="Mario", age=18)

        session.add_all([student1, student2])
        session.commit()

        print("Database created and initialized successfully.")

if __name__ == "__name__":
    create_db_and_data()
