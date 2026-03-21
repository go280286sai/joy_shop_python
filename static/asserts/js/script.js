


/* =========================
   КОРЗИНА
========================= */
function addToCart(product) {
  const existing = cart.find(i => i.id === product.id);

  if (existing) {
    existing.qty++;
  } else {
    cart.push({ ...product, qty: 1 });
  }

  updateCart();
}

function updateCart() {
  localStorage.setItem("cart", JSON.stringify(cart));

  const container = document.getElementById("cartItems");
  const totalEl = document.getElementById("cartTotal");
  const carts_btn = document.getElementById("carts_btn");
  container.innerHTML = "";

  let total = 0;


  cart.forEach(item => {
    total += item.price * item.qty;

    const div = document.createElement("div");
    div.className = "cart-item";

    div.innerHTML = `
      <span>${item.name} x${item.qty}</span>
      <div>
        <button onclick="changeQty(${item.id}, -1)">-</button>
        <button onclick="changeQty(${item.id}, 1)">+</button>
      </div>
    `;

    container.appendChild(div);
  });
  totalEl.innerText = "Итого: " + total + " грн";
  carts_btn.innerHTML = "<button class='btn btn-success carts_btn' onclick='close_trash()'>Continue</button>" +
      "                  <button class='btn btn-danger carts_btn'>To pay</button>"
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);

  item.qty += delta;

  if (item.qty <= 0) {
    cart = cart.filter(i => i.id !== id);
  }

  updateCart();
}


/* =========================
   ОТКРЫТИЕ КОРЗИНЫ
========================= */
document.querySelector(".cart-btn").onclick = () => {
  document.getElementById("cartPanel").classList.toggle("open");
};

/* INIT */
updateCart();

document.getElementById("close_trash").onclick=()=>{
  document.getElementById("cartPanel").classList.toggle("open");
};

function close_trash(){
  document.getElementById("cartPanel").classList.toggle("open");
}

async function get_categories() {
  let response = await fetch("http://localhost:8000/api/v1/categories");
  return response;
}

get_categories().then(async response => {
  let categories = document.getElementById("categories");
  let txt = "";

  if (response.ok) {
    let data = await response.json();   // дождаться JSON
    console.log(data);

    let count = data.length;
    for (let i = 0; i < count; i++) {
      txt += `<a href="http://localhost:8000/api/v1/categories/${data[i].id}">${data[i].name}</a>`;
    }
  } else {
    console.error("Ошибка HTTP: " + response.status);
  }

  categories.innerHTML = txt;
});
