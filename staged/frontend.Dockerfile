FROM node:22-alpine as build-stage

RUN apk add --no-cache git

ARG FRONTEND_GIT_URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /app

RUN git clone --depth 1 ${FRONTEND_GIT_URL} .

RUN npm install
RUN npx vite build

# === ЭТАП 2: Nginx ===
FROM nginx:alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

