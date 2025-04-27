# Etapa de construcción
FROM node:18 as build

WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias y construir la app
RUN npm install
RUN npm run build

# Etapa de producción (servidor liviano para servir la web)
FROM nginx:alpine

# Copiar archivos construidos al contenedor NGINX
COPY --from=build /app/dist /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
