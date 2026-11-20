# VRVR.Tube API/UI Autotests

Автоматизированные API/UI-тесты для https://dev.vrvr-dev.ru

Тесты написаны на Python с использованием Pytest, requests (API) и Playwright (UI).

## Что тестируется
Проверяются основные сценарии работы с каналами:
- авторизация;
- создание канала;
- получение списка каналов;
- получение канала по id;
- изменение Free Play Mode;
- удаление канала;
- создание раздела контента в канале;
- удаление раздела контента в канале;
- изменение порядка разделов в канале;
- негативные проверки.

## Организация тестов
Используются общие `pytest`-фикстуры из `tests/conftest.py`:
- `login` - авторизация перед тестом;
- `channel` - создание тестового канала;
- `cleanup` - удаление созданных каналов после теста.

Это даёт единый стиль setup/teardown и уменьшает дублирование кода в тестах.

Для UI-тестов используются отдельные фикстуры из `tests_ui/conftest.py`:
- `page` - запуск браузера Chromium и создание страницы (с корректным закрытием даже при Ctrl+C);
- `login_form` - открытие страницы логина и поиск локаторов email/password/submit;
- `ui_login_url` - URL страницы логина из `configuration.UI_LOGIN_URL`.

## Запуск тестов

**Примечание:** перед запуском создай `.env` в корне проекта и укажи в нём:
```env
VRVR_USERNAME=your_login@example.com
VRVR_PASSWORD=your_password
```


### Установка зависимостей
```bash
python -m pip install -r requirements.txt
```

### Все тесты
```bash
python -m pytest -v
```

### Запуск конкретного теста
```bash
python -m pytest tests/test_create_channel.py -v
```

## UI тесты
Добавлен отдельный набор UI-тестов в `tests_ui/` на Playwright + Pytest.

Покрытие:
- успешный вход с логином/паролем из `.env`;
- валидация email в UI: ввод email с пробелами в начале и конце должен показывать ошибку (`Неверный email` / `Invalid Email address` в зависимости от языка UI);
- валидация email в UI: ввод email в некорректном формате должен показывать ошибку (`Неверный email` / `Invalid Email address`);
- авторизация с пустым email: проверка ошибки обязательного поля;
- авторизация с пустым паролем: проверка ошибки обязательного поля;
- авторизация с некорректным паролем: проверка ошибки `Invalid email or password`;
- авторизация с некорректным email + некорректным паролем: проверка ошибки `Invalid email or password`;
- успешная авторизация: проверка редиректа на страницу каналов (`/channels`);
- навигация после авторизации: переходы на страницы `Library` (`/contents`), `Devices` (`/devices`) и `Account` (`/account`);
- поиск по каналам в UI: полный/частичный запрос, пустой результат, сброс поиска;
- открытие канала из списка (переход на `/channels/<id>`).

### Установка для UI
```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### Запуск UI тестов
```bash
python -m pytest tests_ui -v
```

Примечание: URL страницы логина берется из `configuration.UI_LOGIN_URL` (по умолчанию `https://dev.vrvr-dev.ru/login`).

## Структура проекта
```
autotest/
│
├── configuration.py        # адрес сервера и API пути
├── data.py                 # тестовые данные и загрузка логина/пароля из .env
├── sender_requests.py      # все HTTP-запросы (обёртки над requests)
├── requirements.txt        # зафиксированные версии зависимостей
├── .gitignore
│
├── tests/
    ├── conftest.py                               # общие фикстуры: login, channel, cleanup
    ├── test_auth_login_positive.py               # авторизация существующего пользователя
    ├── test_auth_login_negative.py               # негативные тесты на авторизацию
    ├── test_auth_login_trim_case.py              # проверка логина с пробелами и разным регистром email (API)
    ├── test_create_channel.py                    # создание канала
    ├── test_create_channel_duplicate.py          # создание канала с дублирующим наименованием
    ├── test_create_folder.py                     # создание раздела в существующем канале
    ├── test_create_folder_invalid_channel.py     # создание раздела в несуществующем канале
    ├── test_create_folder_without_title.py       # создание раздела без обязательного поля Название раздела
    ├── test_delete_channel.py                    # удаление существующего канала
    ├── test_delete_channel_negative.py           # удаление несуществующего канала
    ├── test_delete_folder.py                     # удаление существующего раздела
    ├── test_delete_folder_invalid_channel_id.py  # удаление раздела из несуществующего канала
    ├── test_delete_folder_invalid_folder_id.py   # удаление несуществующего раздела
    ├── test_delete_folder_twice.py               # повторное удаление одного и того же раздела
    ├── test_get_channel_by_id.py                 # получение канала по id
    ├── test_get_channel_not_found.py             # получение канала с несуществующим id
    ├── test_get_channels.py                      # получение списка каналов и проверка созданного
    ├── test_play_mode_toggle.py                  # переключение режима autoplay/singleplay
    ├── test_swap_folders_duplicate_positions.py  # смена порядка с дублирующими позициями разделов
    ├── test_swap_folders_invalid_folder.py       # смена порядка с несуществующим разделом
    ├── test_swap_folders_position.py             # успешная перестановка двух разделов
    ├── test_update_channel.py                    # изменение названия канала
    └── test_update_free_play_mode.py             # включение/выключение free play mode
└── tests_ui/
    ├── conftest.py                               # UI-фикстуры Playwright (браузер, страница логина, локаторы)
    ├── test_auth_login_ui.py                     # UI-тесты логина: success, email с пробелами/неверным форматом, пустые поля, неверные креды
    ├── test_channels_page_ui.py                  # UI-тесты поиска по каналам и открытия канала из списка
    ├── test_post_login_redirect_ui.py            # UI-тест: редирект на /channels после успешного логина
    └── test_navigation_ui.py                     # UI-тесты навигации: переходы на /contents, /devices, /account
```
Всего: 26 API-автотеста + 14 UI-автотестов.
