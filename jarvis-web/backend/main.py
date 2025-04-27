from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import requests
import os
import tempfile
import edge_tts
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

# Cargar variables de entorno si existen
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


# Configuración
CORTEX_API_URL = os.getenv("CORTEX_API_URL", "http://localhost:5000/api/generate")  # Ajusta puerto si es diferente
VOICE_NAME = os.getenv("VOICE_NAME", "es-MX-DaliaNeural")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jarvis:securepass@postgres:5432/jarvisdb")

# Modelos de entrada
class ChatRequest(BaseModel):
    prompt: str
    session_id: str = "default"

class TranscribeResponse(BaseModel):
    text: str

# Endpoint para enviar texto a Cortex y recibir respuesta
@app.post("/chat")
async def chat(payload: ChatRequest):
    try:
        response = requests.post(CORTEX_API_URL, json={
            "prompt": payload.prompt,
            "session_id": payload.session_id
        })
        response.raise_for_status()
        data = response.json()
        return {"response": data.get("text", "")}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint para convertir texto en audio usando edge-tts
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

# Endpoint para simular transcripción (puedes conectar Whisper local si quieres)
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Simula respuesta de texto fijo
    return TranscribeResponse(text="Simulación de transcripción.")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Definimos router si luego quieres modularizar
router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str


@app.post("/api/register")
def register_user(req: RegisterRequest):
    print("📥 Recibido en /api/register:", req.dict())  # 👈 Debug entrada JSON

    hashed_password = pwd_context.hash(req.password)
    print(f"🔒 Password hasheado para {req.username}:", hashed_password)  # 👈 Debug password

    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (req.username, hashed_password)
        )
        conn.commit()

        cursor.execute("SELECT username FROM users WHERE username = %s", (req.username,))
        result = cursor.fetchone()
        print("✅ Resultado en la base de datos:", result)  # 👈 Debug post inserción

        cursor.close()
        conn.close()

        if result:
            return {"message": f"✅ Usuario {req.username} registrado correctamente"}
        else:
            return {"message": f"⚠️ Usuario {req.username} ya existía"}

    except Exception as e:
        print("❌ Error al registrar:", str(e))  # 👈 Debug en error
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)

# Nueva función para autenticar usuario
def verify_user(username: str, password: str):
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT username, hashed_password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and pwd_context.verify(password, user["hashed_password"]):
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de login (token)
@app.post("/api/token")
def login(username: str = Form(...), password: str = Form(...)):
    print(f"🔎 Intento de login -> Usuario: {username}")  # 👈 Debug usuario recibido

    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, hashed_password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        print("🔍 Resultado de búsqueda en DB:", user)  # 👈 Debug resultado DB

        cursor.close()
        conn.close()

        if not user:
            print("❌ Usuario no encontrado")
            raise HTTPException(status_code=400, detail="Usuario no encontrado")

        password_valid = pwd_context.verify(password, user["hashed_password"])
        print(f"✅ Password válido: {password_valid}")  # 👈 Debug validación de password

        if not password_valid:
            raise HTTPException(status_code=400, detail="Contraseña incorrecta")

        token_payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(hours=12)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
        print("🎟️ Token generado:", token)  # 👈 Debug token generado

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print("❌ Error en login:", str(e))  # 👈 Debug en error
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
