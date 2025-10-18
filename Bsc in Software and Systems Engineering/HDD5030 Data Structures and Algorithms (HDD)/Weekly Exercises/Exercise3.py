# Exercise 3 - Student Grade Management System

records = []
def add_record(student_id, name, course_id, score):
    record = {"student_id": student_id, "name": name,
              "course_id": course_id, "score": score}
    records.append(record)
    records.sort(key=lambda x: x["student_id"])
def display_records():
    if not records:
        print("No records found.")
    for r in records:
        print(r)
def delete_record(student_id, course_id):
    global records
    records = [r for r in records if not (r["student_id"] == student_id and r["course_id"] == course_id)]
def display_sorted_by_course():
    sorted_list = sorted(records, key=lambda x: (x["course_id"], -x["score"]))
    for r in sorted_list:
        print(r)
def query_by_student(student_id):
    found = False
    for r in records:
        if r["student_id"] == student_id:
            print(r)
            found = True
    if not found:
        print("Student not found.")

class Node:
    def __init__(self, student_id, name, course_id, score):
        self.student_id = student_id
        self.name = name
        self.course_id = course_id
        self.score = score
        self.next = None

    def __repr__(self):
        return f"({self.student_id}, {self.name}, {self.course_id}, {self.score})"

class LinkedList:
    def __init__(self):
        self.head = None

    def add_record(self, student_id, name, course_id, score):
        new_node = Node(student_id, name, course_id, score)
        if not self.head or student_id < self.head.student_id:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        while current.next and current.next.student_id < student_id:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def display(self, node=None):
        if node is None:
            node = self.head
        if not node:
            return
        print(node)
        self.display(node.next)

    def delete_record(self, student_id, course_id):
        current = self.head
        prev = None
        while current:
            if current.student_id == student_id and current.course_id == course_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev = current
            current = current.next

    def display_sorted_by_course(self):
        temp = []
        current = self.head
        while current:
            temp.append(current)
            current = current.next
        temp.sort(key=lambda x: (x.course_id, -x.score))
        for t in temp:
            print(t)

    def query_by_student(self, student_id, node=None):
        if node is None:
            node = self.head
        if not node:
            return
        if node.student_id == student_id:
            print(node)
        self.query_by_student(student_id, node.next)

def menu():
    ll = LinkedList()
    while True:
        print("\n===== Student Grade Management System =====")
        print("1. Add student record")
        print("2. Display all records (Sequential)")
        print("3. Delete a record (Sequential)")
        print("4. Display records sorted by course ID & score (Sequential)")
        print("5. Query records by student ID (Sequential)")
        print("6. Add student record (LinkedList)")
        print("7. Display all records (LinkedList)")
        print("8. Delete a record (LinkedList)")
        print("9. Display records sorted by course ID & score (LinkedList)")
        print("10. Query records by student ID (LinkedList)")
        print("0. Exit")

        choice = input("Select (0-10): ")

        if choice == "1":
            sid = input("Student ID: ")
            name = input("Name: ")
            cid = input("Course ID: ")
            score = int(input("Score: "))
            add_record(sid, name, cid, score)

        elif choice == "2":
            display_records()

        elif choice == "3":
            sid = input("Student ID: ")
            cid = input("Course ID: ")
            delete_record(sid, cid)

        elif choice == "4":
            display_sorted_by_course()

        elif choice == "5":
            sid = input("Student ID: ")
            query_by_student(sid)

        elif choice == "6":
            sid = input("Student ID: ")
            name = input("Name: ")
            cid = input("Course ID: ")
            score = int(input("Score: "))
            ll.add_record(sid, name, cid, score)

        elif choice == "7":
            ll.display()

        elif choice == "8":
            sid = input("Student ID: ")
            cid = input("Course ID: ")
            ll.delete_record(sid, cid)

        elif choice == "9":
            ll.display_sorted_by_course()

        elif choice == "10":
            sid = input("Student ID: ")
            ll.query_by_student(sid)

        elif choice == "0":
            break

        else:
            print("Invalid!")

if __name__ == "__main__":
    menu()

# AI Statement: AI tools such as VS Code Copilot were used to assist and 
# manage error in the development of this code.