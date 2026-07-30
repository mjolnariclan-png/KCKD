import { getReviews, addReview } from './supabase.js';

function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, (m) => map[m]);
}

export function initPrintReviewsPage() {
    const form = document.getElementById('printReviewForm');
    const starRating = document.getElementById('printStarRating');
    const ratingInput = document.getElementById('printReviewRating');
    const statusEl = document.getElementById('printReviewStatus');
    const reviewsList = document.getElementById('printReviewsList');
    if (!form) return;

    let selectedRating = 0;
    const stars = starRating.querySelectorAll('.star');

    function updateStarDisplay() {
        stars.forEach((s) => {
            const active = parseInt(s.dataset.rating) <= selectedRating;
            s.classList.toggle('active', active);
        });
    }

    stars.forEach((star) => {
        star.addEventListener('click', () => {
            selectedRating = parseInt(star.dataset.rating);
            ratingInput.value = selectedRating;
            updateStarDisplay();
        });
    });

    function setStatus(message) {
        if (statusEl) statusEl.textContent = message;
    }

    async function loadReviews() {
        try {
            const reviews = await getReviews();

            if (!reviews || reviews.length === 0) {
                reviewsList.innerHTML = '<div class="no-reviews">No reviews yet. Be the first to leave one!</div>';
                return;
            }

            reviewsList.innerHTML = reviews.map((review) => `
                <div class="review-card">
                    <div class="review-header">
                        <h4 class="review-name">${escapeHtml(review.customer_name)}</h4>
                        <div class="review-stars">${'⭐'.repeat(review.rating)}</div>
                    </div>
                    <div class="review-date">${new Date(review.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</div>
                    <p class="review-text">${escapeHtml(review.review_text)}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading reviews:', error);
            reviewsList.innerHTML = '<div class="no-reviews">Unable to load reviews.</div>';
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (selectedRating === 0) {
            setStatus('Please select a rating.');
            return;
        }

        const name = document.getElementById('printReviewName').value.trim();
        const reviewText = document.getElementById('printReviewText').value.trim();

        if (!name || !reviewText) {
            setStatus('Please fill in all fields.');
            return;
        }

        const button = form.querySelector('button[type="submit"]');
        button.disabled = true;
        button.textContent = 'Submitting...';

        try {
            const { error } = await addReview({
                customer_name: name,
                rating: selectedRating,
                review_text: reviewText,
                created_at: new Date().toISOString()
            });

            if (error) throw error;

            setStatus('✓ Thank you for your review!');
            form.reset();
            selectedRating = 0;
            ratingInput.value = 0;
            updateStarDisplay();
            await loadReviews();
        } catch (error) {
            console.error('Error submitting review:', error);
            setStatus('Error submitting review. Please try again.');
        } finally {
            button.disabled = false;
            button.textContent = 'Submit Review';
        }
    });

    loadReviews();
}
