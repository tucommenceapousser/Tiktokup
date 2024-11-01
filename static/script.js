    // Palette des couleurs fluo
    const colors = [
        "var(--primary)",
        "var(--secondary)",
        "var(--highlight)",
        "var(--yellow)",
        "var(--green)",
        "var(--purple)",
        "var(--cyan)",
        "var(--border-fluo)",
        "var(--border-alt1)",
        "var(--border-alt2)",
        "var(--border-alt3)",
        "var(--light)",
        "var(--dark)"
    ];

    // Fonction pour appliquer une couleur aléatoire
    function applyRandomColors() {
        // Applique des couleurs aléatoires aux éléments spécifiques
        document.querySelectorAll('h2, .btn, video, img, .sidebar, .transcription-box, .footer, .form-container, textarea, input[type="text"]').forEach(element => {
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            element.style.borderColor = randomColor;
            element.style.boxShadow = `0 0 10px ${randomColor}`;
            element.style.color = randomColor;
        });

        // Ajoute un effet de survol avec une couleur aléatoire sur les boutons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('mouseover', () => {
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                button.style.backgroundColor = randomColor;
                button.style.boxShadow = `0 0 10px ${randomColor}`;
            });
            button.addEventListener('mouseout', () => {
                button.style.backgroundColor = "var(--primary)";
            });
        });
    }

    // Appliquez les couleurs lors du chargement de la page
    window.addEventListener('DOMContentLoaded', applyRandomColors);
