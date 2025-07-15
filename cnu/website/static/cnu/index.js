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
    const feedback = document.querySelector('.form-feedback'); 
    if (contactForm){
    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(contactForm);
        const message = document.getElementById('message');

        if (message.value.trim().length < 10) {
            alert('Mesaj scurt')
            return;
        }

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
    }
        const select = document.getElementById("clasaSelect");
        const downloadSection = document.getElementById("downloadSection");
        const downloadLink = document.getElementById("downloadLink");

        select.addEventListener("change", function () {
            const clasa = select.value;
            console.log(clasa);
            if (clasa){
                const fileUrl = `/media/orare/${clasa}.pdf`;
                fetch(fileUrl, {method: 'HEAD'})
                .then(res =>{
                    if (res.ok){
                        downloadLink.href = fileUrl;
                        downloadSection.classList.remove('d-none');
                    }
                    else{
                        downloadSection.classList.add('d-none');
                        showMessage('⚠️ Orarul pentru această clasă nu a fost găsit sau nu a fost încă adăugat.');
                    }
                })
                .catch(() => {
                    downloadSection.classList.add('d-none');
                    showMessage('⚠️ Eroare la verificarea fișierului.');
                });
            }
            else{
                downloadSection.classList.add('d-none');
            }
        });
});
