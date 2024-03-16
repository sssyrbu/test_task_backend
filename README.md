# Простой RESTful API сервис для реферальной системы
### Тестовое задание на должность "Intern бекенд разработчик на языке Python" в компанию Stakewolle
### Исполнитель тестового задания: Роман Сырбу
### Испульзуемый стек: FastAPI, SQLite3

### Описание проекта
На следующем скриншоте можно увидеть имеющиеся эндпоинты. 
Эндпоинты разделены на 3 блока:
1. /users - всё, что связано с пользователями
2. /codes - всё, что связано с реферальными кодами
3. / - дефолтный эндпоинт с сообщением, что нужно открыть UI документацию /docs
![image](https://github.com/sssyrbu/test_task_backend/assets/68150627/6e010535-bfd3-42bf-a6d9-83f10eaa70bd)
Данная документация разработана на Swagger UI, встроенный в FastAPI по умолчанию.
Я добавил эндпоинт "get_user_id_from_email", хотя его не было в ТЗ. Я решил добавить его, чтобы было удобнее получить id реферрера для дальнейшего использования эндпоинта "get_referrals_from_referrer_id".
Справа в углу есть кнопка авторизации, где нужно ввести почту и пароль. Перед использованием всех эндпоинтов с "замочком" нужно пройти авторизацию, иначе будет выброшен код 403 и приложение выведет сообщение об ошибке.
