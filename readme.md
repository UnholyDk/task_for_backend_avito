# task_for_backend_avito

## Установка
Сначала надо поставить Docker и docker-compose, если у вас их нет.

Для Windows и Mac Docker Desktop поставляется вместе с docker-compose и ничего больше ставить не надо. Для Linux надо будет воспользоваться инструкцией подлиннее. В любом случае, всё есть по ссылке: https://docs.docker.com/compose/install/.

### Клонируем проект:
```bash
git clone https://github.com/UnholyDk/task_for_backend_avito.git
cd task_for_backend_avito
```

### Теперь соберём сервер и тесты:
```bash
cd src
docker-compose build
```

### После успешной сборки обоих контейнеров их можно запустить: сначала нам надо запустить сервер, потом тесты.

```bash
docker-compose up -d server
docker-compose run pytest -vs
```
http://127.0.0.1/docs  - Тут можно подергать API через UI браузера.

### После того, как тесты прошли, можно выключать сервер до следующего запуска:
```bash
docker-compose down
```
