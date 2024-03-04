def solve_cv_easy(riddle):
    return ""
def solve_cv_medium(riddle):
    return ""
def solve_cv_hard(riddle):
    return ""
def solve_ml_easy(riddle):
    return ""
def solve_ml_medium(riddle):
    return ""
def solve_sec_medium(riddle):
    return ""
def solve_sec_hard(riddle):
    return ""
def solve_problem_solving_easy(riddle):
    return ""
def solve_problem_solving_medium(riddle):
    return ""
def solve_problem_solving_hard(riddle):
    return ""

riddle_solvers = {
    'cv_easy': solve_cv_easy,
    'cv_medium': solve_cv_medium,
    'cv_hard': solve_cv_hard,
    'ml_easy': solve_ml_easy,
    'ml_medium': solve_ml_medium,
    'sec_medium_stegano': solve_sec_medium,
    'sec_hard':solve_sec_hard,
    'problem_solving_easy': solve_problem_solving_easy,
    'problem_solving_medium': solve_problem_solving_medium,
    'problem_solving_hard': solve_problem_solving_hard
}
reddle_points = {
    "cv_easy": 1,
    "cv_medium": 2,
    'cv_hard': 3,
    'ml_easy': 1,
    'ml_medium': 2,
    'sec_medium_stegano': 2,
    'sec_hard':3,
    'problem_solving_easy': 1,
    'problem_solving_medium': 2,
    'problem_solving_hard': 3
}
team_id="1322"
for riddle_id in riddle_solvers.keys():
    payload = {
        "team_id": team_id,
        "riddle_id": str(riddle_id),
    }
    print(payload)