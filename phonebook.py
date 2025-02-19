import re
import csv
from collections import defaultdict
from logger_1 import logger


with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


@logger
def format_phone_number(phone):
    """Форматирует номер телефона в стандартный вид +7(XXX)XXX-XX-XX доб.XXXX"""
    pattern = re.compile(
        r"(\+?7|8)\s*\(?(\d{3})\)?[\s*-]*(\d{3})[\s*-]*(\d{2})[\s*-]*(\d{2})"
        r"(?:\s*\(?доб\.?\s*(\d+)\)?)?"
    )
    match = pattern.search(phone)
    if match:
        formatted_phone = f"+7({match[2]}){match[3]}-{match[4]}-{match[5]}"
        if match[6]:
            formatted_phone += f" доб.{match[6]}"
        return formatted_phone
    return phone


@logger
def normalize_name(name_parts):
    """Нормализует ФИО, заполняя недостающие части"""
    full_name = " ".join(name_parts[:3]).split()  # Объединяем и разделяем
    while len(full_name) < 3:
        full_name.append("")
    return full_name


@logger
def merge_contacts(contacts):
    """Объединяет дубликаты в списке контактов"""
    contacts_dict = defaultdict(lambda: ["", "", "", "", "", "", ""])  # Шаблон записи

    for contact in contacts:
        last_name, first_name, surname = normalize_name(contact[:3])
        key = (last_name, first_name)  # Ключ - имя и фамилия

        existing = contacts_dict[key]  # Проверяем, есть ли уже такой человек

        contacts_dict[key] = [
            last_name,
            first_name,
            surname if existing[2] == "" else existing[2],
            contact[3] if existing[3] == "" else existing[3],
            contact[4] if existing[4] == "" else existing[4],
            format_phone_number(contact[5]) if existing[5] == "" else existing[5],
            contact[6] if existing[6] == "" else existing[6],
        ]

    return list(contacts_dict.values())  # Преобразуем в список


table = merge_contacts(contacts_list)


with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(table)

