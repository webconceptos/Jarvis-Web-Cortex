# Jarvis Web v2 - Asistente de Voz Inteligente

Este proyecto implementa un asistente web con reconocimiento y síntesis de voz, autenticación JWT, registro de usuarios, sesiones persistentes, y despliegue en producción con HTTPS y PostgreSQL.

## Características
- 🔐 Login y registro con JWT
- 🧠 Modelos locales con Cortex y Whisper
- 📦 Backend FastAPI + PostgreSQL + Redis
- 🌐 Frontend React moderno
- 🛡️ HTTPS + NGINX + Certbot (Let's Encrypt)

## Estructura
```
jarvis-web/
├── backend/
├── frontend/
├── nginx/
└── docker-compose.prod.yml
```

## Despliegue
1. Clona el repo y ejecuta `./deploy.sh`
2. Accede al dominio configurado con HTTPS
3. Usa el usuario admin (admin/admin123) o registra uno nuevo

## Requisitos
- Docker y Docker Compose
- Dominio propio apuntando a tu IP
- PostgreSQL y Redis como servicios
