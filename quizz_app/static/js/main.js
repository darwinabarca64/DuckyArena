// Main JavaScript file for quizz app

document.addEventListener('DOMContentLoaded', function() {
    console.log('QuizzMaster app loaded!');
    
    // Add smooth transitions
    const cards = document.querySelectorAll('.quiz-card, .question-card, .answer-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});
