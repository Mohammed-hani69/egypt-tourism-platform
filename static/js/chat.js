class ChatManager {
    constructor(containerId, currentUserId) {
        this.container = document.getElementById(containerId);
        this.currentUserId = currentUserId;
        this.setupEventSource();
        this.setupMessageForm();
    }

    setupEventSource() {
        const chatId = window.location.pathname.split('/').pop();
        this.eventSource = new EventSource(`/chat/events/${chatId}`);
        
        this.eventSource.onmessage = (event) => {
            const messageData = JSON.parse(event.data);
            this.addMessage(messageData);
        };
    }

    setupMessageForm() {
        const form = document.querySelector('.message-form');
        const input = form.querySelector('.message-input');
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!input.value.trim()) return;

            try {
                const response = await fetch(window.location.href, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        content: input.value,
                        csrf_token: csrfToken
                    })
                });
                
                if (response.ok) {
                    input.value = '';
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        });
    }

    addMessage(messageData) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message-wrapper');
        
        if (messageData.sender_id === this.currentUserId) {
            messageElement.classList.add('my-message');
        } else {
            messageElement.classList.add('other-message');
        }
        
        messageElement.innerHTML = `
            <div class="message-bubble">
                <div class="message-text">${messageData.message}</div>
                <div class="message-meta">
                    <span class="message-time">${new Date(messageData.timestamp).toLocaleTimeString('ar-EG')}</span>
                </div>
            </div>
        `;
        
        this.container.appendChild(messageElement);
        this.container.scrollTop = this.container.scrollHeight;
    }
}
