from typing import List

from fastapi import APIRouter


from src.packages.subjects.model import SubjectData
from src.packages.utilities.api_response_model import ApiResponseModel

subject_router = APIRouter()

subjects: List[SubjectData] = []


# helper
def check_if_subject_id_exists(subject_id: int):
    for i, subject in enumerate(subjects):
        if subject.subject_id == subject_id:
            return True,i
        else:
            continue
    return False, None



@subject_router.post("/", response_model=ApiResponseModel[List[SubjectData]])
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


@subject_router.get("/", response_model=ApiResponseModel[List[SubjectData]])
def fetch_subject():
    try:
        if len(subjects) <= 0:
            return ApiResponseModel(message="data not found", data=[], status=False)
        else:
            return ApiResponseModel(message="data found", data=subjects, status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@subject_router.get("/{sid}", response_model=ApiResponseModel[List[SubjectData]])
def fetch_subject_by_id(sid: int):
    try:
        exists, i = check_if_subject_id_exists(sid)
        if not exists:
            return ApiResponseModel(message="data not found", data=None, status=False)
        else:
            return ApiResponseModel(message="data found", data=[subjects[i]], status=True)
    except Exception as error:
        return ApiResponseModel(message=str(error), data=None, status=False)


@subject_router.put("/{sid}", response_model=ApiResponseModel[List[SubjectData]])
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


@subject_router.delete("/{sid}", response_model=ApiResponseModel[List[SubjectData]])
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
