"""
Работа с данными курсов
"""
import json
import os


COURSES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "courses.json")


def load_courses():
    """Загружает курсы из JSON файла"""
    if os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_courses(courses):
    """Сохраняет курсы в JSON файл"""
    os.makedirs(os.path.dirname(COURSES_FILE), exist_ok=True)
    with open(COURSES_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


def get_course_by_name(name):
    """Получает курс по названию"""
    courses = load_courses()
    for course in courses:
        if course["name"] == name:
            return course
    return None


def get_course_by_id(course_id):
    """Получает курс по ID"""
    courses = load_courses()
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


def get_course_materials(course_id, material_type="pdf"):
    """Получает материалы курса по типу"""
    course = get_course_by_id(course_id)
    if course and "materials" in course:
        return [m for m in course["materials"] if m.get("type") == material_type]
    return []


def add_course(course):
    """Добавляет новый курс"""
    courses = load_courses()
    courses.append(course)
    save_courses(courses)


def update_course(course_id, updated_data):
    """Обновляет курс"""
    courses = load_courses()
    for course in courses:
        if course["id"] == course_id:
            course.update(updated_data)
            save_courses(courses)
            return True
    return False


def delete_course(course_id):
    """Удаляет курс"""
    courses = load_courses()
    courses = [c for c in courses if c["id"] != course_id]
    save_courses(courses)
