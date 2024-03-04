import cv2
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

def test_solve_sec_hard():
    input = ("266200199BBCDFF1","0123456789ABCDEF")
    output = solve_sec_hard(input)
    print("output: ",output)
    assert output == "4E0E6864B5E1CA52"

def solve_puzzle(pieces):
    #apply best fit algorithm to solve the puzzle
    puzzle_order = [0]  # Start with the leftmost piece at position 0
    current_piece_index = 0

    while len(pieces) > 1:
        min_diff = float('inf')
        next_piece_index = None
        print("current_piece_index: ",current_piece_index)
        print("len(pieces): ",len(pieces))
        current_piece = pieces[current_piece_index]
        for i, piece in enumerate(pieces):
            if i != current_piece_index:
                diff = np.sum(np.abs(current_piece[:, -1] - piece[:, 0]))  # Measure the difference
                if diff < min_diff:
                    min_diff = diff
                    next_piece_index = i

        puzzle_order.append(next_piece_index)
        current_piece_index = next_piece_index
        pieces.pop(current_piece_index)
        if current_piece_index == len(pieces) - 1:
            current_piece_index -= 1

    # Add the last remaining piece
    puzzle_order.append(pieces.index(current_piece))

    return puzzle_order

if __name__ =='__main__':
    # test_solve_problem_solving_easy()
    # test_solve_problem_solving_medium()
    # test_solve_problem_solving_hard()
    # test_solve_sec_hard()
    # read image
    image = cv2.imread('Riddles\cv_easy_example\shredded.jpg')
    # split image into pieces each peice has width 64 and the image height until the end
    pieces = [image[:, i:i + 64] for i in range(0, image.shape[1], 64)]
    print(pieces[0])
    oreder=solve_puzzle(pieces)
    # concatenate the pieces in the order of the puzzle
    puzzle = np.concatenate([pieces[i] for i in oreder], axis=1)
    # show the puzzle

    cv2.imshow('puzzle', puzzle)
    cv2.waitKey(0)


