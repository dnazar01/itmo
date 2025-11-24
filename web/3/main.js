let grid = [
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [0, 0, 0, 0]
];

let totalScore = 0;
let gameOver = false;
let stepsHistory = [];
let bestList = [];
let mergedCells = [];

const KEY_STATE = 'state';
const KEY_RECORDS = 'records';

function makeElement(tag, { className, attrs, text } = {}, children = []) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      node.setAttribute(k, v);
    }
  }
  for (const child of children) {
    node.appendChild(child);
  }
  return node;
}

function cloneGrid(source) {
  return source.map(function (row) {
    return row.slice();
  });
}

function recalcScore() {
  let sum = 0;
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 4; j++) {
      sum += grid[i][j];
    }
  }
  totalScore = sum;
}

const header = makeElement('header');
document.body.prepend(header);

const container = makeElement('div', { className: 'container' });
header.appendChild(container);

const title = makeElement('h1', { text: '2048' });
container.appendChild(title);

const main = makeElement('main');
header.insertAdjacentElement('afterend', main);

const section = makeElement('section', { className: 'main' });
main.appendChild(section);

const wrap = makeElement('div', { className: 'container' });
section.appendChild(wrap);

const scoreText = makeElement('h2', { className: 'score', text: 'Счёт: 0' });
wrap.appendChild(scoreText);

const btnRestart = makeElement('button', { className: 'btn', text: 'Новая игра' });
const btnUndo = makeElement('button', { className: 'btn', text: 'Отмена' });

wrap.appendChild(btnRestart);
wrap.appendChild(btnUndo);

const board = makeElement('div', { className: 'board' });
wrap.appendChild(board);

const btnsBox = makeElement('div', { className: 'controls' });
const btnUp = makeElement('button', { className: 'ctrl', text: '↑' });
const btnLeft = makeElement('button', { className: 'ctrl', text: '←' });
const btnRight = makeElement('button', { className: 'ctrl', text: '→' });
const btnDown = makeElement('button', { className: 'ctrl', text: '↓' });

btnsBox.appendChild(btnUp);
btnsBox.appendChild(btnLeft);
btnsBox.appendChild(btnRight);
btnsBox.appendChild(btnDown);
wrap.appendChild(btnsBox);

const recordsTitle = makeElement('h3', { text: 'Топ-10 рекордов' });
wrap.appendChild(recordsTitle);

const recordsTable = makeElement('table', { className: 'records' });
const thead = makeElement('thead');
const headRow = makeElement('tr');
headRow.appendChild(makeElement('th', { text: '№' }));
headRow.appendChild(makeElement('th', { text: 'Счёт' }));
thead.appendChild(headRow);
recordsTable.appendChild(thead);

const recordsBody = makeElement('tbody', { className: 'records__body' });
recordsTable.appendChild(recordsBody);
wrap.appendChild(recordsTable);

const message = makeElement('div', { className: 'message' });
wrap.appendChild(message);

function loadRecords() {
  const raw = localStorage.getItem(KEY_RECORDS);
  if (!raw) {
    bestList = [];
    return;
  }
  try {
    const arr = JSON.parse(raw);
    if (Array.isArray(arr)) {
      bestList = arr;
    } else {
      bestList = [];
    }
  } catch (e) {
    bestList = [];
  }
}

function saveRecords() {
  localStorage.setItem(KEY_RECORDS, JSON.stringify(bestList));
}

function updateRecords(newScore) {
  bestList.push(newScore);
  bestList.sort(function (a, b) { return b - a; });
  if (bestList.length > 10) {
    bestList = bestList.slice(0, 10);
  }
  saveRecords();
}

function renderRecords() {
  while (recordsBody.firstChild) recordsBody.removeChild(recordsBody.firstChild);

  for (let i = 0; i < bestList.length; i++) {
    const tr = makeElement('tr');
    tr.appendChild(makeElement('td', { text: String(i + 1) }));
    tr.appendChild(makeElement('td', { text: String(bestList[i]) }));
    recordsBody.appendChild(tr);
  }
}

