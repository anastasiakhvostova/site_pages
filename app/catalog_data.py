from enum import Enum


class Categories(Enum):
    romantic = 'про любов'
    fantasy = 'фантастика'
    # SEAFOOD = 'з морепродуктами'


menu = [
    {
        'title': 'Дівчина онлайн. Всі 3 книги.(Зої Загг)',
        'image': 'book1.jpg',
        'price': 820,
        'id': 1,
        'categories': [Categories.romantic.value]
    },
    {
        'title': 'Галант. (В.Е. Шваб)',
        'image': 'book2.jpg',
        'price': 500,
        'id': 2,
        'categories': [Categories.fantasy.value]
    },
    {
        'title': 'Енн. 8 книг(Люсі Мод Монтгомері',
        'image': 'book3.png',
        'price': 1300,
        'id': 3,
        'categories': [Categories.romantic.value]
    },
    {
        'title': 'Незриме життя Аді Лярю. (В.Е. Шваб)',
        'image': 'book4.jpg',
        'price': 500,
        'id': 4,
        'categories': [Categories.romantic.value, Categories.fantasy.value]
    },
    {
        'title': '9 листопада. (Коллін Гувер)',
        'image': 'book5.jpg',
        'price': 420,
        'id': 5,
        'categories': [Categories.romantic.value]
    },
    {
        'title': 'Серце часу. 3 книга.(Моніка Лец)',
        'image': 'book6.jpg',
        'price': 300,
        'id': 6,
        'categories': [Categories.romantic.value, Categories.fantasy.value]
    },
    {
        'title': 'Серце часу. 1 книга.(Моніка Лец)',
        'image': 'book7.jpg',
        'price': 300,
        'id': 7,
        'categories': [Categories.romantic.value, Categories.fantasy.value]
    },
    {
        'title': 'Серце часу. 2 книга.(Моніка Лец)',
        'image': 'book8.jpg',
        'price': 300,
        'id': 8,
        'categories': [Categories.romantic.value, Categories.fantasy.value]
    },
    {
        'title': 'Тисячу памя"тних поцілунків(Тілі Коул)',
        'image': 'book9.jpg',
        'price': 400,
        'id': 9,
        'categories': [Categories.romantic.value]
    },
    {
        'title': 'Шпигунки з притулку Артеміда(Наталія Довгопол)',
        'image': 'book10.jpg',
        'price': 200,
        'id': 10,
        'categories': [Categories.fantasy.value]
    },
    {
        'title': 'Наші приховані дари(Керолайн О"дногіо)',
        'image': 'book11.jpg',
        'price': 300,
        'id': 11,
        'categories': [Categories.fantasy.value]
    },
    {
        'title': 'Локвуд&Ко (Джонатан Страуд)',
        'image': 'book12.jpg',
        'price': 300,
        'id': 12,
        'categories': [Categories.fantasy.value]
    },
]
