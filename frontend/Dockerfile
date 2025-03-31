# Stage 1: Build the Vite app
FROM node:20-alpine AS build-stage

WORKDIR /frontend
COPY package*.json ./
RUN npm install
# Set the working directory inside the container
COPY . .

RUN npm run build

# Stage 2: Serve the built app
FROM node:20-alpine

WORKDIR /app
COPY --from=builder /app/dist ./

EXPOSE 3000
CMD ["npx", "serve", "-p", "3000"]
