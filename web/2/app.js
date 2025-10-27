const STORAGE = 'todo';
let tasks = [];

function createElement(tag, options = {}) {
  const el = document.createElement(tag);

  if (options.class) el.className = options.class;
  if (options.text !== undefined) el.textContent = options.text;

  if (options.attrs) {
    for (const [key, value] of Object.entries(options.attrs)) {
      el.setAttribute(key, value);
    }
  }
  return el;
}

function save() {
  localStorage.setItem(STORAGE, JSON.stringify(tasks));
}

function load() {
  try {
    const s = localStorage.getItem(STORAGE);
    return s ? JSON.parse(s) : [];
  } catch (e) {
    return [];
  }
}

const container = createElement('div', {
  class: 'container'
});
document.body.appendChild(container);

const header = createElement('header', {
  class: 'header'
});

header.appendChild(createElement('h1', { 
  class: 'h1', text: 'Todo листик' 
}));

container.appendChild(header);

const main = createElement('main');
container.appendChild(main);

const controlsSection = createElement('section', { 
  class: 'controls' 
});

main.appendChild(controlsSection);

const form = createElement('form', { 
  class: 'form', attrs: { id: 'addForm' } 
});

const input = createElement('input', { 
  class: 'input', attrs: { placeholder: 'Новая задача', id: 'taskInput', name: 'title' } 
});

const date = createElement('input', { 
  class: 'small', attrs: { type: 'date', id: 'taskDate', name: 'due'} 
});

const add = createElement('button', { 
  class: 'btn', attrs: { type: 'submit' }, text: 'Добавить'
 });

form.appendChild(input);
form.appendChild(date);
form.appendChild(add);
controlsSection.appendChild(form);

const nav = createElement('nav', { 
  class: 'filters' 
});

const search = createElement('input', { 
  class: 'input', attrs: { placeholder: 'Поиск по названию', id: 'searchInput' } 
});

const status = createElement('select', { 
  class: 'small', attrs: { id: 'statusSel' } 
});

['all', 'active', 'completed'].forEach(v => {
  const o = createElement('option', { 
    attrs: { value: v }, text: v === 'all' ? 'Все' : v === 'active' ? 'Невыполненные' : 'Выполненные' 
  });
  status.appendChild(o);
});

const sort = createElement('select', { 
  class: 'small', attrs: { id: 'sortSel' } 
});
[['order', 'По порядку'], ['date-asc', 'Дата ↑'], ['date-desc', 'Дата ↓'], ['title-asc', 'A → Z'], ['title-desc', 'Z → A']]
  .forEach(s => sort.appendChild(createElement('option', {
     attrs: { value: s[0] }, text: s[1] 
    })));


nav.appendChild(search);
nav.appendChild(status);
nav.appendChild(sort);
controlsSection.appendChild(nav);

const listSection = createElement('section', { 
  class: 'list-section' 
});

main.appendChild(listSection);
const list = createElement('ul', { 
  class: 'list', attrs: { id: 'list' } 
});

listSection.appendChild(list);

function uid() {
  return Math.random().toString(36).slice(2, 9); 
}

function dateFunc(d) {
  if (!d) {
    return 'Без срока';
  }

  const date = new Date(d);
  if (isNaN(date)) {
    return '—';
  }

  return date.toLocaleDateString();
}

