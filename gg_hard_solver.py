import json
import pyautogui
import tkinter
from PIL import Image, ImageDraw, ImageGrab, ImageTk
import cv2
import numpy
import keyboard
import os

dirname = os.path.dirname(__file__)

config = json.load(open("config.json"))

screen_width = config["screen_bbox"][2] - config["screen_bbox"][0]
screen_height = config["screen_bbox"][3] - config["screen_bbox"][1]

top_left_point = (23/70 * screen_width + config["screen_bbox"][0], 7/30 * screen_height + config["screen_bbox"][1])
top_left_point_diagonal = (13/35 * screen_width + config["screen_bbox"][0], 61/300 * screen_height + config["screen_bbox"][1])
top_left_point_vertical = (23/70 * screen_width + config["screen_bbox"][0], 29/100 * screen_height + config["screen_bbox"][1])
top_right_point = (47/70 * screen_width + config["screen_bbox"][0], 7/30 * screen_height + config["screen_bbox"][1])

pixel_width = (top_right_point[0] - top_left_point[0]) / 4
pixel_height = (top_left_point_vertical[1] - top_left_point[1]) + 2 * (top_left_point[1] - top_left_point_diagonal[1])
x_offset = top_left_point[0] - top_left_point_diagonal[0]
y_offset = top_left_point[1] - top_left_point_diagonal[1]

top_left_pixel = (top_left_point[0] + pixel_width/2, top_left_point_diagonal[1] + pixel_height/2)

board_bounds = [
    [None] * 4,
    [None] * 5,
    [None] * 6,
    [None] * 7,
    [None] * 6,
    [None] * 5,
    [None] * 4
]

for i, row in enumerate(board_bounds):
    for j, pixel in enumerate(board_bounds[i]):
        modified_x_offset = (-abs(i-3)+3) * x_offset + j * pixel_width
        modified_y_offset = i*y_offset + i*(pixel_height/2)
        center_x = top_left_pixel[0] + modified_x_offset
        center_y = top_left_pixel[1] + modified_y_offset
        board_bounds[i][j] = (int(center_x - pixel_width/2), int(center_y - pixel_height/2), int(center_x + pixel_width/2), int(center_y + pixel_height/2))

board_bbox = (board_bounds[3][0][0], board_bounds[0][0][1], board_bounds[3][6][2], board_bounds[6][0][3])

board_strings = None
click_list = None

def print_formatted_board():
    for i, row in enumerate(board_strings):
        print(" " * abs(i-3), end="")
        for cell in row:
            print(f"{cell} ", end="")
        print()

def print_click_list():
    for i, row in enumerate(click_list):
        print(" " * abs(i-3), end="")
        for bool in row:
            print(f"{str(bool)[:1]} ", end="")
        print()

def toggle_string(i, j):
    if i < 0 or j < 0:
        raise IndexError("list index out of range (negative index)")

    global board_strings
    board_strings[i][j] = "X" if board_strings[i][j] == "O" else "O"

def simulate_click(i, j):
    try:
        global click_list
        click_list[i][j] = not click_list[i][j]
    except IndexError:
        return
    
    toggle_string(i, j)

    if i < 3:
        try:
            toggle_string(i, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j)
        except IndexError:
            pass
        try:
            toggle_string(i, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j)
        except IndexError:
            pass
    elif i == 3:
        try:
            toggle_string(i, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j)
        except IndexError:
            pass
    elif i > 3:
        try:
            toggle_string(i, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j+1)
        except IndexError:
            pass

def propagate_4():
    propagation_coords = (
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)
    )
    for coords in propagation_coords:
        simulate_click(coords[0], coords[1])

def propagate_5():
    propagation_coords = (
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 4), (2, 5), (3, 1), (3, 3), (3, 4), (3, 5), (4, 0), (4, 2)
    )
    for coords in propagation_coords:
        simulate_click(coords[0], coords[1])

