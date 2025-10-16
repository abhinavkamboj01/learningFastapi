
from pydantic import BaseModel
    # This line defines a type variable named T. It’s a placeholder type you can use inside generic classes.

class SubjectData(BaseModel):
    subject_name: str
    subject_id: int
    subject_status: bool
    subject_description: str
    min_passing_marks: int