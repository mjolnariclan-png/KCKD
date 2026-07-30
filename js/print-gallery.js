import { getGalleryPosts, resolveImageUrl } from './supabase.js';

export async function initPrintGalleryPage() {
    const container = document.getElementById('galleryContainer');
    if (!container) return;

    const modal = document.getElementById('printModal');
    const modalImage = document.getElementById('printModalImage');
    const modalTitle = document.getElementById('printModalTitle');
    const modalDescription = document.getElementById('printModalDescription');
    const modalClose = document.getElementById('printModalClose');

    function openModal(imageUrl, title, description) {
        modalImage.src = imageUrl;
        modalTitle.textContent = title;
        modalDescription.textContent = description;
        modal.classList.add('active');
    }

    function closeModal() {
        modal.classList.remove('active');
    }

    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }

    try {
        const posts = await getGalleryPosts();

        if (!posts || posts.length === 0) {
            container.innerHTML = '<p style="color: var(--text-secondary); grid-column: 1/-1; text-align: center;">Gallery coming soon.</p>';
            return;
        }

        const postsWithUrls = await Promise.all(posts.map(async (post) => ({
            ...post,
            resolved_image_url: await resolveImageUrl(post.image_url)
        })));

        container.innerHTML = postsWithUrls.map((post, i) => `
            <article class="gallery-card" data-index="${i}">
                <img src="${post.resolved_image_url || post.image_url}" alt="${post.title}" onerror="this.style.display='none'">
                <h3>${post.title}</h3>
                <p>${post.description || ''}</p>
            </article>
        `).join('');

        container.querySelectorAll('.gallery-card').forEach((card) => {
            card.addEventListener('click', () => {
                const post = postsWithUrls[Number(card.dataset.index)];
                openModal(post.resolved_image_url || post.image_url, post.title, post.description || '');
            });
        });
    } catch (error) {
        console.error('Error loading gallery:', error);
        container.innerHTML = '<p style="color: var(--text-secondary); grid-column: 1/-1;">Error loading gallery.</p>';
    }
}
