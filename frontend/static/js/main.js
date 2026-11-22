/**
 * Community Renewable Energy Portal - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Auto-dismiss flash alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch (e) {}
    }, 6000);
  });

  // 2. Upvote Post AJAX handler
  const upvoteButtons = document.querySelectorAll('.btn-upvote');
  upvoteButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const postId = this.getAttribute('data-post-id');
      const countSpan = document.getElementById(`upvote-count-${postId}`);

      fetch(`/api/post/${postId}/upvote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (response.redirected) {
          window.location.href = response.url;
          return;
        }
        return response.json();
      })
      .then(data => {
        if (data && data.success) {
          if (countSpan) {
            countSpan.textContent = data.upvotes;
          }
          btn.classList.add('text-success');
          btn.disabled = true;
        }
      })
      .catch(err => console.error('Upvote error:', err));
    });
  });

  // 3. Tip filter in Awareness page
  const tipFilterButtons = document.querySelectorAll('.tip-filter-btn');
  const tipCards = document.querySelectorAll('.tip-card-item');

  tipFilterButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      tipFilterButtons.forEach(b => b.classList.remove('active', 'btn-emerald'));
      tipFilterButtons.forEach(b => b.classList.add('btn-light'));
      
      this.classList.remove('btn-light');
      this.classList.add('active', 'btn-emerald');

      const filter = this.getAttribute('data-filter');
      tipCards.forEach(function (card) {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 4. Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});