def propagate_6():
    propagation_coords = (
        (0, 0), (0, 3), (1, 1), (1, 3), (3, 2), (3, 4), (4, 1), (4, 4), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)
    )
    for coords in propagation_coords:
        simulate_click(coords[0], coords[1])

def solve_board():
    global board_strings, click_list
    board_strings = [
        [None] * 4,
        [None] * 5,
        [None] * 6,
        [None] * 7,
        [None] * 6,
        [None] * 5,
        [None] * 4
    ]

    # board_strings = [
    #     ["X"] * 4,
    #     ["X"] * 5,
    #     ["X"] * 6,
    #     ["O"] * 7,
    #     ["X"] * 6,
    #     ["O"] * 5,
    #     ["X"] * 4
    # ]

    click_list = [
        [False] * 4,
        [False] * 5,
        [False] * 6,
        [False] * 7,
        [False] * 6,
        [False] * 5,
        [False] * 4
    ]

    for i, row in enumerate(board_bounds):
        for j, pixel in enumerate(board_bounds[i]):
            if pyautogui.locate(os.path.join(dirname, "glimmer.png"), ImageGrab.grab(board_bounds[i][j]), confidence=0.9):
                board_strings[i][j] = "X"
            elif pyautogui.locate(os.path.join(dirname, "gloom.png"), ImageGrab.grab(board_bounds[i][j]), confidence=0.9):
                board_strings[i][j] = "O"
            else:
                print(f"Failed to find pixel ({i}, {i})")

    print_formatted_board()

    for i, row in enumerate(board_strings):
        if i < 3:
            for j, pixel in enumerate(row):
                if pixel == "X":
                    simulate_click(i+1, j+1)
        if i == 3:
            if row.count("X") % 2 == 1:
                propagate_4()
            for j, pixel in enumerate(row):
                if pixel == "X":
                    simulate_click(i+1, j)
        elif i == 4:
            if row.count("X") % 2 == 1:
                propagate_5()
            for j, pixel in enumerate(row):
                if pixel == "X":
                    simulate_click(i+1, j)
        elif i == 5:
            if row.count("X") % 2 == 1:
                propagate_6()
            for j, pixel in enumerate(row):
                if pixel == "X":
                    simulate_click(i+1, j)

    print("--------------")
    print_click_list()
    
    board_image = ImageGrab.grab(bbox=board_bbox)

    board_image = cv2.cvtColor(numpy.array(board_image), cv2.COLOR_RGB2BGR)

    for i, row in enumerate(click_list):
        for j, pixel in enumerate(row):
            if pixel:
                point1 = (board_bounds[i][j][0] - board_bbox[0] + int(pixel_width/3.6), board_bounds[i][j][1] - board_bbox[1] + int(y_offset))
                point2 = (board_bounds[i][j][2] - board_bbox[0] - int(pixel_width/3.6), board_bounds[i][j][3] - board_bbox[1] - int(y_offset))
                board_image = cv2.rectangle(board_image, point1, point2, (0, 0, 255), 4)

    board_image = Image.fromarray(cv2.cvtColor(board_image, cv2.COLOR_BGR2RGB))

    board_image = board_image.resize((int(board_image.size[0]/1.5), int(board_image.size[1]/1.5)))
    board_image = ImageTk.PhotoImage(board_image)
    image_label.config(image=board_image)
    image_label.image = board_image

gui = tkinter.Tk()
gui.geometry(f"{int((board_bbox[2]-board_bbox[0])/1.5) + 20}x{int((board_bbox[3]-board_bbox[1])/1.5) + 40}")
gui.title("G&G Hard Solver by TheFatRabbit")
gui.attributes("-topmost", True)

image_label = tkinter.Label(gui, image=None)
image_label.pack()

solve_button = tkinter.Button(gui, text="Solve Board", command=solve_board)
solve_button.pack()

keyboard.add_hotkey(config["hotkey"], solve_board)

gui.mainloop()