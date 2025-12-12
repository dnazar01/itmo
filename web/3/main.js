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

  for (const child of children) node.appendChild(child);
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

let tiles = [];
let nextTileId = 1;

function createTileObj(r, c, value, opts = { new: false }) {
  return {
    id: nextTileId++,
    r: r,
    c: c,
    value: value,
    merged: false,
    appearing: !!opts.new,
    vanishing: false
  };
}

function getCellMetrics() {
  const rect = board.getBoundingClientRect();
  const gap = 6;
  const padding = 6;
  const innerWidth = Math.max(0, rect.width - padding * 2);
  const totalGaps = gap * 3;
  const cellSize = Math.floor((innerWidth - totalGaps) / 4);
  return { cellSize, gap, padding, innerWidth, rect };
}

function posFor(r, c) {
  const { cellSize, gap, padding } = getCellMetrics();
  const x = Math.round(padding + c * (cellSize + gap));
  const y = Math.round(padding + r * (cellSize + gap));
  return { x, y, cellSize };
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

const nameInput = makeElement('input', {
  className: 'name-input',
  attrs: { type: 'text', placeholder: 'Введите имя' }
});
const btnSaveResult = makeElement('button', { className: 'btn save-btn', text: 'Сохранить результат' });
const btnRestartIcon = makeElement('button', { className: 'btn restart-icon', text: 'Начать заново ' });

wrap.appendChild(nameInput);
wrap.appendChild(btnSaveResult);
wrap.appendChild(btnRestartIcon);

function loadRecords() {
  const raw = localStorage.getItem(KEY_RECORDS);
  if (!raw) {
    bestList = [];
    return;
  }
  try {
    const arr = JSON.parse(raw);
    bestList = Array.isArray(arr) ? arr : [];
  } catch (e) {
    bestList = [];
  }
}

function saveRecords() {
  localStorage.setItem(KEY_RECORDS, JSON.stringify(bestList));
}

function updateRecords(newEntry) {
  let entry;
  if (typeof newEntry === 'number') entry = { name: null, score: newEntry };
  else if (newEntry && typeof newEntry === 'object' && typeof newEntry.score === 'number')
    entry = { name: newEntry.name || null, score: newEntry.score };
  else return;

  bestList.push(entry);
  bestList.sort(function (a, b) {
    return b.score - a.score;
  });
  
  if (bestList.length > 10) bestList = bestList.slice(0, 10);
  saveRecords();
}

function renderRecords() {
  while (recordsBody.firstChild) recordsBody.removeChild(recordsBody.firstChild);

  for (let i = 0; i < bestList.length; i++) {
    const tr = makeElement('tr');
    tr.appendChild(makeElement('td', { text: String(i + 1) }));
    const entry = bestList[i];
    const display =
      entry.name && entry.name.trim().length > 0 ? entry.name + ' — ' + entry.score : String(entry.score);
    tr.appendChild(makeElement('td', { text: display }));
    recordsBody.appendChild(tr);
  }
}

function saveState() {
  const state = { grid: grid, score: totalScore, gameOver: gameOver };
  localStorage.setItem(KEY_STATE, JSON.stringify(state));
}

function loadStateRaw() {
  const raw = localStorage.getItem(KEY_STATE);
  if (!raw) return false;
  try {
    const state = JSON.parse(raw);
    if (!state || !Array.isArray(state.grid)) return false;
    grid = state.grid;
    if (typeof state.score === 'number') totalScore = state.score;
    if (typeof state.gameOver === 'boolean') gameOver = state.gameOver;
    if (gameOver) showGameOver();
    return true;
  } catch (e) {
    return false;
  }
}

function ensureTileElement(t) {
  let el = board.querySelector('[data-tid="' + t.id + '"]');
  if (!el) {
    el = document.createElement('div');
    el.setAttribute('data-tid', t.id);
    el.className = 'tile';
    board.appendChild(el);
    const { cellSize } = getCellMetrics();
    el.style.width = cellSize + 'px';
    el.style.height = cellSize + 'px';
    el.style.transform = `translate3d(0px, 0px, 0) scale(1)`;
    el.style.opacity = '0';
  }
  el.textContent = t.value;
  return el;
}

function applyTransform(el, x, y, scale) {
  el.style.setProperty('--tx', x + 'px');
  el.style.setProperty('--ty', y + 'px');
  el.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${scale})`;
}

function draw() {
  const existingIds = new Set();

  for (const t of tiles) {
    const el = ensureTileElement(t);
    existingIds.add(t.id);

    el.className = 'tile tile-' + t.value;
    if (t.appearing) el.classList.add('tile-appearing');
    if (t.merged) el.classList.add('tile-merged');
    if (t.vanishing) el.classList.add('tile-vanish');

    const { x, y, cellSize } = posFor(t.r, t.c);
    const scale = t.appearing ? 0.62 : 1;

    el.style.opacity = t.vanishing ? '0' : '1';
    el.style.filter = t.vanishing ? 'blur(0)' : 'none';
    el.style.width = cellSize + 'px';
    el.style.height = cellSize + 'px';

    if (t.appearing) {
      applyTransform(el, x, y, 0.62);
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          el.classList.remove('tile-appearing');
          el.style.opacity = '1';
          applyTransform(el, x, y, 1);
        });
      });
    } else {
      applyTransform(el, x, y, scale);
    }
  }

  scoreText.textContent = 'Счёт: ' + totalScore;

  board.querySelectorAll('.tile').forEach(function (el) {
    const tid = Number(el.getAttribute('data-tid'));
    if (!existingIds.has(tid)) {
      if (!el.classList.contains('tile-vanish')) {
        el.classList.add('tile-vanish');
        el.style.opacity = '0';
        const tx = el.style.getPropertyValue('--tx') || '0px';
        const ty = el.style.getPropertyValue('--ty') || '0px';
        el.style.transform = `translate3d(${tx}, ${ty}, 0) scale(0.9)`;
        setTimeout(() => {
          if (el.parentNode) el.parentNode.removeChild(el);
        }, 360);
      }
    }
  });

  tiles.forEach((t) => {
    t.appearing = false;
    t.merged = false;
  });
}

function addRandomTiles(field) {
  let count = Math.random() < 0.9 ? 1 : 2;
  const empty = [];

  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (field[r][c] === 0) empty.push({ r, c });
    }
  }

  if (empty.length === 0) return;

  for (let i = empty.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const t = empty[i];
    empty[i] = empty[j];
    empty[j] = t;
  }

  for (let k = 0; k < count && k < empty.length; k++) {
    const cell = empty[k];
    const val = Math.random() < 0.9 ? 2 : 4;
    field[cell.r][cell.c] = val;
    tiles.push(createTileObj(cell.r, cell.c, val, { new: true }));
  }
}

function hasMoves() {
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (grid[r][c] === 0) return true;
    }
  }

  for (let r = 0; r < 4; r++){
     for (let c = 0; c < 3; c++) {
      if (grid[r][c] === grid[r][c + 1]) {
        return true;
      }
    }
  }

  for (let c = 0; c < 4; c++) {
    for (let r = 0; r < 3; r++) {
      if (grid[r][c] === grid[r + 1][c]) {
        return true;
      }
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
  tiles = [];
  nextTileId = 1;

  hideGameOver();
  addRandomTiles(grid);
  addRandomTiles(grid);

  recalcScore();

  tiles = [];
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (grid[r][c] !== 0) tiles.push(createTileObj(r, c, grid[r][c], { new: true }));
    }
  }

  draw();
  saveState();
}

function isMergedCell(r, c) {
  return mergedCells.some(function (cell) {
    return cell.r === r && cell.c === c;
  });
}

function moveRight() {
  let moved = false;

  for (let r = 0; r < 4; r++) {
    let line = grid[r].filter((x) => x !== 0);

    for (let j = line.length - 1; j > 0; j--) if (line[j] === line[j - 1]) {
      line[j] *= 2;
      line[j - 1] = 0;
    }

    line = line.filter((x) => x !== 0);
    while (line.length < 4) line.unshift(0);

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
    let line = grid[r].filter((x) => x !== 0);

    for (let j = 0; j < line.length - 1; j++) if (line[j] === line[j + 1]) {
      line[j] *= 2;
      line[j + 1] = 0;
    }

    line = line.filter((x) => x !== 0);
    while (line.length < 4) line.push(0);

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

    for (let r = 3; r >= 0; r--) if (grid[r][c] !== 0) column.push(grid[r][c]);

    for (let i = column.length - 1; i > 0; i--) if (column[i] === column[i - 1]) {
      column[i] *= 2;
      column[i - 1] = 0;
    }

    column = column.filter((x) => x !== 0);
    while (column.length < 4) column.push(0);

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

    for (let r = 0; r < 4; r++) if (grid[r][c] !== 0) column.push(grid[r][c]);

    for (let i = 0; i < column.length - 1; i++) if (column[i] === column[i + 1]) {
      column[i] *= 2;
      column[i + 1] = 0;
    }

    column = column.filter((x) => x !== 0);
    while (column.length < 4) column.push(0);

    for (let r = 0; r < 4; r++) {
      if (grid[r][c] !== column[r]) {
        grid[r][c] = column[r];
        moved = true;
      }
    }
  }

  return moved;
}

function syncTilesWithGrid(prevGrid) {
  const prev = tiles.slice();
  const usedPrevIds = new Set();
  const mapped = [];
  const vanishing = [];

  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const val = grid[r][c];
      if (val === 0) continue;

      let bestIndex = -1;
      let bestDist = Infinity;

      for (let i = 0; i < prev.length; i++) {
        const p = prev[i];
        if (usedPrevIds.has(p.id)) continue;
        if (p.value !== val) continue;
        const dist = Math.abs(p.r - r) + Math.abs(p.c - c);
        if (dist < bestDist) {
          bestDist = dist;
          bestIndex = i;
        }
      }

      if (bestIndex !== -1) {
        const t = prev[bestIndex];
        usedPrevIds.add(t.id);
        t.r = r;
        t.c = c;
        t.value = val;
        t.vanishing = false;
        if (prevGrid && prevGrid[r][c] && val > prevGrid[r][c]) t.merged = true;
        else t.merged = false;
        t.appearing = false;
        mapped.push(t);
      } else {
        const t = {
          id: nextTileId++,
          r: r,
          c: c,
          value: val,
          merged: false,
          appearing: true,
          vanishing: false
        };
        if (prevGrid && prevGrid[r][c] && val > prevGrid[r][c]) t.merged = true;
        mapped.push(t);
      }
    }
  }

  for (let i = 0; i < prev.length; i++) {
    const p = prev[i];
    if (!usedPrevIds.has(p.id)) {
      p.vanishing = true;
      vanishing.push(p);
    }
  }

  tiles = mapped.concat(vanishing);
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

  stepsHistory.push({ grid: before, score: prevScore });

  addRandomTiles(grid);
  recalcScore();
  syncTilesWithGrid(before);
  draw();
  if (!hasMoves()) {
    gameOver = true;
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

  tiles = [];
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (grid[r][c] !== 0) tiles.push(createTileObj(r, c, grid[r][c]));
    }
  }

  draw();
  saveState();
}

function loadState() {
  const ok = loadStateRaw();
  if (!ok) return false;

  tiles = [];
  nextTileId = 1;
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (grid[r][c] !== 0) tiles.push(createTileObj(r, c, grid[r][c]));
    }
  }

  return true;
}

function init() {
  loadRecords();
  renderRecords();

  const restored = loadState();
  if (!restored) resetGame();
  else draw();
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

btnUp.addEventListener('click', function () {
  handleMove('up');
});
btnDown.addEventListener('click', function () {
  handleMove('down');
});
btnLeft.addEventListener('click', function () {
  handleMove('left');
});
btnRight.addEventListener('click', function () {
  handleMove('right');
});

function showGameOver() {
  message.textContent = 'Игра окончена. Введите имя для сохранения рекорда:';
  message.classList.add('message--visible');

  nameInput.value = '';
  nameInput.style.display = 'block';
  btnSaveResult.style.display = 'inline-block';
  btnRestartIcon.style.display = 'inline-block';
}

function hideSaveUI() {
  nameInput.style.display = 'none';
  btnSaveResult.style.display = 'none';
  btnRestartIcon.style.display = 'none';
}

btnSaveResult.addEventListener('click', function () {
  const name = nameInput.value.trim();
  if (name.length === 0) return;

  updateRecords({ name: name, score: totalScore });
  renderRecords();

  nameInput.style.display = 'none';
  btnSaveResult.style.display = 'none';
  message.textContent = 'Ваш рекорд сохранен.';
});

btnRestartIcon.addEventListener('click', function () {
  hideSaveUI();
  resetGame();
});

const origResetGame = resetGame;
resetGame = function () {
  hideSaveUI();
  message.classList.remove('message--visible');
  origResetGame();
};

const origUndo = undo;
undo = function () {
  hideSaveUI();
  origUndo();
};

document.addEventListener('DOMContentLoaded', init);
window.addEventListener('resize', function () {
  draw();
});
