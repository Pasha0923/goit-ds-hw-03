
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv() # для завантаження змінних середовища з .env файлу
mongo_uri = os.getenv("MONGO_URI") # отримання URI з змінних середовища
# Підключення до MongoDB
client = MongoClient(mongo_uri)

# Створення бази даних cats_database
db = client["cats_database"]

# Створення колекції cats
cats_collection = db["cats"]

# Список документів для вставки
cats = [
    {
    "name": "Barsik", 
    "age": 3, 
    "features": ["ходить в лоток", "дає себе гладити", "рудий"]
    },
    {
    "name": "Lama",
    "age": 2, 
    "features": ["ходить в лоток", "не дає себе гладити", "сірий"]
    },
    {
    "name": "Liza",
    "age": 4, 
    "features": ["ходить в лоток", "не дає себе гладити", "білий"]
    },
    {
    "name": "Boris",
    "age": 12,
    "features": ["ходить в лоток", "дає себе гладити", "сірий"]
    },
    {
    "name": "Murzik",
    "age": 1, 
    "features": ["ходить в лоток", "дає себе гладити", "чорний"]
    }
]

# Вставка документів
# result = cats_collection.insert_many(cats)
# print("Додані документи з ID:", result.inserted_ids)

# Вставка документів (тільки якщо колекція порожня для уникнення дублювання даних при повторних запусках)
if cats_collection.count_documents({}) == 0:
    result = cats_collection.insert_many(cats)
    print("Якщо колекція порожня — документи додані з ID:", result.inserted_ids)
else:
    print("Колекція вже містить дані — вставка пропущена")
    print("--------------------------------------------")
# -------------READ----------------
# Функція 1: Вивести всіх котів
def show_all_cats():
    print("\nВсі записи про котів в колекції:")
    for cat in cats_collection.find({}):
        print(f"Ім'я: {cat['name']}, Вік: {cat['age']}, Характеристики: {cat['features']}")
    print("-----------------------------------------")

# Функція 2: Знайти кота за ім'ям
def find_cat_by_name():
    name = input("Введіть ім'я кота: ")
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(f"Ім'я: {cat['name']}, Вік: {cat['age']}, Характеристики: {cat['features']}")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдений")
    
# -------------UPDATE----------------
def update_cat_age():
    name = input("Введіть ім'я кота, якого хочете оновити: ")
    try:
        new_age = int(input("Введіть новий вік кота: "))
    except ValueError:
        print("Вік повинен бути цілим числом")
        return
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"Вік кота '{name}' оновлено до {new_age}")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдений")

def add_feature_to_cat():
    name = input("Введіть ім'я кота: ")
    new_feature = input("Введіть нову характеристику: ")

    if not new_feature.strip():
        print("Характеристика не повинна бути порожньою")
        return
    result = cats_collection.update_one({"name": name},{"$addToSet": {"features": new_feature}})
    if result.matched_count :
         print(f"Характеристика додана коту '{name}'")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдений")

# -------------DELETE----------------
#видалення кота за ім'ям
def delete_cat_by_name():
    name = input("Введіть ім'я кота, якого хочете видалити: ")
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Кіт з ім'ям '{name}' видалений")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдений")

# видалення всіх документів з колекції
def delete_all_cats():
    confirm = input("Бажаєте видалити всіх котів з колекції? (так/ні): ").strip().lower()
    if confirm == "так":
        result = cats_collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів")
    else:
        print("Операція скасована")

# Виклик функцій
# find_cat_by_name() # Пошук одного кота за ім'ям
update_cat_age() # Оновлення віку кота
# add_feature_to_cat() # Додавання нової характеристики коту
# delete_cat_by_name() # Видалення кота за ім'ям
# delete_all_cats() # Видалення всіх котів з колекції
show_all_cats() # Виведення всіх котів
