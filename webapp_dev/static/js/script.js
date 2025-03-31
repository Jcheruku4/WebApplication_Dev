const deleteAllBtn = document.querySelector('.delete-all-btn');
if (deleteAllBtn) {
    deleteAllBtn.addEventListener('click', function(event) {
        if (!confirm('Are you sure you want to delete all expenditures?')) {
            event.preventDefault();
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.textContent = '↑';
    scrollToTopBtn.style.position = 'fixed';
    scrollToTopBtn.style.bottom = '20px';
    scrollToTopBtn.style.right = '20px';
    scrollToTopBtn.style.backgroundColor = '#002366';
    scrollToTopBtn.style.color = 'white';
    scrollToTopBtn.style.padding = '10px';
    scrollToTopBtn.style.borderRadius = '5px';
    scrollToTopBtn.style.cursor = 'pointer';
    scrollToTopBtn.style.display = 'none';
    scrollToTopBtn.style.transition = 'all 0.3s ease';
    document.body.appendChild(scrollToTopBtn);

    window.addEventListener('scroll', function() {
        scrollToTopBtn.style.display = window.scrollY > 200 ? 'block' : 'none';
    });

    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
