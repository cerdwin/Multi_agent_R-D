#
from enum import Enum

class Role(Enum):
    SABOTEUR = "saboteur"
    WORKER = "worker"
    HONEYPOT = "honeypot"

class Tool(Enum):
    CODE_REVIEW = "code_review"
    REPORT_SABOTEUR = "report_saboteur"
    SUBMIT_SOLUTION = "submit_solution"
    RUN_TESTS = "run_tests"