function saveState() {
  const state = {
    grid: grid,
    score: totalScore,
    gameOver: gameOver
  };
  localStorage.setItem(KEY_STATE, JSON.stringify(state));
}

function loadState() {
  const raw = localStorage.getItem(KEY_STATE);
  if (!raw) return false;

  try {
    const state = JSON.parse(raw);
    if (!state || !Array.isArray(state.grid)) return false;

    grid = state.grid;
    if (typeof state.score === 'number') {
      totalScore = state.score;
    }
    if (typeof state.gameOver === 'boolean') {
      gameOver = state.gameOver;
    }
    if (gameOver) {
      showGameOver();
    }
    return true;
  } catch (e) {
    return false;
  }
}

function addRandomTiles(field) {
  let count = Math.random() < 0.9 ? 1 : 2;
  const empty = [];

  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (field[r][c] === 0) {
        empty.push({ r: r, c: c });
      }
    }
  }

  if (empty.length === 0) return;

  for (let i = empty.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = empty[i];
    empty[i] = empty[j];
    empty[j] = tmp;
  }

  for (let k = 0; k < count && k < empty.length; k++) {
    const cell = empty[k];
    field[cell.r][cell.c] = Math.random() < 0.9 ? 2 : 4;
  }
}

function hasMoves() {
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (grid[r][c] === 0) return true;
    }
  }

  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 3; c++) {
      if (grid[r][c] === grid[r][c + 1]) return true;
    }
  }

  for (let c = 0; c < 4; c++) {
    for (let r = 0; r < 3; r++) {
      if (grid[r][c] === grid[r + 1][c]) return true;
    }
  }

  return false;
}

function showGameOver() {
  message.textContent = 'Нет возможных ходов. Игра окончена.';
  message.classList.add('message--visible');
}

function hideGameOver() {
  message.textContent = '';
  message.classList.remove('message--visible');
}

function resetGame() {
  grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ];
  totalScore = 0;
  gameOver = false;
  stepsHistory = [];
  mergedCells = [];
  hideGameOver();

  addRandomTiles(grid);
  recalcScore();
  draw();
  saveState();
}

function isMergedCell(r, c) {
  return mergedCells.some(function (cell) {
    return cell.r === r && cell.c === c;
  });
}

function draw() {
  while (board.firstChild) board.removeChild(board.firstChild);

  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const value = grid[r][c];
      let cls = 'tile tile-' + value;
      if (value !== 0 && isMergedCell(r, c)) {
        cls += ' tile-merged';
      }

      const tile = makeElement('div', {
        className: cls,
        text: value === 0 ? '' : value
      });

      tile.style.gridRowStart = r + 1;
      tile.style.gridColumnStart = c + 1;

      board.appendChild(tile);
    }
  }

  scoreText.textContent = 'Счёт: ' + totalScore;
}

function moveRight() {
  let moved = false;

  for (let r = 0; r < 4; r++) {
    let line = grid[r].filter(function (x) { return x !== 0; });

    for (let j = line.length - 1; j > 0; j--) {
      if (line[j] === line[j - 1]) {
        line[j] *= 2;
        line[j - 1] = 0;
      }
    }

    line = line.filter(function (x) { return x !== 0; });
    while (line.length < 4) {
      line.unshift(0);
    }

    for (let c = 0; c < 4; c++) {
      if (grid[r][c] !== line[c]) {
        grid[r][c] = line[c];
        moved = true;
      }
    }
  }

  return moved;
}

