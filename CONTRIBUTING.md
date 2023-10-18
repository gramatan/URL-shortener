# Вклад в проект "Shift Rest"

## Введение

Этот файл предназначен для разработчиков, которые хотят внести свой вклад в проект. Здесь вы найдете информацию о том, как настроить проект для разработки, структуру проекта, а также рекомендации и требования по стилю кода.

## Сетап для разработки

1. Клонируйте репозиторий:
```
git clone [ссылка на ВАШ форк этого репозитория]
```

2. Перейдите в директорию проекта:
```
cd имя проекта
```

3. Установите все зависимости с помощью [Poetry](https://python-poetry.org/):
```
poetry install
```

4. Активация виртуального окружение для запуска приложения или flake8, mypy и pytest:
```
poetry shell
```

5. Запуск приложения:

```shell
docker build -t gran_url .
docker run -d -p 24501:24501 --name url_shortener gran_url
```


## Шаги для разворачивания в кубернетис

1. Примените конфигурации для хранилища данных:
  ```
   kubectl apply -f k8s/volume.yaml
  ```

2. Добавьте секреты и константы:
  ```
  kubectl apply -f k8s/secret.yaml
  kubectl apply -f k8s/configmap.yaml
  ```

3. Деплоим сервисы:
  ```
  kubectl apply -f k8s/deployment_cc_auth.yaml
  kubectl apply -f k8s/deployment_cc_balance.yaml
  kubectl apply -f k8s/deployment_cc_verify.yaml
  ```

4. Деплоим сервисы:
  ```
  kubectl apply -f k8s/service_cc_auth.yaml
  kubectl apply -f k8s/service_cc_balance.yaml
  ```

5. Джобом накатываем миграции(но так как у нас нет доступа к джобам - мы сделаем это с помощью одноразового пода.):
  ```
  kubectl apply -f k8s/job_alembic.yaml
  ```

  Проверка статуса:
  ```
  kubectl get pods
  kubectl logs <pod_name>
  ```

## Структура проекта

Единый для всех сервисов конфигурационный файл:
- `config/`[config.py](config%2Fconfig.py) : Файл с константами для приложения.
  - APP_PORT : Порт, на котором будет запущено приложение.
  - HEALTHZ_PREFIX : Префикс для healthcheck эндпоинта.

- [main_short.py](main_short.py): Основной файл приложения.

- `src` : Исходный код проекта.
  - [database](src%2Fdatabase) : Файлы для работы с базой данных.
  - [repositories](credit_card_auth%2Fsrc%2Frepositories) : Файлы с репозиториями для работы с базой данных.
  - [routers](credit_card_auth%2Fsrc%2Frouters) : Файлы с описанием эндпоинтов.
  - [schemas](credit_card_auth%2Fsrc%2Fschemas) : Схемы данных.
  - [services](credit_card_auth%2Fsrc%2Fservices) : Файлы с сервисами для работы с приложением.

- `tests`: Тесты сервиса.
  - `unit`: Юнит тесты разбиты по файлам в соответствии со структурой проекта.
  - `integration`: Сценарий интеграционных тестов из задания в одном файле + тесты API.

  #### БД:
 TBD

### Общие файлы
- [alembic](alembic) : Скрипты для миграции.
- [CHANGELOG.md](CHANGELOG.md) : История изменений проекта.
- `CONTRIBUTING.md` : Рекомендации для контрибьюторов (вы сейчас читаете его).
- [README.md](README.md) : Описание проекта.

## Процесс внесения изменений

1. Создайте форк проекта на GitLab.
2. Клонируйте ваш форк на свой локальный компьютер.
3. Создайте новую ветку для ваших изменений.
4. Внесите необходимые изменения и убедитесь, что все тесты проходят.
5. Отправьте ваши изменения на проверку в виде pull/merge request в основной репозиторий.

## Кодовые стандарты и соглашения

Мы следуем стандартам кодирования, предложенным `wemake-python-styleguide`, а также проверяем типы с помощью `mypy`. Убедитесь, что ваш код соответствует этим требованиям перед отправкой на ревью.

## Процесс ревью

Все изменения в проекте проходят процесс проверки другими разработчиками. Ваш код будет проверен на соответствие стандартам качества и функциональности.

## Полезные ссылки

- [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide)
- [mypy](http://mypy-lang.org/)