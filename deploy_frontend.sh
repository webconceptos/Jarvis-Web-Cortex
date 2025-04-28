#!/bin/bash

echo "🚀 Empezando build de Frontend..."

# Ir a la carpeta del frontend
cd jarvis-web/frontend || exit

# Instalar dependencias (por si falta algo)
echo "📦 Instalando dependencias..."
npm install

# Hacer build de producción
echo "🏗️ Construyendo frontend (npm run build)..."
npm run build

# Volver a raíz
cd ../../

# Parar contenedores anteriores
echo "🛑 Deteniendo contenedores previos..."
docker compose -f docker-compose.prod.yml down

# Lanzar nuevamente
echo "🚀 Reconstruyendo e iniciando contenedores..."
docker compose -f docker-compose.prod.yml up --build -d

echo "✅ Deploy terminado. Frontend actualizado y contenedores corriendo."
