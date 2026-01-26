FROM node:20-alpine

# Le workspace Angular est ici
WORKDIR /app

# Copier UNIQUEMENT le frontend
COPY frontend/package*.json ./
RUN npm install --silent --no-audit --no-fund

COPY frontend ./

EXPOSE 4200

CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4200"]
