// update cart 
var update_cart = document.getElementsByClassName("update-cart");
for (let i = 0; i < update_cart.length; i++) {
    update_cart[i].addEventListener("click", function () {
        let productId = update_cart[i].getAttribute("product_id");
        let action = update_cart[i].getAttribute("action");

        console.log({
            'productId': productId, 
            'action': action
        });
        console.log("User:",user);

        if (user === 'AnonymousUser') {
            location.assign('/admin/'); // login
        }
        else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    var url = '/update_cart/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    }).then((response) => {
        return response.json();
    }).then((data) => {
        location.reload();
    });
}

// delete category or product
var delete_item = document.getElementsByClassName("delete-item");
for (let i = 0; i < delete_item.length; i++) {
    delete_item[i].addEventListener("click", function () {
        let item = delete_item[i].getAttribute("item");
        let model = delete_item[i].getAttribute("model");

        console.log({
            model: item, 
            'action': 'remove'
        });

        deleteItem(item, model);
    });
}

function deleteItem(item, model) {
    var url = `/${model}/delete/${item}/`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if (model == 'product') {
            location.replace('/');
        }
        else {
            location.reload();
        }
    });
}
