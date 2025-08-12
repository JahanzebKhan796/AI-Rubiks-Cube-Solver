# Rubik's Cube Solver & Animator

This project captures all six faces of a real Rubik's Cube using your webcam, identifies the colors using **Google Gemini**, converts the cube state into **Kociemba notation**, solves it using the **Kociemba algorithm**, and animates the solution using **Pygame**.

---

## ✨ Features

- 📷 **Webcam Capture** — Step-by-step capture of each cube face.
- 🎨 **AI Color Recognition** — Uses Google Gemini Vision to identify sticker colors from images.
- 🔢 **Kociemba Notation Conversion** — Automatically maps colors to cube face labels.
- 🧠 **Rubik's Cube Solver** — Finds the shortest solution using the Kociemba algorithm.
- 🎥 **Pygame Animation** — Visualizes the solving process with move descriptions and a "Next" button.

---

## 📂 Project Structure

```
rubiks_solver/
│
├── main.py              # Main script (capture, solve, animate)
├── requirements.txt     # Python dependencies
├── .env                 # Stores Google API key
└── README.md            # Documentation
```

---

## ⚙️ Installation

1. **Clone this repository**

```bash
git clone https://github.com/JahanzebKhan796/AI-Rubiks-Cube-Solver.git
cd rubiks_solver
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup

1. **Get a Google Gemini API Key**

   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create and copy your API key.

2. **Create a `.env` file** in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Usage

Run the program:

```bash
python Rubik.py
```

### Step-by-step flow:

1. **Face Capture**

   - The script will prompt you for each cube face in this order:  
     `Front → Right → Back → Left → Bottom → Top`
   - Press **SPACE** to capture.

2. **AI Color Detection**

   - Gemini identifies colors and returns them in JSON format.

3. **Cube Solving**

   - The script converts colors to Kociemba notation.
   - The **kociemba** library computes the solution.

4. **Solution Animation**
   - The cube is displayed in a 2D unfolded layout.
   - Click **"Next"** to perform each move.
   - Move descriptions appear below the cube.

---

## 📦 Dependencies

Listed in `requirements.txt`:

```
python-dotenv
google-generativeai
pydantic
opencv-python
kociemba
pygame
pycuber
```

## 📝 Notes

- Make sure your webcam is functional before running the program.
- Proper lighting helps AI detect colors accurately.
- This script assumes a **standard color scheme** for center stickers.
- The solving sequence may vary in length depending on cube state.

---

## 📜 License

MIT License. Feel free to modify and use this code.
