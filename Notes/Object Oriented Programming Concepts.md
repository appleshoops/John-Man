In OOP, an object is anything of interest to the the program that you want to store data about. They are sometimes called entities. There are 4 main concepts relating to this.

## Abstraction
This concept means that when talking about an object, you only want to store attributes that are relevant to what you are creating. Each method (known as a function or subroutine in non-OOP coding) has its own attributes (known as variables in non-OOP coding) relating to it. 
### Classes
A class is a template written by a coder to define the attributes of an object and how to create it. They can contain properties and behaviours. Once a class is written, it can be repeated to make copies of the same object that is defined within it. This process is called **instantiation**. Classes are sometimes called types. Each object created by the same class can be assigned different properties, making them unique. 

## Encapsulation
This concept refers to hiding data and complexity to keep it safe from outside forces. With encapsulation, objects cannot alter the properties of another object when they interact. Classes are sometimes written by more experienced developers for others to use, which can then be packaged into class libraries. Examples of these are Python libraries like math or random. To use a class from a library, the user only needs to know how to interact with it, which keeps the classes hidden from the user and protecting the intellectual property of the developer who wrote it. 

## Inheritance
This concept means a class can inherit properties from another. If the class of "person" is used for all people, it could have the properties of first name, last name, date of birth and more; but the subclass of "employee" would inherit all of these properties from "person" because the have all of these attributes. They also have their own exclusive properties like job title, start date, and salary. This goes on and on represented by this diagram.
![[Pasted image 20250429101540.png]]Any class that derives from another class is called a subclass, and any class that has a subclass is called a superclass. 

## Classes and Instances
- Classes encapsulate data into a single unit to promote encapsulation and abstraction
- All objects are instances of a class that are exist in memory and can be manipulated
	- They have their own unique properties and attributes
### Creating a Class in Python
```python
class Student:
    # Constructor Method to initialise attributes
    def __init__(self, first_name, surname, dob, gender):
        self.student_first_name = first_name
        self.student_surname = surname
        self.student_dob = dob
        self.student_gender = gender

class Classroom:
    # Constructor Method (builder)
    def __init__(self, title):
        self.class_title = title
        self.students = []

    # Setter Method (writer)
    def add_student(self, first_name, surname, dob, gender):
        self.students.append(Student(first_name, surname, dob, gender))

    # Getter Method (reader)
    def find_student(self, dob): 
        for student in self.students: 
            if student.student_dob == dob: 
                return student
        return None
```

The init stands for initialisation which executes when an instance of the class is created. This is where the properties are assigned. You also need to include 'self' or it won't work.
