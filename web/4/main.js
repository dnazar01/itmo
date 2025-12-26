let appState = {
  primary: null,
  cities: []
};

let primaryCandidate = null;
let addCandidate = null;

const KEY_APP = 'weather';

const geoBlock = document.getElementById('geoBlock');
const geoStatus = document.getElementById('geoStatus');
const geoContent = document.getElementById('geoContent');
const geoError = document.getElementById('geoError');
const primaryCityBlock = document.getElementById('primaryCityBlock');
const primaryCityStatus = document.getElementById('primaryCityStatus');
const primaryCityContent = document.getElementById('primaryCityContent');
const primaryCityError = document.getElementById('primaryCityError');
const primaryCityForm = document.getElementById('primaryCityForm');
const primaryCityInput = document.getElementById('primaryCityInput');
const primaryCityDropdown = document.getElementById('primaryCityDropdown');
const primaryCityFieldError = document.getElementById('primaryCityFieldError');

const citiesList = document.getElementById('citiesList');

const btnRefresh = document.getElementById('btnRefresh');
const btnAddCity = document.getElementById('btnAddCity');

const addCityModal = document.getElementById('addCityModal');
const modalBackdrop = document.getElementById('modalBackdrop');
const btnCloseModal = document.getElementById('btnCloseModal');
const btnCancelModal = document.getElementById('btnCancelModal');

const addCityForm = document.getElementById('addCityForm');
const addCityInput = document.getElementById('addCityInput');
const addCityDropdown = document.getElementById('addCityDropdown');
const addCityFieldError = document.getElementById('addCityFieldError');

function saveState() {
  localStorage.setItem(KEY_APP, JSON.stringify(appState));
}

function loadState() {
  const data = localStorage.getItem(KEY_APP);
  if (!data) return false;
  try {
    const parsed = JSON.parse(data);
    if (!parsed || typeof parsed !== 'object') return false;

    if (parsed.primary && typeof parsed.primary === 'object') appState.primary = parsed.primary;
    if (Array.isArray(parsed.cities)) appState.cities = parsed.cities;

    return true;
  } catch (e) {
    return false;
  }
}

function show(el) {
  el.style.display = '';
}

function hide(el) {
  el.style.display = 'none';
}

function setText(el, text) {
  el.textContent = text == null ? '' : String(text);
}

function clearNode(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

function createEl(tag, { className, attrs, text } = {}, children = []) {
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

function openModal() {
  addCandidate = null;
  addCityInput.value = '';
  addCityFieldError.textContent = '';
  hideDropdown(addCityDropdown);
  addCityModal.style.display = 'block';
  addCityInput.focus();
}

function closeModal() {
  addCityModal.style.display = 'none';
}

function showLoader(container) {
  clearNode(container);
  container.appendChild(createEl('div', { className: 'loader', text: 'Загрузка...' }));
}


const weatherTextMap = new Map([
  [[0], 'Ясно'],
  [[1, 2], 'Малооблачно'],
  [[3], 'Пасмурно'],
  [[45, 48], 'Туман'],
  [[51, 53, 55], 'Морось'],
  [[61, 63, 65], 'Дождь'],
  [[66, 67], 'Ледяной дождь'],
  [[71, 73, 75], 'Снег'],
  [[77], 'Снежные зерна'],
  [[80, 81, 82], 'Ливни'],
  [[85, 86], 'Снегопад'],
  [[95], 'Гроза'],
  [[96, 99], 'Гроза с градом']
]);

const weatherEmojiMap = new Map([
  [[0], '☀️'],
  [[1, 2], '🌤️'],
  [[3], '☁️'],
  [[45, 48], '🌫️'],
  [[51, 53, 55], '🌦️'],
  [[61, 63, 65], '🌧️'],
  [[71, 73, 75], '❄️'],
  [[80, 81, 82], '🌧️'],
  [[95, 96, 99], '⛈️']
]);

function fromMap(map, code, fallback) {
  for (const [codes, value] of map) {
    if (codes.includes(code)) return value;
  }
  return fallback;
}

function weatherText(code) {
  return fromMap(weatherTextMap, code, 'Неизвестно');
}

function weatherEmoji(code) {
  return fromMap(weatherEmojiMap, code, '🌡️');
}


function formatDate(iso) {
  const d = new Date(iso);
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  return dd + '.' + mm;
}

function buildForecastView(data) {
  const daily = data.daily;
  if (!daily || !daily.time || daily.time.length < 3) {
    return createEl('div', { className: 'error', text: 'Нет данных прогноза' });
  }

  const box = createEl('div', { className: 'forecast' });

  for (let i = 0; i < 3; i++) {
    const date = daily.time[i];
    const code = daily.weathercode[i];
    const tMax = daily.temperature_2m_max[i];
    const tMin = daily.temperature_2m_min[i];

    const card = createEl('div', { className: 'day' });

    card.appendChild(createEl('div', { className: 'day__date', text: (i === 0 ? 'Сегодня' : formatDate(date)) }));
    card.appendChild(createEl('div', { className: 'badge', text: weatherEmoji(code) + ' ' + weatherText(code) }));
    card.appendChild(createEl('div', { className: 'day__row' }, [
      createEl('div', { text: 'Макс' }),
      createEl('div', { text: Math.round(tMax) + '°' })
    ]));
    card.appendChild(createEl('div', { className: 'day__row' }, [
      createEl('div', { text: 'Мин' }),
      createEl('div', { text: Math.round(tMin) + '°' })
    ]));

    box.appendChild(card);
  }

  return box;
}

function fetchWeather(lat, lon) {
  const url =
    'https://api.open-meteo.com/v1/forecast' +
    '?latitude=' + encodeURIComponent(lat) +
    '&longitude=' + encodeURIComponent(lon) +
    '&daily=weathercode,temperature_2m_max,temperature_2m_min' +
    '&current_weather=true' +
    '&timezone=auto';

  return fetch(url).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  });
}

