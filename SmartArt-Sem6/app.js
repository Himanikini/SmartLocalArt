let listProductHTML = document.querySelector('.listProduct');
let listCartHTML = document.querySelector('.listCart');
let iconCart = document.querySelector('.icon-cart');
let iconCartSpan = document.querySelector('.icon-cart span');
let body = document.querySelector('body');
let closeCart = document.querySelector('.close');
let products = [];
let cart = [];

// Toggle cart visibility
iconCart.addEventListener('click', () => {
    body.classList.toggle('showCart');
});
closeCart.addEventListener('click', () => {
    body.classList.toggle('showCart');
});

// Add products to the page
const addDataToHTML = () => {
    if (products.length > 0) {
        products.forEach(product => {
            let newProduct = document.createElement('div');
            newProduct.dataset.id = product.id;
            newProduct.classList.add('item');
            newProduct.innerHTML = `
                <img src="${product.image}" alt="">
                <h2>${product.name}</h2>
                <div class="price">Ru.${product.price}</div>
                <button class="addCart">Add To Cart</button>`;
            listProductHTML.appendChild(newProduct);
        });
    }
};

// Add to cart functionality
listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('addCart')) {
        let id_product = positionClick.parentElement.dataset.id;
        addToCart(id_product);
    }
});

const addToCart = (product_id) => {
    let positionThisProductInCart = cart.findIndex((value) => value.product_id == product_id);
    if (cart.length <= 0) {
        cart = [{
            product_id: product_id,
            quantity: 1
        }];
    } else if (positionThisProductInCart < 0) {
        cart.push({
            product_id: product_id,
            quantity: 1
        });
    } else {
        cart[positionThisProductInCart].quantity = cart[positionThisProductInCart].quantity + 1;
    }
    addCartToHTML();
    addCartToMemory();
};

const addCartToMemory = () => {
    localStorage.setItem('cart', JSON.stringify(cart));
};

const addCartToHTML = () => {
    listCartHTML.innerHTML = '';
    let totalQuantity = 0;
    if (cart.length > 0) {
        cart.forEach(item => {
            totalQuantity += item.quantity;
            let newItem = document.createElement('div');
            newItem.classList.add('item');
            newItem.dataset.id = item.product_id;

            let positionProduct = products.findIndex((value) => value.id == item.product_id);
            let info = products[positionProduct];
            listCartHTML.appendChild(newItem);
            newItem.innerHTML = `
                <div class="image">
                    <img src="${info.image}">
                </div>
                <div class="name">
                    ${info.name}
                </div>
                <div class="totalPrice">Ru.${info.price * item.quantity}</div>
                <div class="quantity">
                    <span class="minus"><</span>
                    <span>${item.quantity}</span>
                    <span class="plus">></span>
                </div>
            `;
        });
    }
    iconCartSpan.innerText = totalQuantity;
};

// Change cart quantity
listCartHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('minus') || positionClick.classList.contains('plus')) {
        let product_id = positionClick.parentElement.parentElement.dataset.id;
        let type = positionClick.classList.contains('plus') ? 'plus' : 'minus';
        changeQuantityCart(product_id, type);
    }
});

const changeQuantityCart = (product_id, type) => {
    let positionItemInCart = cart.findIndex((value) => value.product_id == product_id);
    if (positionItemInCart >= 0) {
        if (type === 'plus') {
            cart[positionItemInCart].quantity += 1;
        } else {
            let changeQuantity = cart[positionItemInCart].quantity - 1;
            if (changeQuantity > 0) {
                cart[positionItemInCart].quantity = changeQuantity;
            } else {
                cart.splice(positionItemInCart, 1);
            }
        }
    }
    addCartToHTML();
    addCartToMemory();
};

// Initial data fetching and rendering
const initApp = () => {
    fetch('products.json')
        .then(response => response.json())
        .then(data => {
            products = data;
            addDataToHTML();

            // Retrieve cart from localStorage
            if (localStorage.getItem('cart')) {
                cart = JSON.parse(localStorage.getItem('cart'));
                addCartToHTML();
            }
        });
};

// Checkout button event
const buyButton = document.querySelector('.checkOut');
buyButton.addEventListener('click', async function () {
    // Get cart details from localStorage
    let totalPrice = 0;

cart.forEach(cartItem => {
    // Find the corresponding product in the products array
    const product = products.find(prod => prod.id == cartItem.product_id);
    
    // Add the product's price multiplied by the quantity to the total price
    if (product) {
        totalPrice += product.price * cartItem.quantity;
    }
});
    console.log(totalPrice)
    // Prepare Razorpay options
    var options = {
        "key": "rzp_test_frIfdCScDuiqjD", // Replace with your Razorpay key_id
        "amount": totalPrice*100, // Amount is in paise, convert your amount to paise
        "currency": "INR",
        "name": "AH EcommerceStore",
        "description": "Test Transaction",
        "image": "", // Optional: add your logo URL
        "order_id": "", // Pass the order ID if you have one from your server
        "handler": function (response) {
            alert("Payment successful! Payment ID: " + response.razorpay_payment_id);
            console.log(response)
            // Handle the successful payment here (e.g., save payment details, update UI)
             localStorage.removeItem('cart');
             location.reload()
        },
        "prefill": {
            "name": "Your Customer Name",
            "email": "customer.email@example.com",
            "contact": "9999999999"
        },
        "theme": {
            "color": "#3399cc"
        }
    };

    // Create a new Razorpay instance
    var rzp1 = new Razorpay(options);

    // Open the Razorpay checkout interface
    await rzp1.open();
    

    // Prevent the default behavior

    // Optional: Clear the cart after successful payment
    
    // await location.reload()
});

initApp();
