document.addEventListener('DOMContentLoaded', function () {
    const deleteAllBtn = document.querySelector('.delete-all-btn');
    const modal = document.getElementById('delete-all-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete');
    const cancelDeleteBtn = document.getElementById('cancel-delete');
    if (deleteAllBtn) {
        deleteAllBtn.addEventListener('click', function (event) {
            event.preventDefault();
            modal.style.display = 'flex';
        });
    }
    confirmDeleteBtn.addEventListener('click', function () {
        modal.style.display = 'none';
        document.querySelector('form[action="/delete_all"]').submit();
    });
    cancelDeleteBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.textContent = '↑';
    scrollToTopBtn.classList.add('scroll-to-top-btn');
    document.body.appendChild(scrollToTopBtn);
    window.addEventListener('scroll', function () {
        scrollToTopBtn.style.display = window.scrollY > 200 ? 'block' : 'none';
    });
    scrollToTopBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
