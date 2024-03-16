# Простой RESTful API сервис для реферальной системы
### Тестовое задание на должность "Intern бекенд разработчик на языке Python" в компанию Stakewolle
### Исполнитель тестового задания: Роман Сырбу
### Используемый стек: FastAPI, SQLite3

### Описание проекта
На следующем скриншоте можно увидеть имеющиеся эндпоинты. 
Эндпоинты разделены на 3 блока:
1. /users - всё, что связано с пользователями
2. /codes - всё, что связано с реферальными кодами
3. / - дефолтный эндпоинт с сообщением, что нужно открыть UI документацию /docs
   
![image](https://github.com/sssyrbu/test_task_backend/assets/68150627/6e010535-bfd3-42bf-a6d9-83f10eaa70bd)

Данная документация разработана на Swagger UI, встроенный в FastAPI по умолчанию.

Я добавил эндпоинт "get_user_id_from_email", хотя его не было в ТЗ. Я решил добавить его, чтобы было удобнее получить id реферрера для дальнейшего использования эндпоинта "get_referrals_from_referrer_id". Также, я добавил хэширование паролей, и хранение их в БД, так как считаю хэширование хорошей практикой.

Справа в углу есть кнопка авторизации, где нужно ввести почту и пароль. Перед использованием всех эндпоинтов с "замочком" нужно пройти авторизацию, иначе будет выброшен код 403 и приложение выведет сообщение об ошибке.

Я решил добавить на гитхаб файл .env, в котором лежат глобальные переменные для создания и валидации jwt токенов и название файла с БД.

### Установка
Есть два варианта установки: локально и через докер.
#### Локально
1. ```
   git clone https://github.com/sssyrbu/test_task_backend
   ```
2. ```
   cd test_task_backend/
   ```
3. Этой юникс командой создадим приватный ключ для создания и валидации jwt
   ```
   echo "SECRET_KEY = '$(openssl rand -hex 32)'" >> .env
   ```  
5. ```
   python3 -m venv venv
   ```
6. ```
   source venv/bin/activate
   ```
7. ```
   pip install -r requirements.txt
   ```
8. ```
   cd app/
   ```
9. ```
   python3 main.py
   ```

#### Докер
1. ```
   git clone https://github.com/sssyrbu/test_task_backend
   ```
2. ```
   cd test_task_backend/
   ```
3. ```
   docker build -t referral_app .
   ```   
4. ```
   docker run -p 8081:8081 --name ref_app_container referral_app
   ```

### Адрес
http://0.0.0.0:8081/
### UI docs
http://0.0.0.0:8081/


![image](https://github.com/sssyrbu/test_task_backend/assets/68150627/77dcb94a-fcf3-4d27-bd75-42248e3d566d)
