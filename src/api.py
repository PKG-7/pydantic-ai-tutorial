from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

from basic import agent1
from structured_response import agent2
from tools import agent, CustomerDetails

app = FastAPI(title="LLaMA API", description="API для взаимодействия с разными типами LLaMA агентов")

# Базовые модели запросов и ответов
class BasicRequest(BaseModel):
    message: str

class BasicResponse(BaseModel):
    response: str

class StructuredRequest(BaseModel):
    message: str

class ShippingRequest(BaseModel):
    message: str
    customer_id: str
    name: str
    email: str

@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Чат с ботом</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                display: flex;
                min-height: 100vh;
                position: relative;
            }
            .main-container {
                flex: 0 1 800px;
                margin: 0 auto;
                padding: 0 20px;
                box-sizing: border-box;
                width: 100%;
                max-width: 800px;
                transition: all 0.3s ease;
            }
            .sidebar {
                width: 300px;
                padding: 20px;
                background-color: white;
                border-left: 1px solid #ddd;
                position: fixed;
                right: 0;
                top: 0;
                bottom: 0;
                overflow-y: auto;
                display: none;
                transition: all 0.3s ease;
                z-index: 10;
                box-shadow: -2px 0 5px rgba(0,0,0,0.1);
            }
            .parameter {
                margin-bottom: 15px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
            .parameter-label {
                font-weight: bold;
                color: #2196f3;
                margin-bottom: 5px;
            }
            .parameter-value {
                word-break: break-word;
            }
            #chat-container {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 20px;
                margin-bottom: 20px;
                background-color: white;
                border-radius: 5px;
            }
            .message {
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 5px;
            }
            .user-message {
                background-color: #e3f2fd;
                margin-left: 20%;
            }
            .bot-message {
                background-color: #f5f5f5;
                margin-right: 20%;
            }
            #input-container {
                display: flex;
                gap: 10px;
            }
            #message-input {
                flex-grow: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #1976d2;
            }
            select {
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        </style>
    </head>
    <body>
        <div class="main-container">
            <h1>Чат с ботом</h1>
            
            <select id="bot-type" onchange="handleBotTypeChange()">
                <option value="basic">Базовый бот</option>
                <option value="structured">Структурированный бот</option>
                <option value="shipping">Бот доставки</option>
            </select>

            <div id="chat-container"></div>
            
            <div id="input-container">
                <input type="text" id="message-input" placeholder="Введите сообщение...">
                <button onclick="sendMessage()">Отправить</button>
            </div>
        </div>

        <div id="sidebar" class="sidebar">
            <h2>Параметры ответа</h2>
            <div id="parameters-container"></div>
        </div>

        <script>
            const chatContainer = document.getElementById('chat-container');
            const messageInput = document.getElementById('message-input');
            const botType = document.getElementById('bot-type');
            const sidebar = document.getElementById('sidebar');
            const parametersContainer = document.getElementById('parameters-container');

            function handleBotTypeChange() {
                sidebar.style.display = botType.value === 'structured' ? 'block' : 'none';
            }

            function addParameter(label, value) {
                const paramDiv = document.createElement('div');
                paramDiv.className = 'parameter';
                
                const labelDiv = document.createElement('div');
                labelDiv.className = 'parameter-label';
                labelDiv.textContent = label;
                
                const valueDiv = document.createElement('div');
                valueDiv.className = 'parameter-value';
                valueDiv.textContent = value;
                
                paramDiv.appendChild(labelDiv);
                paramDiv.appendChild(valueDiv);
                parametersContainer.appendChild(paramDiv);
            }

            function updateParameters(data) {
                parametersContainer.innerHTML = '';
                if (data.needs_escalation !== undefined) {
                    addParameter('Требует эскалации', data.needs_escalation);
                }
                if (data.follow_up_required !== undefined) {
                    addParameter('Требует следующих действий', data.follow_up_required);
                }
                if (data.is_offensive !== undefined) {
                    addParameter('Содержит оскорбления', data.is_offensive);
                }
                if (data.sentiment) {
                    addParameter('Тональность', data.sentiment);
                }
                if (data.response) {
                    addParameter('Ответ', data.response);
                }
            }

            function addMessage(message, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                messageDiv.textContent = message;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                messageInput.value = '';

                let endpoint = '/basic';
                let body = { message };

                switch(botType.value) {
                    case 'basic':
                        endpoint = '/basic';
                        break;
                    case 'structured':
                        endpoint = '/structured';
                        break;
                    case 'shipping':
                        endpoint = '/shipping';
                        body = {
                            message,
                            customer_id: "1",
                            name: "Test User",
                            email: "test@example.com"
                        };
                        break;
                }

                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(body)
                    });

                    const data = await response.json();
                    let botResponse = data.response;
                    
                    if (botType.value === 'structured') {
                        updateParameters(data);
                        botResponse = data.response || JSON.stringify(data, null, 2);
                    } else if (typeof data === 'object' && !data.response) {
                        botResponse = JSON.stringify(data, null, 2);
                    }

                    addMessage(botResponse, false);
                } catch (error) {
                    addMessage('Произошла ошибка: ' + error.message, false);
                }
            }

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Инициализация отображения сайдбара
            handleBotTypeChange();
        </script>
    </body>
    </html>
    """

@app.post("/basic", response_model=BasicResponse)
async def basic_chat(request: BasicRequest):
    """Простой чат без дополнительных параметров"""
    try:
        response = agent1.run_sync(request.message)
        return BasicResponse(response=str(response.data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/structured")
async def structured_chat(request: StructuredRequest):
    """Чат со структурированным ответом"""
    try:
        response = agent2.run_sync(request.message)
        return response.data.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/shipping")
async def shipping_chat(request: ShippingRequest):
    """Чат с информацией о доставке"""
    try:
        customer = CustomerDetails(
            customer_id=request.customer_id,
            name=request.name,
            email=request.email
        )
        response = agent.run_sync(
            user_prompt=request.message,
            deps=customer
        )
        return response.data.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 