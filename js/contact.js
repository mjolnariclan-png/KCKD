import { supabase, updateNavbar } from './app.js';

export function initContactPage() {
    const form = document.getElementById('deckRequestForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = form.querySelector('input[type="email"]').value;
        const interest = form.querySelector('select').value;
        const message = form.querySelector('textarea').value;
        
        console.log('Submitting:', { email, interest, message });
        
        const { data, error } = await supabase.from('contact_requests').insert([{
            email: email,
            interest: interest,
            message: message,
            created_at: new Date().toISOString()
        }]);
        
        if (error) {
            console.error('Insert error:', error);
            alert('Error: ' + error.message);
        } else {
            console.log('Inserted:', data);
            alert('Request sent. We will be in touch.');
            form.reset();
        }
    });
}

export function initQAForm() {
    const askForm = document.getElementById('askForm');
    if (!askForm) return;
    
    askForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = askForm.querySelector('input[type="text"]').value;
        
        const { data, error } = await supabase.from('qa_questions').insert([{
            question: question,
            status: 'pending',
            created_at: new Date().toISOString()
        }]);
        
        if (error) {
            console.error('Q&A error:', error);
            alert('Error: ' + error.message);
        } else {
            alert('Question submitted. Answers appear when approved.');
            askForm.reset();
        }
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    console.log('DOM ready - contact.js');
    updateNavbar();
    initContactPage();
    initQAForm();
});