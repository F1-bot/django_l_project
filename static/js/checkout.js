document.addEventListener('DOMContentLoaded', function() {
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    const cryptoForm = document.getElementById('crypto-form');
    const cardForm = document.getElementById('card-form');

    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            if (this.value === 'crypto') {
                cryptoForm.classList.remove('d-none');
                cardForm.classList.add('d-none');
            } else {
                cryptoForm.classList.add('d-none');
                cardForm.classList.remove('d-none');
            }
        });
    });

    const form = document.getElementById('checkout-form');

    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });

    const cardNumber = document.querySelector('input[placeholder="1234 5678 9012 3456"]');
    if (cardNumber) {
        cardNumber.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(.{4})/g, '$1 ').trim();
            e.target.value = value;
        });
    }

    const expiry = document.querySelector('input[placeholder="MM/YY"]');
    if (expiry) {
        expiry.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0,2) + '/' + value.slice(2);
            }
            e.target.value = value;
        });
    }
});