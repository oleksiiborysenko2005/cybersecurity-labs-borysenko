import re

def analyze_password(password, name, birth_date):
    score = 10
    issues = []
    
    if len(password) < 8: 
        score -= 3
    elif len(password) < 12: 
        score -= 1
    
    if not re.search(r'[a-z]', password): score -= 2
    if not re.search(r'[A-Z]', password): score -= 1
    if not re.search(r'[0-9]', password): score -= 1
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score -= 2
    
    name_lower = name.lower()
    password_lower = password.lower()
    
    if name_lower in password_lower:
        score -= 4
        issues.append("містить ім'я")
    
    birth_year = birth_date.split('.')[-1]
    if birth_year in password:
        score -= 4
        issues.append("містить рік народження")
    
    day, month = birth_date.split('.')[:2]
    if day in password or month in password:
        score -= 3
        issues.append("містить дату народження")
    
    final_score = max(1, min(score, 10))
    
    recommendations = []
    if issues:
        recommendations.append("Уникайте особистих даних у паролі")
    if len(password) < 12:
        recommendations.append("Збільште довжину до 12+ символів")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        recommendations.append("Додайте спеціальні символи")
    if not re.search(r'[A-Z]', password):
        recommendations.append("Додайте великі літери")
    
    return final_score, issues, recommendations

password = input("Пароль: ")
name = input("Ім'я: ")
birth_date = input("Дата народження (дд.мм.рррр): ")

score, issues, recommendations = analyze_password(password, name, birth_date)

print(f"\nОцінка: {score}/10")
if issues:
    print(f"Проблеми: {', '.join(issues)}")
if recommendations:
    print("Рекомендації:")
    for rec in recommendations:
        print(f"• {rec}")
