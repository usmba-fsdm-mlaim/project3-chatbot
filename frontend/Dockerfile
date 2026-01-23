# Étape 1 : Construction
# ON PASSE À LA VERSION 20-alpine
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Étape 2 : Production
# ON PASSE À LA VERSION 20-alpine ICI AUSSI
FROM node:20-alpine AS runner
WORKDIR /app

# Copie des fichiers construits
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]