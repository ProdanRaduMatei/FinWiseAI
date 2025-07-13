# Use official Node image
FROM node:20-alpine

# Create app dir
WORKDIR /app

# Install deps
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy source
COPY . .

# Start the app
CMD ["npm", "start"]