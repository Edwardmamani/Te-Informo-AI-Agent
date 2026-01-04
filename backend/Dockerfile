FROM node:24-alpine

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./
COPY tsconfig.json ./
COPY nodemon.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente (se montará como volumen en desarrollo)
COPY . .

# Exponer puerto
EXPOSE 9374

# Comando para desarrollo con nodemon y polling
CMD ["npm", "run", "dev"]

