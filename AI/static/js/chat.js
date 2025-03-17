let messages = [];
let currentAssistantMessage = null;

function createMessageElement(content, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
    
    // 处理代码块
    const formattedContent = content.replace(/```([\s\S]*?)```/g, (match, code) => {
        return `<pre><code>${code}</code></pre>`;
    }).replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = formattedContent;
    return messageDiv;
}

function addMessage(content, isUser) {
    const messagesContainer = document.getElementById('messages');
    const messageElement = createMessageElement(content, isUser);
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return messageElement;
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 清空输入框
    input.value = '';
    
    // 添加用户消息
    addMessage(message, true);
    messages.push({ role: "user", content: message });
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ messages: messages })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let assistantResponse = '';
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(5));
                        if (data.content) {
                            assistantResponse += data.content;
                            if (!currentAssistantMessage) {
                                currentAssistantMessage = addMessage(assistantResponse, false);
                            } else {
                                currentAssistantMessage.innerHTML = createMessageElement(assistantResponse, false).innerHTML;
                            }
                        }
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                    }
                }
            }
        }
        
        // 保存助手回复
        if (assistantResponse) {
            messages.push({ role: "assistant", content: assistantResponse });
        }
        
        currentAssistantMessage = null;
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('抱歉，发生错误。请稍后重试。', false);
    }
}

// 事件监听器
document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}); 