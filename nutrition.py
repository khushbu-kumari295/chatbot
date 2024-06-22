from openai import OpenAI
from fastapi import FastAPI, Form, Request, WebSocket
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

# Initialize OpenAI client
client = OpenAI()

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
chat_responses = []

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

# Chat log to maintain conversation history
chat_log = [
    {
        'role': 'system',
        'content': 'You are a helpful nutrition assistant. You provide accurate information about nutrition, '
                   'Your role is to provide accurate information about nutrition, '
                   'dietary advice,'
                   'meal planning, and healthy eating habits,'
                   'Any questions other then nutrition or health should be responded with "I\'m sorry, but I can only assist with questions about nutrition."'
    }
]




@app.websocket("/ws")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_input = await websocket.receive_text()
        chat_log.append({'role': 'user', 'content': user_input})
        try:
            response = client.chat.completions.create(
                model='gpt-4',
                messages=chat_log,
                temperature=0.6,
                stream=True
            )
            ai_response = ''
            for chunk in response:
                #if 'choices' in chunk and 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                if chunk.choices[0].delta.content is not None:
                    ai_response += chunk.choices[0].delta.content
                    await websocket.send_text(chunk.choices[0].delta.content)
            chat_log.append({'role': 'assistant', 'content': ai_response})
        except Exception as e:
            await websocket.send_text(f'Error: {str(e)}')
            break


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({'role': 'user', 'content': user_input})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log,
            temperature=0.6
        )
        bot_response = response.choices[0].message.content
        chat_log.append({'role': 'assistant', 'content': bot_response})
        chat_responses.append(bot_response)

    except Exception as e:
        bot_response = f'Error: {str(e)}'
        chat_log.append({'role': 'assistant', 'content': bot_response})

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_log})


@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input: Annotated[str, Form()]):
    try:
        response = client.images.generate(
            prompt=user_input,
            n=1,
            size="256x256"
        )
        image_url = response.data[0].url
    except Exception as e:
        image_url = f'Error: {str(e)}'
    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})
