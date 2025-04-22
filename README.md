# 🧠 Jarvis Web Cortex

**Asistente de voz inteligente y privado**, basado en modelos locales de lenguaje (LLMs), con reconocimiento de voz, autenticación JWT, y despliegue listo para producción.

![Jarvis Web Demo](https://img.shields.io/badge/status-en%20desarrollo-blue)  
![Docker](https://img.shields.io/badge/docker-ready-blue)  
![License](https://img.shields.io/badge/license-MIT-green)

## 🚀 Características

- 🔊 Reconocimiento de voz con **Whisper**
- 🧠 Modelos locales con **Cortex** (LLaMA, Mistral, Phi, etc.)
- 🗣️ Síntesis de voz con **Edge-TTS**
- 🔐 Autenticación con **JWT**
- 📋 Registro de usuarios con contraseña encriptada
- 🧠 Almacenamiento de sesiones en **Redis/PostgreSQL**
- 🌐 Frontend en **React** + Vite
- 🛡️ Despliegue con HTTPS automático (**NGINX + Let's Encrypt**)
- 🐳 Orquestado con **Docker Compose**

## 🧱 Arquitectura General

```
Usuario ↔ Micrófono 🎤
       ↕
[Whisper] → Texto → [Cortex (LLM)] → Respuesta → [edge-tts] → Audio
       ↕                                       ↕
   Frontend (React)                  Backend (FastAPI + Redis + PostgreSQL)
```

## 🛠️ Requisitos

- Docker & Docker Compose
- Dominio personalizado (opcional)
- Servidor Linux (Ubuntu 22.04+ recomendado)
- Puerto 80 y 443 abiertos
- Python 3.11+ si quieres probar localmente

## 📦 Instalación y Despliegue

1. Clona este repositorio:
```bash
git clone https://github.com/webconceptos/Jarvis-Web-Cortex.git
cd Jarvis-Web-Cortex
```

2. Configura tu archivo `.env` para el backend:
```env
DATABASE_URL=postgresql://jarvis:securepass@postgres:5432/jarvisdb
SECRET_KEY=una_clave_ultrasecreta
```

3. Inicia todo con Docker:
```bash
chmod +x deploy.sh
./deploy.sh
```

## ✅ Acceso

Una vez desplegado:

- Accede a `https://tudominio.com`
- Usuario por defecto: `admin`
- Contraseña: `admin123`  
*(puedes cambiarlo con el script `init_db.py`)*

## 🧪 Uso y Desarrollo Local

### Ejecutar Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🧰 Herramientas Usadas

| Tecnología   | Rol                                 |
|--------------|--------------------------------------|
| **FastAPI**  | API backend                         |
| **PostgreSQL** | Base de datos usuarios/sesiones   |
| **Redis**    | Cache y almacenamiento temporal     |
| **React + Vite** | Interfaz de usuario moderna     |
| **Whisper**  | Reconocimiento de voz               |
| **Cortex.so** | LLM local para respuestas IA       |
| **Edge-TTS** | Generación de audio neural          |
| **NGINX + Certbot** | HTTPS automático              |

## 🧾 Licencia

MIT © [Web Conceptos](https://github.com/webconceptos)

## 📬 Contacto

📧 fgarcia@webconceptos.com | ☎️ +51 985 670 257  
🔗 [webconceptos.com](https://webconceptos.com)
=======
<p align="center">
  <img src="jarvis-banner.svg" alt="Jarvis Web Banner" width="100%" />
</p>

