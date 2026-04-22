import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.receiver import receive_tasks
from src.sources import APISource, FileSource, GeneratorSource
from src.task import Task


def print_tasks(title: str, tasks: list[Task]) -> None:
    print(f"\n{title}")
    print("-" * len(title))

    for task in tasks:
        print(task)
        print(f"  id: {task.id}")
        print(f"  description: {task.description}")
        print(f"  priority: {task.priority}")
        print(f"  status: {task.status}")
        print(f"  created_at: {task.created_at}")
        print(f"  is_ready: {task.is_ready}")
        print(f"  is_completed: {task.is_completed}")
        print()


def demo_generator_source() -> None:
    source = GeneratorSource(count=3)
    tasks = receive_tasks(source)
    print_tasks("GeneratorSource", tasks)


def demo_api_source() -> None:
    source = APISource()
    tasks = receive_tasks(source)
    print_tasks("APISource", tasks)


def demo_file_source() -> None:
    demo_data = [
        {"id": 201, "payload": {"source": "file", "message": "alpha task"}},
        {"id": 202, "payload": {"source": "file", "message": "beta task"}},
    ]

    with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as tmp:
        json.dump(demo_data, tmp, ensure_ascii=False, indent=2)
        tmp_path = Path(tmp.name)

    try:
        source = FileSource(tmp_path)
        tasks = receive_tasks(source)
        print_tasks("FileSource", tasks)
    finally:
        tmp_path.unlink(missing_ok=True)


from src.receiver import receive_tasks
from src.sources import GeneratorSource
from src.task_queue import TaskQueue


def main() -> None:
    source = GeneratorSource(5)
    tasks = receive_tasks(source)

    queue = TaskQueue(tasks)

    print("Все задачи:")
    for task in queue:
        print(task)

    print("\nЗадачи со статусом new:")
    for task in queue.filter_by_status("new"):
        print(task)

    print("\nЗадачи с приоритетом >= 3:")
    for task in queue.filter_by_priority(min_priority=3):
        print(task)

    completed_count = sum(1 for task in queue if task.is_completed)
    print(f"\nКоличество завершённых задач: {completed_count}")


if __name__ == "__main__":
    main()