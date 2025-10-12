
from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List

app = FastAPI()


"""
Implement CRUD
"""
T = TypeVar("T")    # This line defines a type variable named T. It’s a placeholder type you can use inside generic classes.

class StudentData(BaseModel):
    student_roll: int
    student_name : str
    student_class : str
    student_contact: int
    student_address: str

class ApiResponseModel(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None  # optional means this field can be None
    status: bool

class SubjectData(BaseModel):
    subject_name: str
    subject_id: int
    subject_status: bool
    subject_description: str
    min_passing_marks: int

# This means: “students is a list that holds StudentData objects.”
students: List[StudentData] = [] # list of objects(dictionaries)

subjects: List[SubjectData] = []

# helper
def check_if_roll_no_exists(roll_no: int):
    for i, student in enumerate(students):
        if student.student_roll == roll_no:
            return True,i
        else:
            continue
    return False, None

def check_if_subject_id_exists(subject_id: int):
    for i, subject in enumerate(subjects):
        if subject.subject_id == subject_id:
            return True,i
        else:
            continue
    return False, None


@app.get("/")
def index():
    return "hello world"

# CREATE
@app.post("/students", response_model=ApiResponseModel[List[StudentData]])
def create_student(student_data: StudentData):
    try:
        exists, i = check_if_roll_no_exists(student_data.student_roll)
        if not exists:
            students.append(student_data)
            return ApiResponseModel(message="created successfully", data=[student_data], status=True)
        else:
            return ApiResponseModel(message="record already exists", data=None, status=False)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.get("/students", response_model=ApiResponseModel[List[StudentData]])
def fetch_students():
    try:
        if len(students) <= 0:
            return ApiResponseModel(message="data not found", data=[], status=False)
        else:
            return ApiResponseModel(message="data found", data=students, status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.get("/students/{rid}", response_model=ApiResponseModel[List[StudentData]])
def fetch_student_by_roll_no(rid: int):
    try:
        exists, i = check_if_roll_no_exists(rid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            return ApiResponseModel(message="data found", data=[students[i]], status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.put("/students/{rid}", response_model=ApiResponseModel[List[StudentData]])
def update_student(rid:int, student_data: StudentData):
    try:
        exists, i = check_if_roll_no_exists(rid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            if rid == student_data.student_roll:
                students[i] = student_data
                return ApiResponseModel(message="data updated", data=[students[i]], status=True)
            else:
                return ApiResponseModel(message="record already exists", data=None, status=False)

    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.delete("/students/{rid}", response_model=ApiResponseModel[List[StudentData]])
def delete_student(rid:int):
    try:
        exists, i = check_if_roll_no_exists(rid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            deleted_student = students.pop(i)
            return ApiResponseModel(message="data deleted", data=[deleted_student], status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)





# Subject details





@app.post("/subjects", response_model=ApiResponseModel[List[SubjectData]])
def create_subject(subject_data: SubjectData):
    try:
        exists, i = check_if_subject_id_exists(subject_data.subject_id)
        if not exists:
            subjects.append(subject_data)
            return ApiResponseModel(message="created successfully", data=[subject_data], status=True)
        else:
            return ApiResponseModel(message="record already exists", data=None, status=False)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.get("/subjects", response_model=ApiResponseModel[List[SubjectData]])
def fetch_subject():
    try:
        if len(subjects) <= 0:
            return ApiResponseModel(message="data not found", data=[], status=False)
        else:
            return ApiResponseModel(message="data found", data=subjects, status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.get("/subjects/{sid}", response_model=ApiResponseModel[List[SubjectData]])
def fetch_subject_by_id(sid: int):
    try:
        exists, i = check_if_subject_id_exists(sid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            return ApiResponseModel(message="data found", data=[subjects[i]], status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.put("/subjects/{sid}", response_model=ApiResponseModel[List[SubjectData]])
def update_subject(sid:int, subject_data: SubjectData):
    try:
        exists, i = check_if_subject_id_exists(sid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            if sid == subject_data.subject_id:
                subjects[i] = subject_data
                return ApiResponseModel(message="data updated", data=[subjects[i]], status=True)
            else:
                return ApiResponseModel(message="record already exists", data=None, status=False)

    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@app.delete("/subjects/{sid}", response_model=ApiResponseModel[List[SubjectData]])
def delete_subject(sid:int):
    try:
        exists, i = check_if_subject_id_exists(sid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            deleted_subject = subjects.pop(i)
            return ApiResponseModel(message="data deleted", data=[deleted_subject], status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)






# Student Marks & Pass/Fail Check



class StudentMarks(BaseModel):
    student_roll: int
    subject_id: int
    marks_obtained: int

# List to store marks
student_marks: List[StudentMarks] = []

# Add marks for a student
@app.post("/marks", response_model=ApiResponseModel[List[StudentMarks]])
def add_student_marks(marks_data: StudentMarks):
    try:
        # Check if student and subject exist
        student_exists, _ = check_if_roll_no_exists(marks_data.student_roll)
        subject_exists, _ = check_if_subject_id_exists(marks_data.subject_id)

        if not student_exists:
            return ApiResponseModel(message="student not found", data=None, status=False)
        if not subject_exists:
            return ApiResponseModel(message="subject not found", data=None, status=False)

        # Add marks
        student_marks.append(marks_data)
        return ApiResponseModel(message="marks added successfully", data=[marks_data], status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


# Check if a student passed or failed a subject
@app.get("/result/{student_roll}/{subject_id}", response_model=ApiResponseModel[List[StudentMarks]])
def check_pass_status(student_roll: int, subject_id: int):
    try:
        # Find subject
        subject_exists, subj_index = check_if_subject_id_exists(subject_id)
        if not subject_exists:
            return ApiResponseModel(message="subject not found", data=None, status=False)
        min_marks = subjects[subj_index].min_passing_marks

        # Find marks entry
        for entry in student_marks:
            if entry.student_roll == student_roll and entry.subject_id == subject_id:
                passed = entry.marks_obtained >= min_marks
                return ApiResponseModel(message="student is pass",data=[entry],status=True)
            else:
                return ApiResponseModel(message="student is not pass", data=None, status=False)

        return ApiResponseModel(message="marks not found for given student and subject", data=None, status=False)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)
