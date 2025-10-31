import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validators import InputValidator


def test_validate_user_input():
    print("Тестирование валидации пользовательского ввода...")
    
    valid_inputs = [
        "Мне нравятся кооперативные игры",
        "Хочу простые партийные игры",
        "евро игры с рабочими",
    ]
    
    for inp in valid_inputs:
        is_valid, error = InputValidator.validate_user_input(inp)
        assert is_valid, f"Должно быть валидным: '{inp}', ошибка: {error}"
        print(f"  ✓ '{inp}' - валидно")
    
    invalid_inputs = [
        ("", "пустая строка"),
        ("  ", "только пробелы"),
        ("ab", "слишком короткая"),
        ("a" * 501, "слишком длинная"),
        ("test@#$%", "недопустимые символы"),
    ]
    
    for inp, reason in invalid_inputs:
        is_valid, error = InputValidator.validate_user_input(inp)
        assert not is_valid, f"Должно быть невалидным ({reason}): '{inp}'"
        print(f"  ✓ '{inp[:20]}...' - невалидно ({reason})")
    
    print("✅ Тест валидации ввода пройден\n")


def test_validate_choice():
    print("Тестирование валидации выбора...")
    
    valid_choices = [
        ("1", 1, 4, 1),
        ("3", 1, 4, 3),
        ("2", 1, 3, 2),
    ]
    
    for choice, min_val, max_val, expected in valid_choices:
        is_valid, error, result = InputValidator.validate_choice(choice, min_val, max_val)
        assert is_valid, f"Должно быть валидным: {choice}"
        assert result == expected, f"Ожидалось {expected}, получено {result}"
        print(f"  ✓ '{choice}' в диапазоне [{min_val}, {max_val}] = {result}")
    
    invalid_choices = [
        ("", 1, 4, "пустой ввод"),
        ("abc", 1, 4, "не число"),
        ("0", 1, 4, "вне диапазона"),
        ("5", 1, 4, "вне диапазона"),
    ]
    
    for choice, min_val, max_val, reason in invalid_choices:
        is_valid, error, result = InputValidator.validate_choice(choice, min_val, max_val)
        assert not is_valid, f"Должно быть невалидным ({reason}): {choice}"
        print(f"  ✓ '{choice}' - невалидно ({reason})")
    
    print("✅ Тест валидации выбора пройден\n")


def test_sanitize_input():
    print("Тестирование санитизации ввода...")
    
    test_cases = [
        ("  text  ", "text"),
        ("multiple   spaces", "multiple spaces"),
        ("  leading and trailing  ", "leading and trailing"),
    ]
    
    for inp, expected in test_cases:
        result = InputValidator.sanitize_input(inp)
        assert result == expected, f"Ожидалось '{expected}', получено '{result}'"
        print(f"  ✓ '{inp}' → '{result}'")
    
    print("✅ Тест санитизации пройден\n")


def test_has_meaningful_content():
    print("Тестирование проверки содержания...")
    
    meaningful = ["евро игры", "кооперативные настольные", "простые партийные"]
    for text in meaningful:
        assert InputValidator.has_meaningful_content(text), f"Должно быть содержательным: {text}"
        print(f"  ✓ '{text}' - содержательно")
    
    not_meaningful = ["евро", "игры", "а"]
    for text in not_meaningful:
        assert not InputValidator.has_meaningful_content(text), f"Не должно быть содержательным: {text}"
        print(f"  ✓ '{text}' - недостаточно содержательно")
    
    print("✅ Тест проверки содержания пройден\n")


def run_all_tests():
    print("=" * 60)
    print("Тестирование модуля валидации".center(60))
    print("=" * 60)
    print()
    
    try:
        test_validate_user_input()
        test_validate_choice()
        test_sanitize_input()
        test_has_meaningful_content()
        
        print("=" * 60)
        print("✅ ВСЕ ТЕСТЫ ВАЛИДАЦИИ ПРОЙДЕНЫ".center(60))
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()

