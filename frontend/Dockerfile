FROM node:24-alpine

WORKDIR /app

# Instalar Electron dependencies (necesarias para el build)
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente (se montará como volumen en desarrollo)
COPY . .

# Exponer puerto si se usa un servidor de desarrollo
EXPOSE 3000

# Comando para desarrollo
CMD ["npm", "run", "dev"]

