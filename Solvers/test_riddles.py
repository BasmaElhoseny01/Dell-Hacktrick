from Solvers.riddle_solvers import *

# test problem solving problem

def test_solve_problem_solving_easy():
    strings = ["pharaoh","sphinx","pharaoh","pharaoh","nile", "sphinx","pyramid","pharaoh","sphinx","sphinx"]
    top_x = 3
    output = solve_problem_solving_easy((strings,top_x))
    print(output)
    assert output == ["pharaoh","sphinx","nile"]
    strings = ["pharaoh","sphinx","pharaoh","pharaoh","pyramida", "sphinx","pyramid","pharaoh","sphinx","sphinx"]
    top_x = 3
    output = solve_problem_solving_easy((strings,top_x))
    print(output)
    assert output == ["pharaoh","sphinx","pyramid"]

def test_solve_problem_solving_medium():
    input = "3[d1[e2[l]]]"
    output = solve_problem_solving_medium(input)
    print(output)
    assert output == "delldelldell"
    input = "3[d1[e2[l]]]b"
    output = solve_problem_solving_medium(input)
    print(output)
    assert output == "delldelldellb"
    input = "3[d1[e2[l]]]4[2[ab]]"
    output = solve_problem_solving_medium(input)
    print(output)
    assert output == "delldelldellabababababababab"
    input ="1[]1[]"
    output = solve_problem_solving_medium(input)
    print(output)
    assert output == ""

def test_solve_problem_solving_hard():
    input = (3,2)
    output = solve_problem_solving_hard(input)
    print(output)
    assert output == 3
    input = (2,2)
    output = solve_problem_solving_hard(input)
    print(output)
    assert output == 2
    input = (1,1)
    output = solve_problem_solving_hard(input)
    print(output)
    assert output == 1

    input = (3,3)
    output = solve_problem_solving_hard(input)
    print(output)
    assert output == 6

if __name__ =='__main__':
    test_solve_problem_solving_easy()
    test_solve_problem_solving_medium()
    test_solve_problem_solving_hard()


