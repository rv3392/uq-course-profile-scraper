import dataclasses
import enum
import typing

@dataclasses.dataclass
class CourseClass:
    """A class (tutorial, practical, lecture, etc.) within a course.

    Attributes:
        hours (int): the length of the class in whole hours
        class_type (str): the type of the class (tutorial, etc.)
    """

    hours: int
    class_type: str

@dataclasses.dataclass
class CourseDetails:
    """Details of a course.

    Attributes:
        course_code (str): the course code with 4 letters and 4 
            digits (e.g. CSSE1001, MATH1051, COMP3506)
        course_title (str): a descriptive name of the course 
            officially used by the university
        course_description (str): a long description for the course
        cooordinating_unit (str): name of the running school
        semester (str): semester these details are for
        mode (str): mode these details are for
        level (str): undergraduate, postgraduate
        location (str): the campus these details are for
        num_units (int): the number of units the course is worth
        classes (List[CourseClass]): the classes the course
            contains and the number of hours for each
    """

    course_code: str
    course_title: str
    course_description: str
    coordinating_unit: str
    semester: str
    mode: str
    level: str
    location: str
    num_units: int
    contact_hours: typing.List[CourseClass]

@dataclasses.dataclass
class CourseStaff:
    """A member of staff involved with running the course.

    Attributes:
        name (str): name of staff member
        staff_type (str): lecturer, coordinator, etc.
        email (str): email contact of staff member
    """

    name: str
    staff_type: str
    email: str

@dataclasses.dataclass
class Assessment:
    """ Details for a particular assessment of a class.

    Attributes:
        task (str): A short description of the assessment task
        due_date (str): The due date of the assessment
        weighting (int): Percentage weighting of the assessment
        description (str): A long description of the assessment
    """

    task: str
    due_date: str
    weighting: int
    description: str

@dataclasses.dataclass
class CourseProfile:
    """The programmatic representation of a UQ course profile.
        
    Attributes:
        details (CourseDetails): the details of a course
        staff (List[CourseStaff]): a list of course staff
        prerequisites (List[str]): a list of course prerequisites
        assessments (List[Assessment]): a list of assessment and details
    """

    details: CourseDetails
    staff: typing.List[CourseStaff]
    prerequisites: typing.List[str]
    assessments: typing.List[Assessment]

