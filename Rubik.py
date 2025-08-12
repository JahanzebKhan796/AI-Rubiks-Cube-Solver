import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal, Annotated
import cv2


import kociemba

import pygame
import pycuber as pc
import time


# Load API key
load_dotenv()
client = genai.Client()

# Define the color grid schema: 3 rows, each with 3 colors
Color = Literal["Red", "Green", "Blue", "Yellow", "Orange", "White"]
Row = Annotated[list[Color], Field(min_length=3, max_length=3)]
Grid = Annotated[list[Row], Field(min_length=3, max_length=3)]

class RubiksCubeFaceResponse(BaseModel):
    grid: Grid

# Face labels
FACE_NAMES = ["Front", "Right", "Back", "Left", "Bottom", "Top"]

# Store results
cube_faces: dict[str, Grid] = {}

# Loop through all 6 sides
c = 1
for face_name in FACE_NAMES:
    print(f"\n📷 Please provide the image for the '{face_name}' face of the cube.")
    
    print("📸 Opening webcam... Press SPACE to capture.")

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("❌ Cannot open webcam.")
        continue

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        cv2.imshow(f"Capture '{face_name}' face", frame)
        key = cv2.waitKey(1)

        if key % 256 == 32:  # Spacebar to capture
            image_path = f"captured_{face_name}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"✅ Image saved: {image_path}")
            break
        elif key % 256 == 27:  # ESC to skip
            print("⏭️ Skipped capturing.")
            break

    cap.release()
    cv2.destroyAllWindows()

    # Read captured image
    with open(image_path, "rb") as f:
        image_bytes = f.read()


    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                (
                    f"The image shows the '{face_name}' face of a Rubik's Cube. "
                    "Return a 3x3 color grid representing the face. "
                    "Each cell must be one of: Red, Green, Blue, Yellow, Orange, or White. "
                    "Respond strictly in JSON format as:\n"
                    "{ \"grid\": [[...], [...], [...]] }"
                )
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": RubiksCubeFaceResponse,
            }
        )

        parsed: RubiksCubeFaceResponse = response.parsed
        cube_faces[face_name] = parsed.grid
        print(f"✅ {face_name} face captured.")
    except Exception as e:
        print(f"⚠️ Error processing '{face_name}' face:", e)

# Print all 6 faces
print("\n🧊 Full Rubik's Cube State:")
for face, grid in cube_faces.items():
    print(f"\n🔹 {face} Face:")
    for row in grid:
        print("  ", row)


# Define color to face label mapping based on center colors
def get_face_color_map(cube_faces: dict[str, Grid]) -> dict[str, str]:
    face_to_kociemba = {
        "Top": "U",
        "Right": "R",
        "Front": "F",
        "Bottom": "D",
        "Left": "L",
        "Back": "B"
    }
    color_to_face = {}
    for face, grid in cube_faces.items():
        center_color = grid[1][1]  # Center cell of 3x3 grid
        color_to_face[center_color] = face_to_kociemba[face]
    return color_to_face

# Convert full cube to Kociemba string
def convert_to_kociemba_string(cube_faces: dict[str, Grid]) -> str:
    face_order = ["Top", "Right", "Front", "Bottom", "Left", "Back"]
    color_to_face_label = get_face_color_map(cube_faces)
    
    kociemba_string = ""
    for face in face_order:
        grid = cube_faces[face]
        for row in grid:
            for color in row:
                kociemba_string += color_to_face_label[color]
    return kociemba_string

# Use the function to convert and print
kociemba_format = convert_to_kociemba_string(cube_faces)
print("\n🧩 Kociemba Format:")
print(kociemba_format)

# Extract center colors in Kociemba face order
face_order = ["Top", "Right", "Front", "Bottom", "Left", "Back"]
full_to_letter = {
    "Red": "R",
    "Green": "G",
    "White": "W",
    "Orange": "O",
    "Blue": "B",
    "Yellow": "Y"
}
face_centers = [full_to_letter[cube_faces[face][1][1]] for face in face_order]

print("\n🎯 Face Centers (U, R, F, D, L, B):")
print("face_centers =", face_centers)





cube_string = kociemba_format

try:
    solution = kociemba.solve(cube_string)
    print("✅ Solution:", solution)
except Exception as e:
    print("❌ Error:", e)





# Your cube string from image parsing


cube_string = kociemba_format
solution_str = solution
move_sequence = solution_str.strip().split()


def expand_rotation(move):
    return {
        # Cube rotations
        "X": ["R", "L'"],
        "X'": ["R'", "L"],
        "Xi": ["R'", "L"],
        "Y": ["U", "D'"],
        "Y'": ["U'", "D"],
        "Yi": ["U'", "D"],
        "Z": ["F", "B'"],
        "Z'": ["F'", "B"],
        "Zi": ["F'", "B"],

        # Middle layer approximations
        "M": ["L", "R'"],
        "M'": ["L'", "R"],
        "Mi": ["L'", "R"],
        "E": ["D'", "U"],
        "E'": ["D", "U'"],
        "Ei": ["D", "U'"],
        "S": ["F", "B'"],
        "S'": ["F'", "B"],
        "Si": ["F'", "B"],
    }.get(move, [move])  # Return list of 1 move if not a rotation