function setBlockError(blockEl, msg) {
  const errorEl = blockEl.querySelector('.error');
  if (!errorEl) return;
  errorEl.textContent = msg || '';
}

function requestGeo() {
  setText(geoError, '');
  setText(geoStatus, 'Запрос геопозиции...');
  showLoader(geoContent);

  if (!navigator.geolocation) {
    setText(geoStatus, '');
    setText(geoError, 'Геолокация не поддерживается браузером');
    showPrimaryCityForm(true);
    return;
  }

  navigator.geolocation.getCurrentPosition(function (pos) {
  const lat = pos.coords.latitude;
  const lon = pos.coords.longitude;

  appState.primary = {
    type: 'geo',
    label: 'Текущее местоположение',
    lat: lat,
    lon: lon
  };

  saveState();
  renderAll();
  }, function () {
  setText(geoStatus, '');
  setText(geoError, 'Доступ к геолокации отклонен. Введите город вручную.');

  appState.primary = {
    type: 'city',
    name: '',
    lat: null,
    lon: null
  };

  hide(geoBlock);
  show(primaryCityBlock);
  showPrimaryCityForm(true);
}, { enableHighAccuracy: false, timeout: 10000 });


}

function showPrimaryCityForm(showIt) {
  if (showIt) primaryCityForm.style.display = 'flex';
  else primaryCityForm.style.display = 'none';
}


function hideGeoBlockIfNeed() {
  if (appState.primary && appState.primary.type === 'geo') {
    show(geoBlock);
    hide(primaryCityBlock);
  } else {
    hide(geoBlock);
    show(primaryCityBlock);
  }
}

function fetchAndRenderPrimary() {
  hideGeoBlockIfNeed();

  if (!appState.primary) {
    show(geoBlock);
    show(primaryCityBlock);
    showPrimaryCityForm(true);
    return;
  }

  if (appState.primary.type === 'geo') {
    setText(geoStatus, 'Обновление...');
    setText(geoError, '');
    showLoader(geoContent);

    fetchWeather(appState.primary.lat, appState.primary.lon)
      .then(function (data) {
        setText(geoStatus, 'Готово');
        clearNode(geoContent);
        geoContent.appendChild(buildForecastView(data));
      })
      .catch(function () {
        setText(geoStatus, '');
        setText(geoError, 'Ошибка загрузки погоды');
      });

    return;
  }

  if (appState.primary.type === 'city') {
    setText(primaryCityStatus, 'Обновление...');
    setText(primaryCityError, '');
    showLoader(primaryCityContent);

    fetchWeather(appState.primary.lat, appState.primary.lon)
      .then(function (data) {
        setText(primaryCityStatus, 'Готово');
        clearNode(primaryCityContent);
        primaryCityContent.appendChild(buildForecastView(data));
      })
      .catch(function () {
        setText(primaryCityStatus, '');
        setText(primaryCityError, 'Ошибка загрузки погоды');
      });

    return;
  }
}

function renderCitiesList() {
  clearNode(citiesList);

  if (!appState.cities || appState.cities.length === 0) {
    citiesList.appendChild(createEl('div', { className: 'small', text: 'Пока нет добавленных городов' }));
    return;
  }

  for (let i = 0; i < appState.cities.length; i++) {
    const city = appState.cities[i];

    const card = createEl('div', { className: 'cityCard' });

    const head = createEl('div', { className: 'cityHead' });
    const name = createEl('div', { className: 'cityName', text: city.name });

    const removeBtn = createEl('button', { className: 'iconBtn', text: 'Удалить' });
    removeBtn.addEventListener('click', function () {
      appState.cities.splice(i, 1);
      saveState();
      renderAll();
    });

    head.appendChild(name);
    head.appendChild(removeBtn);

    const status = createEl('div', { className: 'small', text: '' });
    const err = createEl('div', { className: 'error', text: '' });
    const content = createEl('div', { className: 'content' });

    card.appendChild(head);
    card.appendChild(status);
    card.appendChild(content);
    card.appendChild(err);

    citiesList.appendChild(card);

    status.textContent = 'Обновление...';
    showLoader(content);

    fetchWeather(city.lat, city.lon)
      .then(function (data) {
        status.textContent = 'Готово';
        clearNode(content);
        content.appendChild(buildForecastView(data));
      })
      .catch(function () {
        status.textContent = '';
        err.textContent = 'Ошибка загрузки погоды';
      });
  }
}

