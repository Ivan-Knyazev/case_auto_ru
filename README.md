# Система определения стоимости автомобиля по его характеристикам и описанию

## Инструкция для запуска приложения в Docker:

### 1. Создание Docker образа:

```bash
docker build -t auto_ru:0.0.1 .
```

<!-- ```bash
docker build --platform=linux/amd64 -t auto_ru:0.0.1 .
``` -->


### 2. Запуск контейнера:

```bash
docker run -p 8000:8000 -d auto_ru:0.0.1
```



## Инструкция для запуска приложения на OS Linux (Ubuntu) и локального использования

### 1. Установка git lfs:

```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
```
```bash
sudo apt-get install git-lfs
```


### 2. Клонирование всего репозитория:

Настройка пропуска отслеживаемых файлов LFS 
```bash
git lfs install --skip-smudge
```

Конирование репозитория:

- По SSH:
  ```bash
  git clone git@github.com:Ivan-Knyazev/case_auto_ru.git
  ```

- Или по HTTPS:
  ```bash
  git clone https://github.com/Ivan-Knyazev/case_auto_ru.git
  ```

Переход в директорию приложения
```bash
cd case_auto_ru/
```

Загрузка отслеживаемых файлов LFS (model.h5)
```bash
git lfs pull
```


### 3. Первый запуск приложения
Запускаем bash скрипт, который выполняет: нициализацию виртуального окружения, его настройку, создание базы данных и первый запуск приложения
```bash
chmod +x start.sh
```
```bash
./start.sh
```
Дожидаемся окончания выполнения операции (это займёт некоторое время)

Поздравляем!
Можете переходить в браузере по [адресу](http://127.0.0.1:8000 "localhost:8000") http://127.0.0.1:8000 и пользоваться сервисом


### 4. Старт приложения в последующие разы

```bash
python3 main.py
```