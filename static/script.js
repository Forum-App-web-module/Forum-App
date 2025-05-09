// Функция за обработка на гласуването
function vote(type, button) {
    const voteCountElement = button.parentElement.querySelector('.vote-count');
    let currentVotes = parseInt(voteCountElement.innerText);

    // Ако е натиснат upvote бутон
    if (type === 'up') {
        currentVotes++;
    }
    // Ако е натиснат downvote бутон
    else if (type === 'down') {
        currentVotes--;
    }

    // Обновяваме брояча на гласовете
    voteCountElement.innerText = currentVotes;
}

// или изпращане чрез API заявка, можеш да използваш JavaScript

document.querySelector('.send-message-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const recipient = document.querySelector('#recipient').value;
    const message = document.querySelector('#message').value;

    // Изпращане на съобщението към сървъра чрез AJAX или Fetch
    fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            recipient: recipient,
            message: message
        })
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Съобщението е изпратено успешно!');
              // Може да изчистиш полетата или да актуализираш UI-то
          } else {
              alert('Грешка при изпращането на съобщението.');
          }
      });
});

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.choose-best');
  
    buttons.forEach(button => {
      button.addEventListener('click', () => {
        document.querySelectorAll('.reply').forEach(reply => {
          reply.classList.remove('best-reply');
        });
  
        const replyId = button.getAttribute('data-reply-id');
        const selectedReply = document.getElementById('reply-' + replyId);
        selectedReply.classList.add('best-reply');
      });
    });
  });