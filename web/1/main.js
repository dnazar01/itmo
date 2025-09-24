
const productsGrid = document.getElementById("productsGrid");
const cartList = document.getElementById("cartList");
const cartEmpty = document.getElementById("cartEmpty");
const cartTotalEl = document.getElementById("cartTotal");
const cartCountEl = document.getElementById("cartCount");
const checkoutModal = document.getElementById("checkoutModal");
const checkoutBtn = document.getElementById("checkoutBtn");
const closeModalBtn = document.getElementById("closeModalBtn");
const checkoutForm = document.getElementById("checkoutForm");

let cart = loadCart();

function loadCart() {
  try {
    return JSON.parse(localStorage.getItem("instruments_cart")) || [];
  } catch {
    return [];
  }
}

function saveCart() {
  localStorage.setItem("instruments_cart", JSON.stringify(cart));
}

function currency(val) {
  return `${Number(val).toLocaleString("ru-RU")} ₽`;
}

function addToCart(product) {
  const found = cart.find((i) => i.id === product.id);
  if (found) {
    found.qty += 1;
  } else {
    const newItem = {
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      qty: 1
    };
    cart.push(newItem);
  }
  saveCart();
  renderCart();
}

function updateQty(id, qty) {
  const item = cart.find((i) => i.id === id);
  if (!item) return;
  const newQty = Math.max(1, Number(qty) || 1);
  item.qty = newQty;
  saveCart();
  renderCartTotals();
}

function removeFromCart(id) {
  cart = cart.filter((i) => i.id !== id);
  saveCart();
  renderCart();
}

function cartCount() {
  return cart.reduce((s, i) => s + i.qty, 0);
}

function cartTotal() {
  return cart.reduce((s, i) => s + i.qty * i.price, 0);
}

productsGrid.addEventListener("click", (e) => {
  const btn = e.target.closest(".product__card-btn");
  if (!btn) return;
  addToCart({
    id: btn.dataset.id,
    name: btn.dataset.name,
    price: Number(btn.dataset.price),
    image: btn.dataset.img,
  });
});

function renderCart() {
  cartList.innerHTML = "";
  cartEmpty.style.display = cart.length ? "none" : "block";

  cart.forEach((i) => {
    const row = document.createElement("div");
    row.className = "cart__item";
    row.innerHTML = `
      <img class="cart__thumb" src="${i.image}" alt="${i.name}">
      <div>
        <div class="cart__name">${i.name}</div>
        <div class="cart__controls">
          <input class="cart__qty" id="qty-${i.id}" type="number" min="1" value="${i.qty}" data-id="${i.id}">
          <button class="cart__remove" type="button" data-id="${i.id}">Удалить</button>
        </div>
      </div>
      <div class="cart__price">${currency(i.price * i.qty)}</div>
    `;
    cartList.appendChild(row);
  });

  cartList.querySelectorAll(".cart__qty").forEach((input) => {
    input.addEventListener("input", (e) => {
      updateQty(e.target.dataset.id, e.target.value);
    });
  });
  cartList.querySelectorAll(".cart__remove").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      removeFromCart(e.target.dataset.id);
    });
  });

  renderCartTotals();
}

function renderCartTotals() {
  cartTotalEl.textContent = currency(cartTotal());
  cartCountEl.textContent = cartCount();

  cartList.querySelectorAll(".cart__item").forEach((itemEl) => {
    const input = itemEl.querySelector(".cart__qty");
    if (!input) return;
    const id = input.dataset.id;
    const item = cart.find((x) => x.id === id);
    if (item) {
      itemEl.querySelector(".cart__price").textContent = currency(
        item.price * item.qty
      );
    }
  });

  cartEmpty.style.display = cart.length ? "none" : "block";
}

function openModal() {
  checkoutModal.classList.add("modal__open");
}

function closeModal() {
  checkoutModal.classList.remove("modal__open");
}

checkoutBtn.addEventListener("click", openModal);
closeModalBtn.addEventListener("click", closeModal);
checkoutModal.addEventListener("click", (e) => {
  if (e.target === checkoutModal) closeModal();
});

checkoutForm.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!cart.length) {
    alert("Корзина пуста");
    return;
  }
  alert("Заказ создан");
  cart = [];
  saveCart();
  renderCart();
  checkoutForm.reset();
  closeModal();
});

renderCart();