function render() {
  const search = (document.querySelector('#searchInput').value || '').toLowerCase().trim();
  const status = document.querySelector('#statusSel').value;
  const sort = document.querySelector('#sortSel').value;

  let arr = tasks.filter(t => {
    const okSearch = !search || t.title.toLowerCase().includes(search);
    const okStatus = status === 'all' || (status === 'active' && !t.completed) || (status === 'completed' && t.completed);
    return okSearch && okStatus;
  });

  arr = arr.slice().sort((a, b) => {
    if (sort === 'date-asc') {
      const A = a.due || '';
      const B = b.due || '';
      if (A === B) return a.order - b.order;
      return A.localeCompare(B);
    }
    if (sort === 'date-desc') {
      const A = a.due || '';
      const B = b.due || '';
      if (A === B) return a.order - b.order;
      return B.localeCompare(A);
    }
    if (sort === 'title-asc') {
      return a.title.toLowerCase().localeCompare(b.title.toLowerCase());
    }
    if (sort === 'title-desc') {
      return b.title.toLowerCase().localeCompare(a.title.toLowerCase());
    }
    return a.order - b.order;
  });

  while (list.firstChild) list.removeChild(list.firstChild);
  for (const task of arr) {
  const listItem = createElement('li', {
    class: 'item' + (task.completed ? ' completed' : ''),
    attrs: { 
      draggable: true, 
      'data-id': task.id 
    }
  });

  const leftContent = createElement('div', { class: 'left' });
  
  const checkbox = createElement('input', {
    attrs: { 
      type: 'checkbox', 
      'aria-label': 'Отметить задачу' 
    }
  });
  checkbox.checked = !!task.completed;
  checkbox.addEventListener('change', () => {
    task.completed = checkbox.checked;
    save();
    render();
  });

  const title = createElement('div', { 
    class: 'title', 
    text: task.title 
  });

  const meta = createElement('div', { 
    class: 'meta', 
    text: dateFunc(task.due) 
  });

  leftContent.appendChild(checkbox);
  leftContent.appendChild(title);
  leftContent.appendChild(meta);

  const actions = createElement('div', { class: 'actions' });
  
  const editButton = createElement('button', { 
    class: 'icon', 
    text: 'Ред.' 
  });
  
  const deleteButton = createElement('button', { 
    class: 'icon', 
    text: 'Удал.' 
  });

  actions.appendChild(editButton);
  actions.appendChild(deleteButton);

  listItem.appendChild(leftContent);
  listItem.appendChild(actions);

  editButton.addEventListener('click', () => {
    const newTitle = prompt('Введите новое название задачи', task.title);
    if (newTitle === null) return;
    
    const newDate = prompt('Новая дата (YYYY-MM-DD) или пусто', task.due || '');
    
    task.title = (newTitle || '').trim() || task.title;
    task.due = newDate ? newDate : null;
    
    save();
    render();
  });

  deleteButton.addEventListener('click', () => {
    if (!confirm('Удалить?')) return;
    
    tasks = tasks.filter(x => x.id !== task.id);
    renumber();
    save();
    render();
  });

  listItem.addEventListener('dragstart', (event) => {
    listItem.classList.add('dragging');
    event.dataTransfer.setData('text/plain', task.id);
  });

  listItem.addEventListener('dragend', () => {
    listItem.classList.remove('dragging');
  });

  list.appendChild(listItem);
}
}

function renumber() { tasks.forEach((t, i) => t.order = i); }

form.addEventListener('submit', (event) => {
  event.preventDefault();
  
  const title = input.value.trim();
  if (!title) return;
  
  const dueDate = date.value || null;
  const maxOrder = tasks.length ? Math.max(...tasks.map(task => task.order)) : 0;
  const newOrder = maxOrder + 1;
  
  const newTask = {
    id: uid(),
    title: title,
    due: dueDate,
    completed: false,
    order: newOrder
  };
  
  tasks.push(newTask);
  save();

  input.value = '';
  date.value = '';
  input.focus();
  
  render();
});

input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    add.click();
  }
});

search.addEventListener('input', render);
status.addEventListener('change', render);
sort.addEventListener('change', render);

let draggedItem = null;

list.addEventListener('dragstart', (event) => {
  draggedItem = event.target;
  event.target.classList.add('dragging');
});

list.addEventListener('dragover', (event) => {
  event.preventDefault();
  const afterElement = getDragAfterElement(list, event.clientY);
  const dragging = document.querySelector('.dragging');
  if (afterElement == null) {
    list.appendChild(dragging);
  } else {
    list.insertBefore(dragging, afterElement);
  }
});

list.addEventListener('drop', (event) => {
  event.preventDefault();
  const items = Array.from(list.querySelectorAll('li.item'));
  const newOrder = items.map(item => item.getAttribute('data-id'));
  
  tasks.sort((a, b) => {
    return newOrder.indexOf(a.id) - newOrder.indexOf(b.id);
  });
  
  renumber();
  save();
  render();
});

list.addEventListener('dragend', (event) => {
  event.target.classList.remove('dragging');
});

function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('li.item:not(.dragging)')];

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

(function init() {
  const loadedTasks = load();
  
  if (loadedTasks.length > 0) {
    tasks = loadedTasks.map((taskData, index) => ({
      id: taskData.id || uid(),
      title: taskData.title || 'Без названия',
      due: taskData.due || null,
      completed: !!taskData.completed,
      order: Number.isFinite(taskData.order) ? taskData.order : index
    }));
  } else {
    tasks = [];
  }
  
  tasks.sort((a, b) => a.order - b.order);
  render();
})();
