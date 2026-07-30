import { createOrder, uploadPrintFile } from './supabase.js';

export function initPrintOrderPage() {
    const form = document.getElementById('printOrderForm');
    const status = document.getElementById('printFormStatus');
    if (!form) return;

    function setStatus(message) {
        if (status) status.textContent = message;
    }

    async function uploadFiles(files) {
        if (!files || files.length === 0) return [];
        const uploaded = [];
        for (const file of files) {
            try {
                const path = await uploadPrintFile(file, 'orders');
                uploaded.push({ name: file.name, path });
            } catch (err) {
                console.warn('Upload failed:', err.message);
            }
        }
        return uploaded;
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const button = form.querySelector('button[type="submit"]');
        setStatus('Submitting your order...');
        button.disabled = true;
        button.textContent = 'Sending...';

        try {
            const formData = new FormData(form);
            const files = Array.from(formData.getAll('files')).filter((f) => f instanceof File);
            const uploadedFiles = await uploadFiles(files);
            const selectedColors = formData.getAll('colors');
            const allowGalleryPost = formData.get('allowGalleryPost') === 'on';

            const order = {
                name: (formData.get('name') || '').toString().trim(),
                email: (formData.get('email') || '').toString().trim(),
                phone: (formData.get('phone') || '').toString().trim(),
                service: (formData.get('service') || '').toString().trim(),
                deadline: (formData.get('deadline') || '').toString().trim(),
                notes: (formData.get('notes') || '').toString().trim(),
                source_link: (formData.get('sourceLink') || '').toString().trim(),
                selected_colors: selectedColors,
                allow_gallery_post: allowGalleryPost,
                file_names: uploadedFiles.map((f) => f.name),
                file_paths: uploadedFiles.map((f) => f.path),
                status: 'new',
                created_at: new Date().toISOString()
            };

            const { error } = await createOrder(order);
            if (error) throw error;

            setStatus('Your order was received. We will reach out with a quote within 24hrs.');
            form.reset();
        } catch (error) {
            console.error(error);
            setStatus(error.message || 'The order could not be saved right now.');
        } finally {
            button.disabled = false;
            button.textContent = 'Send Order';
        }
    });
}