function moveLeft() {
  let moved = false;

  for (let r = 0; r < 4; r++) {
    let line = grid[r].filter(function (x) { return x !== 0; });

    for (let j = 0; j < line.length - 1; j++) {
      if (line[j] === line[j + 1]) {
        line[j] *= 2;
        line[j + 1] = 0;
      }
    }

    line = line.filter(function (x) { return x !== 0; });
    while (line.length < 4) {
      line.push(0);
    }

    for (let c = 0; c < 4; c++) {
      if (grid[r][c] !== line[c]) {
        grid[r][c] = line[c];
        moved = true;
      }
    }
  }

  return moved;
}

function moveDown() {
  let moved = false;

  for (let c = 0; c < 4; c++) {
    let column = [];

    for (let r = 3; r >= 0; r--) {
      if (grid[r][c] !== 0) {
        column.push(grid[r][c]);
      }
    }

    for (let i = column.length - 1; i > 0; i--) {
      if (column[i] === column[i - 1]) {
        column[i] *= 2;
        column[i - 1] = 0;
      }
    }

    column = column.filter(function (x) { return x !== 0; });
    while (column.length < 4) {
      column.push(0);
    }

    for (let r = 3, idx = 0; r >= 0; r--, idx++) {
      if (grid[r][c] !== column[idx]) {
        grid[r][c] = column[idx];
        moved = true;
      }
    }
  }

  return moved;
}

function moveUp() {
  let moved = false;

  for (let c = 0; c < 4; c++) {
    let column = [];

    for (let r = 0; r < 4; r++) {
      if (grid[r][c] !== 0) {
        column.push(grid[r][c]);
      }
    }

    for (let i = 0; i < column.length - 1; i++) {
      if (column[i] === column[i + 1]) {
        column[i] *= 2;
        column[i + 1] = 0;
      }
    }

    column = column.filter(function (x) { return x !== 0; });
    while (column.length < 4) {
      column.push(0);
    }

    for (let r = 0; r < 4; r++) {
      if (grid[r][c] !== column[r]) {
        grid[r][c] = column[r];
        moved = true;
      }
    }
  }

  return moved;
}

function handleMove(direction) {
  if (gameOver) return;

  mergedCells = [];

  const before = cloneGrid(grid);
  const prevScore = totalScore;

  let moved = false;
  switch (direction) {
    case 'up':
      moved = moveUp();
      break;
    case 'down':
      moved = moveDown();
      break;
    case 'left':
      moved = moveLeft();
      break;
    case 'right':
      moved = moveRight();
      break;
  }

  if (!moved) return;

  stepsHistory.push({
    grid: before,
    score: prevScore
  });

  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const was = before[r][c];
      const now = grid[r][c];
      if (was !== 0 && now > was) {
        mergedCells.push({ r: r, c: c });
      }
    }
  }

  addRandomTiles(grid);
  recalcScore();
  draw();

  if (!hasMoves()) {
    gameOver = true;
    updateRecords(totalScore);
    renderRecords();
    showGameOver();
  }

  saveState();
}

function undo() {
  if (stepsHistory.length === 0) return;

  const last = stepsHistory.pop();
  grid = cloneGrid(last.grid);
  totalScore = last.score;
  gameOver = false;
  mergedCells = [];
  hideGameOver();

  draw();
  saveState();
}


function init() {
  loadRecords();
  renderRecords();

  const restored = loadState();
  if (!restored) {
    resetGame();
  } else {
    draw();
  }
}

document.addEventListener('keydown', function (event) {
  switch (event.key) {
    case 'ArrowUp':
      handleMove('up');
      break;
    case 'ArrowDown':
      handleMove('down');
      break;
    case 'ArrowLeft':
      handleMove('left');
      break;
    case 'ArrowRight':
      handleMove('right');
      break;
  }
});

btnRestart.addEventListener('click', resetGame);
btnUndo.addEventListener('click', undo);

btnUp.addEventListener('click', function () { handleMove('up'); });
btnDown.addEventListener('click', function () { handleMove('down'); });
btnLeft.addEventListener('click', function () { handleMove('left'); });
btnRight.addEventListener('click', function () { handleMove('right'); });

document.addEventListener('DOMContentLoaded', init);
