document.addEventListener('DOMContentLoaded', function () {

    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault(); 

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            if (name === '' || email === '' || message === '') {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Please fill out all the fields!',
                });
                return;
            }

            const formData = {
                name: name,
                email: email,
                message: message,
            };

            axios.post('/submit_contact', formData)
                .then(function (response) {
          
                    Swal.fire({
                        icon: 'success',
                        title: 'Thank you!',
                        text: 'Your message has been sent successfully.',
                        timer: 3000,
                        showConfirmButton: false,
                    });

                    contactForm.reset();
                })
                .catch(function (error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Submission Failed',
                        text: 'There was an issue submitting your message. Please try again later.',
                    });
                    console.error(error);
                });
        });
    }

    const searchForm = document.querySelector('.search-form');

    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();  

            let query = document.querySelector('input[name="query"]').value;

            window.location.href = `/search?query=${encodeURIComponent(query)}`;
        });
    }
});