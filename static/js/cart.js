function updateQuantity(itemId, change) {
    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ change: change })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const quantitySpan = document.querySelector(`.cart-item[data-item-id="${itemId}"] .quantity-controls span`);
            quantitySpan.textContent = data.quantity;

            const itemSubtotal = document.querySelector(`.cart-item[data-item-id="${itemId}"] .price`);
            itemSubtotal.textContent = `${data.item_subtotal.toFixed(2)} ETH`;

            document.querySelector('.subtotal').textContent = `${data.subtotal.toFixed(2)} ETH`;
            document.querySelector('.fee').textContent = `${data.fee.toFixed(2)} ETH`;
            document.querySelector('.total-price').textContent = `${data.total.toFixed(2)} ETH`;

            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.textContent = data.quantity;
            }
        }
    });
}

function removeItem(itemId) {
    if (confirm('Ви впевнені, що хочете видалити цей товар?')) {
        fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const item = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                item.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    location.reload();
                }, 300);
            }
        });
    }
}