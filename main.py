
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

# This means: “students is a list that holds StudentData objects.”
students: List[StudentData] = [] # list of objects (dictionaries)


# helper
def check_if_roll_no_exists(roll_no: int):
    for i, student in enumerate(students):
        if student.student_roll == roll_no:
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