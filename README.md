# Pathfinder

This project demonstrates **BFS**, **Dijkstra**, and **A\*** algorithms on a small map, visualized in a web-based interface.

## Features

- **Flask Backend**:
  - Loads a JSON-based graph (nodes with coordinates, weighted edges).
  - Implements BFS, Dijkstra, and A\* to compute shortest paths.
  - Provides REST endpoints to fetch graph data and compute paths.
- **Web Frontend** (HTML/CSS/JS):
  - Renders nodes/edges on a canvas.
  - Allows selecting start/goal nodes and an algorithm.
  - Highlights the resulting path.

## Project Structure

```bash
pathfinder/
├── README.md
├── backend/
│   ├── app.py
│   ├── graph.py
│   ├── algorithms.py
│   └── data/
│       └── sample_map.json
├── frontend/
│   ├── index.html
│   ├── main.js
│   └── style.css
└── tests/
    ├── test_graph.py
    └── test_algorithms.py
```

## How to Run

1. **Install Dependencies**

```bash
   cd backend
   pip install -r requirements.txt
```

2. **Start the Flask Server**

```bash
python app.py
```

By default, it listens on http://127.0.0.1:5000.

3. **Open the Frontend**

- In another terminal, serve the frontend/ folder with a simple local server. For example:

```bash
cd frontend
python -m http.server 8080
```

- Open http://localhost:8080/index.html in your browser.

## Run Tests

```bash
cd tests
python -m unittest discover
```
