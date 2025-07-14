document.addEventListener('DOMContentLoaded', function () {
    

    // ----------------------------
    // 1. INITIALIZATION & UTILITIES
    // ----------------------------

    // Utility function to show messages
    function showMessage(message, isSuccess = false) {
        const messageEl = document.createElement('div');
        messageEl.className = 'message';
        messageEl.innerHTML = message;

        if (isSuccess) {
            messageEl.style.backgroundColor = '#d4edda';
            messageEl.style.color = '#155724';
        }

        document.body.appendChild(messageEl);

        setTimeout(() => {
            messageEl.remove();
        }, 7000);
    }

    const contactForm = document.querySelector('.contact-form');
    const feedback = document.querySelector('.form-feedback'); // un div unde afișăm mesajele

    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(contactForm);
        const message = document.getElementById('message');

        // Validare simplă
        if (message.value.trim().length < 10) {
            alert('Mesaj scurt')
            return;
        }

        // Trimitem datele
        fetch(contactForm.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) throw new Error('Eroare la trimitere.');
            return response.json(); 
        })
        .then(data => {
            showMessage(data.message, true);
            contactForm.reset();
        })
        .catch(error => {
            showMessage(error.message || 'Eroare la trimitere.', false);
        });
    });
});
