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