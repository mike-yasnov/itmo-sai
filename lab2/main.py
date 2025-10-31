import os
import sys

from src import OWLKnowledgeBase, RecommendationEngine, DialogueManager


def validate_environment():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    owl_file = os.path.join(project_root, 'lab1', 'boardgames_fixed.owl')
    
    if not os.path.exists(owl_file):
        print(f"Ошибка: файл онтологии не найден: {owl_file}")
        print(f"Убедитесь что файл существует по пути: {owl_file}")
        sys.exit(1)
    
    if not os.access(owl_file, os.R_OK):
        print(f"Ошибка: нет прав на чтение файла: {owl_file}")
        sys.exit(1)
    
    return owl_file


def main():
    owl_file = validate_environment()
    
    try:
        kb = OWLKnowledgeBase(owl_file)
        engine = RecommendationEngine(kb)
        dialogue = DialogueManager(engine)
        
        dialogue.start_dialogue()
        
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Проверьте что все модули установлены корректно")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Работа системы прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        print("Детали ошибки:")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

