#!/bin/bash

echo "🚀 Empezando deploy del Backend..."

# Ir a la carpeta del backend
cd jarvis-web/backend || exit

# Instalar dependencias Python (por si acaso quieres usar un entorno virtual en el futuro)
# Nota: Si quieres más adelante, podemos integrar virtualenv, pero por ahora solo reconstruimos

# Volver a raíz
cd ../../

# Parar contenedores anteriores
echo "🛑 Deteniendo contenedores previos..."
docker compose -f docker-compose.prod.yml down

# Lanzar nuevamente
echo "🚀 Reconstruyendo e iniciando contenedores..."
docker compose -f docker-compose.prod.yml up --build -d

echo "✅ Deploy terminado. Backend actualizado y contenedores corriendo."

