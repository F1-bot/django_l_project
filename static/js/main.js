function animateOnScroll() {
    const elements = document.querySelectorAll('.monkey-card-wrapper');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(element => {
        observer.observe(element);
    });
}

function handleFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const rarityFilter = document.getElementById('rarityFilter');

    if (categoryFilter && rarityFilter) {
        const updateFilters = () => {
            const params = new URLSearchParams(window.location.search);

            if (categoryFilter.value) {
                params.set('category', categoryFilter.value);
            } else {
                params.delete('category');
            }

            if (rarityFilter.value) {
                params.set('rarity', rarityFilter.value);
            } else {
                params.delete('rarity');
            }

            window.location.search = params.toString();
        };

        categoryFilter.addEventListener('change', updateFilters);
        rarityFilter.addEventListener('change', updateFilters);
    }
}

function animateCart() {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        cartBadge.addEventListener('animationend', () => {
            cartBadge.classList.remove('shake');
        });
    }
}

function highlightActiveMenu() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    animateOnScroll();
    handleFilters();
    animateCart();
    highlightActiveMenu();

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

async function updateCart(monkeyId, quantity) {
    try {
        const response = await fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                monkey_id: monkeyId,
                quantity: quantity
            })
        });

        const data = await response.json();

        if (data.success) {
            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.textContent = data.cart_count;
                cartBadge.classList.add('shake');
            }

            showNotification('Кошик оновлено!', 'success');
        } else {
            showNotification('Помилка при оновленні кошика', 'error');
        }
    } catch (error) {
        showNotification('Сталася помилка', 'error');
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    }

    .notification.show {
        opacity: 1;
        transform: translateX(0);
    }

    .shake {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;

document.head.appendChild(style);