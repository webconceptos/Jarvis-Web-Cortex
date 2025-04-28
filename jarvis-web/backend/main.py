from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from passlib.context import CryptContext
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import requests
import tempfile
import edge_tts
import uvicorn
import jwt
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

# Configuraciones generales
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jarvis:securepass@postgres:5432/jarvisdb")
CORTEX_API_URL = os.getenv("CORTEX_API_URL", "http://localhost:5000/api/generate")
VOICE_NAME = os.getenv("VOICE_NAME", "es-MX-DaliaNeural")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


# Modelos Pydantic
class ChatRequest(BaseModel):
    prompt: str
    session_id: str = "default"

class TranscribeResponse(BaseModel):
    text: str

class RegisterRequest(BaseModel):
    username: str
    password: str


# 🔥 /api/register - Registro de nuevos usuarios
@app.post("/api/register")
def register_user(req: RegisterRequest):
    print("📥 /api/register recibido:", req.dict())

    hashed_password = pwd_context.hash(req.password)
    print(f"🔒 Password hasheado para {req.username}: {hashed_password}")

    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, hashed_password)
            VALUES (%s, %s)
            ON CONFLICT (username) DO NOTHING;
        """, (req.username, hashed_password))
        conn.commit()

        cursor.execute("SELECT username FROM users WHERE username = %s", (req.username,))
        user = cursor.fetchone()

        print("✅ Resultado en DB:", user)

        cursor.close()
        conn.close()

        if user:
            return {"message": f"✅ Usuario {req.username} registrado correctamente"}
        else:
            return {"message": f"⚠️ Usuario {req.username} ya existía"}

    except Exception as e:
        print("❌ Error en registro:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# 🔥 /api/token - Login de usuarios
@app.post("/api/token")
def login(username: str = Form(...), password: str = Form(...)):
    print(f"🔎 /api/token login -> Usuario: {username}")

    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT username, hashed_password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        print("🔍 Resultado en DB:", user)

        cursor.close()
        conn.close()

        if not user:
            print("❌ Usuario no encontrado")
            raise HTTPException(status_code=400, detail="Usuario no encontrado")

        password_valid = pwd_context.verify(password, user["hashed_password"])
        print(f"✅ Password válido: {password_valid}")

        if not password_valid:
            raise HTTPException(status_code=400, detail="Contraseña incorrecta")

        token_payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(hours=12)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
        print("🎟️ Token generado:", token)

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print("❌ Error en login:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# 🔥 /chat - Envía mensajes a Cortex
@app.post("/chat")
async def chat(payload: ChatRequest):
    try:
        response = requests.post(CORTEX_API_URL, json={"prompt": payload.prompt, "session_id": payload.session_id})
        response.raise_for_status()
        data = response.json()
        return {"response": data.get("text", "")}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 🔥 /speak - Convierte texto a voz
@app.post("/speak")
async def speak(payload: ChatRequest):
    final_text = payload.prompt.strip()
    if not final_text:
        return JSONResponse(content={"error": "Texto vacío"}, status_code=400)

    try:
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        communicate = edge_tts.Communicate(final_text, voice=VOICE_NAME)
        await communicate.save(audio_path)
        return FileResponse(audio_path, media_type="audio/mpeg", filename="respuesta.mp3")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 🔥 /transcribe - Simulación de transcripción de voz
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return TranscribeResponse(text="Simulación de transcripción.")

# 🔥 Run backend local
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)