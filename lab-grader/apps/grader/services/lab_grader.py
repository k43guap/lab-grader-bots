import math
from datetime import datetime

from apps.authorization.models import StudentFromSheet
from apps.grader.models import LaboratoryWork
from apps.grader.services.github_log_parser import GithubLogParser
from config import Settings


def calc_task_id(student_task_id: int, laboratory_work: LaboratoryWork) -> int:
    student_task_id += laboratory_work.taskid_shift
    student_task_id = student_task_id % laboratory_work.taskid_max
    if student_task_id == 0:
        student_task_id = laboratory_work.taskid_max
    return student_task_id


def get_status(
    student: StudentFromSheet,
    laboratory_work: LaboratoryWork,
    completion_date: datetime,
    lab_deadline: datetime,
    log_parser: GithubLogParser,
    settings: Settings,
) -> str:
    task_id = calc_task_id(student.variant_number, laboratory_work)
    task_id_from_log = log_parser.parse_task_id()

    if not laboratory_work.ignore_task_id and task_id != task_id_from_log:
        return settings.WRONG_TASK_ID_MARK

    grading_points = log_parser.parse_grading_points()
    points_part = ""
    if grading_points:
        points_part = f"@{grading_points}"

    reduction_coefficient = log_parser.parse_grade_reduction_coefficient()
    grader_reduction_part = ""
    if reduction_coefficient:
        grader_reduction_part = f"*{reduction_coefficient}"

    penalty_part = ""
    completion_date = completion_date.replace(tzinfo=None)
    lab_deadline = lab_deadline.replace(tzinfo=None)
    if completion_date > lab_deadline:
        overdue = completion_date - lab_deadline
        penalty = min(math.ceil((overdue.days + overdue.seconds / 86400) / 7), laboratory_work.penalty_max)
        if penalty > 0:
            penalty_part = f"-{penalty}"

    status = f"v{points_part}{grader_reduction_part}{penalty_part}"
    return status
