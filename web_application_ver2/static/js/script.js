document.querySelectorAll('button').forEach(b => {
    b.addEventListener('mouseover', () => {
        b.style.transform = "scale(1.05)";
        b.style.boxShadow = "0px 4px 12px rgba(0, 0, 0, 0.2)";
    });
    b.addEventListener('mouseout', () => {
        b.style.transform = "scale(1)";
        b.style.boxShadow = "none";
    });
});
document.querySelectorAll('form').forEach(f => {
    f.addEventListener('submit', e => {
        e.preventDefault();
        f.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => f.submit(), 300);
    });
});