function renderAll() {
  fetchAndRenderPrimary();
  renderCitiesList();
}

function geocode(query) {
  const url =
    'https://geocoding-api.open-meteo.com/v1/search' +
    '?name=' + encodeURIComponent(query) +
    '&count=7&language=ru&format=json';

  return fetch(url).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function (data) {
    if (!data || !Array.isArray(data.results)) return [];
    return data.results.map(function (x) {
      const parts = [];
      if (x.name) parts.push(x.name);
      if (x.admin1) parts.push(x.admin1);
      if (x.country) parts.push(x.country);
      return {
        label: parts.join(', '),
        name: x.name,
        lat: x.latitude,
        lon: x.longitude
      };
    });
  });
}

function showDropdown(drop, items, onPick) {
  clearNode(drop);

  if (!items || items.length === 0) {
    hideDropdown(drop);
    return;
  }

  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const node = createEl('div', { className: 'dropdown__item', text: it.label });
    node.addEventListener('click', function () {
      onPick(it);
      hideDropdown(drop);
    });
    drop.appendChild(node);
  }

  drop.style.display = 'block';
}

function hideDropdown(drop) {
  drop.style.display = 'none';
  clearNode(drop);
}

function setupAutocomplete(input, dropdown, setCandidate, setError) {
  let t = 0;

  input.addEventListener('input', function () {
    const q = input.value.trim();
    setError('');
    setCandidate(null);

    if (t) clearTimeout(t);

    if (q.length < 2) {
      hideDropdown(dropdown);
      return;
    }

    t = setTimeout(function () {
      geocode(q)
        .then(function (items) {
          showDropdown(dropdown, items, function (picked) {
            input.value = picked.label;
            setCandidate(picked);
            setError('');
          });
        })
        .catch(function () {
          hideDropdown(dropdown);
        });
    }, 300);
  });

  document.addEventListener('click', function (e) {
    if (e.target === input) return;
    if (dropdown.contains(e.target)) return;
    hideDropdown(dropdown);
  });
}

function validatePicked(candidate, setError) {
  if (!candidate) {
    setError('Выберите город из списка');
    return false;
  }
  return true;
}

function initPrimaryFlow() {
  if (!appState.primary) {
    show(geoBlock);
    show(primaryCityBlock);
    showPrimaryCityForm(false);
    requestGeo();
    return;
  }

  if (appState.primary.type === 'geo') {
    show(geoBlock);
    hide(primaryCityBlock);
  } else {
    hide(geoBlock);
    show(primaryCityBlock);
    showPrimaryCityForm(false);
  }
}

btnRefresh.addEventListener('click', function () {
  renderAll();
});

btnAddCity.addEventListener('click', function () {
  openModal();
});

modalBackdrop.addEventListener('click', function () {
  closeModal();
});

btnCloseModal.addEventListener('click', function () {
  closeModal();
});

btnCancelModal.addEventListener('click', function () {
  closeModal();
});

primaryCityForm.addEventListener('submit', function (e) {
  e.preventDefault();

  primaryCityFieldError.textContent = '';
  if (!validatePicked(primaryCandidate, function (m) { primaryCityFieldError.textContent = m; })) return;

  appState.primary = {
    type: 'city',
    name: primaryCandidate.label,
    lat: primaryCandidate.lat,
    lon: primaryCandidate.lon
  };

  saveState();
  showPrimaryCityForm(false);
  renderAll();
});

addCityForm.addEventListener('submit', function (e) {
  e.preventDefault();

  addCityFieldError.textContent = '';

  if (!addCandidate) {
    const first = addCityDropdown.querySelector('.dropdown__item');
    if (first) {
      first.click();
    }
  }

  if (!validatePicked(addCandidate, function (m) { addCityFieldError.textContent = m; })) return;


  const exists = appState.cities.some(function (c) {
    return c.name === addCandidate.label;
  });

  if (exists) {
    addCityFieldError.textContent = 'Этот город уже добавлен';
    return;
  }

  appState.cities.push({
    name: addCandidate.label,
    lat: addCandidate.lat,
    lon: addCandidate.lon
  });

  saveState();
  closeModal();
  renderAll();
});

setupAutocomplete(
  primaryCityInput,
  primaryCityDropdown,
  function (x) { primaryCandidate = x; },
  function (m) { primaryCityFieldError.textContent = m; }
);

setupAutocomplete(
  addCityInput,
  addCityDropdown,
  function (x) { addCandidate = x; },
  function (m) { addCityFieldError.textContent = m; }
);

document.addEventListener('DOMContentLoaded', function () {
  loadState();
  initPrimaryFlow();
  renderAll();
});