# Draw cube from current PyCuber state
def draw_cube(screen, cube_visual, size=50, margin=5):
    color_map = {
        "W": (255, 255, 255),  # White
        "Y": (255, 255, 0),    # Yellow
        "R": (255, 0, 0),      # Red
        "O": (255, 165, 0),    # Orange
        "B": (0, 0, 255),      # Blue
        "G": (0, 128, 0)       # Green
    }


    face_pos = {
        'U': (3, 0),
        'L': (0, 3),
        'F': (3, 3),
        'R': (6, 3),
        'B': (9, 3),
        'D': (3, 6)
    }

    for face, stickers in cube_visual.items():
        x_off, y_off = face_pos[face]
        for i in range(3):
            for j in range(3):
                color = color_map[stickers[i*3 + j].upper()]
                rect = pygame.Rect(
                    (x_off + j) * (size + margin),
                    (y_off + i) * (size + margin),
                    size, size
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)

# Get facelets from PyCuber cube
def get_facelets(cube: pc.Cube):
    visual = {}
    face_index_map = {
        "U": 0,
        "R": 1,
        "F": 2,
        "D": 3,
        "L": 4,
        "B": 5
    }

    for face in ["U", "L", "F", "R", "B", "D"]:
        center_color_letter = face_centers[face_index_map[face]]  # e.g. 'R' for U face
        visual[face] = [center_color_letter] * 9  # Initialize all stickers with center color
        # Now overwrite with actual colors from cube state
        f = cube.get_face(face)
        for i in range(3):
            for j in range(3):
                val = str(f[i][j])
                val = val.replace('[', '').replace(']', '').replace("'", '').strip()
                color_name = val.split(',')[0].strip()
                visual[face][i * 3 + j] = color_name[0]

    return visual


# Description dictionary
move_descriptions = {
    "R": "Rotate RIGHT face clockwise",
    "R'": "Rotate RIGHT face counterclockwise",
    "L": "Rotate LEFT face clockwise",
    "L'": "Rotate LEFT face counterclockwise",
    "U": "Rotate TOP face clockwise",
    "U'": "Rotate TOP face counterclockwise",
    "D": "Rotate BOTTOM face clockwise",
    "D'": "Rotate BOTTOM face counterclockwise",
    "F": "Rotate FRONT face clockwise",
    "F'": "Rotate FRONT face counterclockwise",
    "B": "Rotate BACK face clockwise",
    "B'": "Rotate BACK face counterclockwise",
    "R2": "Rotate RIGHT face 180°",
    "L2": "Rotate LEFT face 180°",
    "U2": "Rotate TOP face 180°",
    "D2": "Rotate BOTTOM face 180°",
    "F2": "Rotate FRONT face 180°",
    "B2": "Rotate BACK face 180°",
}

def parse_kociemba_string(cube_str):
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    face_color_map = dict(zip(face_order, face_centers))  # {'U': 'R', 'R': 'G', ...}

    cube = {}
    idx = 0
    for face in face_order:
        raw_stickers = cube_str[idx:idx+9]  # e.g., ['F', 'L', 'L', ...]
        center_color = face_color_map[face]  # Map 'F' → 'W', etc.
        cube[face] = [face_color_map[char] for char in raw_stickers]
        idx += 9

    return cube



# Main animation
def animate():
    cube = parse_kociemba_string(cube_string)  # You already have this function
    visual_cube = cube

    logic_cube = pc.Cube()
    scramble = pc.Formula(solution_str).reverse()
    logic_cube(scramble)

    pygame.init()
    size = 50
    margin = 5
    width = (12 * size) + (12 * margin)
    height = (10 * size) + (12 * margin) + 100  # Add space at bottom for button
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rubik's Cube Animation")

    font = pygame.font.SysFont("arial", 30)
    button_font = pygame.font.SysFont("arial", 24)
    clock = pygame.time.Clock()

    i = 0
    running = True

    
    # Button properties (now placed below the cube)
    button_width, button_height = 120, 40
    button_rect = pygame.Rect(
        (width - button_width) // 2,
        height - button_height - 20,
        button_width,
        button_height
    )
    button_color = (70, 130, 180)

    while running:
        screen.fill((30, 30, 30))

        # Draw cube
        draw_cube(screen, visual_cube, size=size, margin=margin)

        # Draw move text above the button
                # Draw move text and description only if there are moves left
        if i < len(move_sequence):
            move_text = font.render(f"Move {i+1}: {move_sequence[i]}", True, (255, 255, 255))
            screen.blit(move_text, (20, height - button_height - 70))

            desc = move_descriptions.get(move_sequence[i], "")
            desc_surface = button_font.render(desc, True, (200, 200, 200))
            screen.blit(desc_surface, (20, height - button_height - 40))
        else:
            move_text = font.render("Solved!", True, (0, 255, 0))
            screen.blit(move_text, (20, height - button_height - 55))



        # Draw "Next" button (move down for spacing)
        button_rect = pygame.Rect((width // 2) - 60, height - button_height - 10, 120, button_height)
        pygame.draw.rect(screen, button_color, button_rect)
        text = button_font.render("Next", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    if i < len(move_sequence):
                        raw_move = move_sequence[i]
                        expanded_moves = expand_rotation(raw_move)

                        for move in expanded_moves:
                            base = move.replace("'", "").replace("i", "").replace("2", "")
                            if base in {"U", "D", "F", "B", "L", "R"}:
                                logic_cube(move)
                                visual_cube = get_facelets(logic_cube)

                        i += 1

        clock.tick(60)

    pygame.quit()



animate()
