
# Приложение для обработки изображений

Это приложение для обработки изображений на основе PyQt5 и OpenCV. Оно позволяет загружать изображения, захватывать их с камеры, а также выполнять различные операции по редактированию изображений, такие как изменение размера, снижение яркости, рисование круга и выбор каналов изображения (красный, зелёный, синий).

## Установка

### Шаг 1: Клонирование репозитория

Склонируйте репозиторий на свой локальный компьютер:

```bash
git clone https://github.com/lop121/practika-letnia.git
cd practika-letnia
```

### Шаг 2: Создание виртуального окружения

Создайте и активируйте виртуальное окружение:
```bash
# Для Windows
python -m venv venv
venv\Scripts\activate

# Для macOS и Linux
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

Установите все необходимые зависимости из файла requirements.txt:
````bash
pip install -r requirements.txt
````

### Шаг 4: Установка PyTorch (рекомендовано)

Если ваше приложение использует PyTorch, установите его с помощью следующей команды:
```bash
# Для Windows
conda install pytorch==1.11.0 torchvision torchaudio cpuonly -c pytorch

# Для macOS и Linux
conda install pytorch==1.11.0 torchvision torchaudio -c pytorch
```
### Запуск приложения
Для запуска приложения выполните следующую команду:
```bash
python app.py
````
