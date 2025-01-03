### DOCKER 🙁/😃
### 🙁 Dockerfile:

```Dockerfile
FROM ubuntu:latest

RUN apt-get update && apt-get install -y nodejs npm
RUN mkdir /app
RUN cd /app

COPY . /app
RUN npm install

CMD ["npm", "start"]
```

#### Ошибки:

1. **Использование полного образа (`ubuntu:latest`)**
    - Полный образ занимает много места(контейнеры должны быть легковесными)
    - Использую `node:16-alpine`. Занимает меньше места и используют только необходимое

2. **Необъединение`RUN`**
    - Каждый `RUN` создает новый слой `=>` больше места занимает
    - Я объединил `RUN`. Меньше лишних слоев

3. **Неудаление кеша после установки зависимостей**
    - Кеш остается в контейнере и занимает память
    - Очищаю кеш **в той же строке** ``RUN npm install --production && npm cache clean --force``

4. **Запуск приложения от пользователя `root`**
    - **БЕЗОПАСНОСТЬ!**
    - Создаю нового пользователя и запускаю от его прав

   ```Dockerfile
   RUN adduser -D user_dock
   USER user_dock
   ```
---

### 😃 Dockerfile:

```Dockerfile
# Этап сборки проекта
FROM node:16-alpine AS build

WORKDIR /app

# Сначала копируем только package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install --production && npm cache clean --force

# Копируем проект и собираем его
COPY . .
RUN npm run build

# Финальный образ для запуска
FROM node:16-alpine

WORKDIR /app
COPY --from=build /app .

# Добавляем пользователя для повышения безопасности
RUN adduser -D user_dock
USER user_dock

EXPOSE 3000
CMD ["npm", "start"]
```

---

### Плохие практики по работе с контейнерами

1. **Создание слишком больших Docker-образов**

Если получается большой докер образ лучше разбить на несколько.

2. **Хранение данных внутри контейнера**

При удалении контейнера все данные потеряются

3. **Ручная настройка чего-то в контейнере**

Контейнер должен быть автоматизирован и собираться автоматически
(предыдущий пункт)

4. **Запуск ``root``**

Любой у кого есть доступ к контейнеру может все поломать либо украсть данные

5. **Не ограничивать ресурсы**

Комп горит/все висит/нет памяти?

``=>`` **проверь запущенные контейнеры!**

Чтобы не возникало таких проблем нужно ограничивать доступ к памяти и CPU

---

### Вывод
Docker - классная штука, но нужно **уметь** пользоваться!

# 🦒
