const canvas = document.getElementById("graph-canvas");
const ctx = canvas.getContext("2d");
let nodes = []; // [{id, x, y}, ...]
let edges = []; // [{source, target, weight}, ...]

const startSelect = document.getElementById("start-select");
const goalSelect = document.getElementById("goal-select");
const algoSelect = document.getElementById("algo-select");
const computeBtn = document.getElementById("compute-btn");
const resultDiv = document.getElementById("result");

// Fetch graph data from backend
async function loadGraphData() {
  const nodesRes = await fetch("http://127.0.0.1:5000/nodes");
  nodes = await nodesRes.json();
  const edgesRes = await fetch("http://127.0.0.1:5000/edges");
  edges = await edgesRes.json();

  // Populate dropdowns
  nodes.forEach((n) => {
    const opt1 = document.createElement("option");
    opt1.value = n.id;
    opt1.textContent = `Node ${n.id}`;
    startSelect.appendChild(opt1);

    const opt2 = document.createElement("option");
    opt2.value = n.id;
    opt2.textContent = `Node ${n.id}`;
    goalSelect.appendChild(opt2);
  });

  // Set defaults
  startSelect.value = nodes[0]?.id || "";
  goalSelect.value = nodes[nodes.length - 1]?.id || "";

  drawGraph();
}

function drawArrow(ctx, x1, y1, x2, y2, arrowSize = 10, color = "#888") {
  // Draw the main line
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();

  // Calculate the angle of the line
  const angle = Math.atan2(y2 - y1, x2 - x1);

  // Draw arrowhead at the (x2, y2) end
  ctx.beginPath();
  // The tip is at (x2, y2), so we draw two lines angled back from that point
  ctx.moveTo(x2, y2);
  ctx.lineTo(
    x2 - arrowSize * Math.cos(angle - Math.PI / 6),
    y2 - arrowSize * Math.sin(angle - Math.PI / 6)
  );
  ctx.moveTo(x2, y2);
  ctx.lineTo(
    x2 - arrowSize * Math.cos(angle + Math.PI / 6),
    y2 - arrowSize * Math.sin(angle + Math.PI / 6)
  );
  ctx.stroke();
}

// Draw the graph on canvas
function drawGraph(path = []) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw edges
  ctx.strokeStyle = "#888";
  edges.forEach((edge) => {
    const src = nodes.find((n) => n.id === edge.source);
    const tgt = nodes.find((n) => n.id === edge.target);
    if (!src || !tgt) return;

    drawArrow(ctx, src.x, src.y, tgt.x, tgt.y, 20, "##ff0000");

    // Label the edge with its weight
    const midX = (src.x + tgt.x) / 2;
    const midY = (src.y + tgt.y) / 2;
    ctx.fillStyle = "#fff";
    ctx.font = "14px sans-serif";
    ctx.fillText(edge.weight, midX, midY - 5);
  });

  // If there's a path, highlight the edges in path
  if (path.length > 1) {
    ctx.strokeStyle = "yellow";
    for (let i = 0; i < path.length - 1; i++) {
      const srcId = path[i];
      const tgtId = path[i + 1];
      const src = nodes.find((n) => n.id === srcId);
      const tgt = nodes.find((n) => n.id === tgtId);
      if (src && tgt) {
        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.lineTo(tgt.x, tgt.y);
        ctx.stroke();
      }
    }
  }

  // Draw nodes
  nodes.forEach((node) => {
    ctx.beginPath();
    ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
    ctx.fillStyle = "#00b7ff";
    ctx.fill();
    ctx.strokeStyle = "#000";
    ctx.stroke();

    // If node is in path, color it differently
    if (path.includes(node.id)) {
      ctx.fillStyle = "yellow";
      ctx.beginPath();
      ctx.arc(node.x, node.y, 6, 0, 2 * Math.PI, false);
      ctx.fill();
    }

    // Draw node ID
    ctx.fillStyle = "#00b7ff";
    ctx.font = "14px sans-serif";
    ctx.fillText(node.id, node.x - 3, node.y - 15);
  });
}

// Compute path
async function computePath() {
  const start = parseInt(startSelect.value, 10);
  const goal = parseInt(goalSelect.value, 10);
  const algo = algoSelect.value;

  const res = await fetch("http://127.0.0.1:5000/path", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start, goal, algo }),
  });
  const data = await res.json();

  if (data.error) {
    resultDiv.textContent = `Error: ${data.error}`;
    drawGraph(); // no path highlight
  } else {
    const path = data.path;
    resultDiv.textContent = `Path found: ${path.join(" -> ")}`;
    drawGraph(path);
  }
}

// Initialize
loadGraphData();
computeBtn.addEventListener("click", computePath);
