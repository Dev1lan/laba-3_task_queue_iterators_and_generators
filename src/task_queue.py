from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Callable
from src.task import Task


class TaskQueue:
    """Очередь задач с поддержкой итерации и ленивых фильтров"""

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        self._tasks: list[Task] = list(tasks) if tasks is not None else []

    def add(self, task: Task) -> None:
        """Добавить одну задачу в очередь"""
        self._tasks.append(task)

    def extend(self, tasks: Iterable[Task]) -> None:
        """Добавить несколько задач в очередь"""
        self._tasks.extend(tasks)

    def __iter__(self) -> Iterator[Task]:
        """Возвращает новый итератор при каждом вызове"""
        return iter(self._tasks)

    def __len__(self) -> int:
        """Количество задач в очереди"""
        return len(self._tasks)

    def __bool__(self) -> bool:
        """Пустая очередь -> False, непустая -> True"""
        return bool(self._tasks)

    def __repr__(self) -> str:
        return f"TaskQueue(tasks={self._tasks!r})"

    def filter(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """Общий ленивый фильтр"""
        for task in self._tasks:
            if predicate(task):
                yield task

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """Ленивый фильтр по статусу"""
        normalized_status = status.strip().lower()
        yield from self.filter(lambda task: task.status == normalized_status)

    def filter_by_priority(
        self,
        min_priority: int | None = None,
        max_priority: int | None = None,
    ) -> Iterator[Task]:
        """Ленивый фильтр по диапазону приоритета"""
        for task in self._tasks:
            if min_priority is not None and task.priority < min_priority:
                continue
            if max_priority is not None and task.priority > max_priority:
                continue
            yield task

    def iter_ready(self) -> Iterator[Task]:
        """Ленивый обход задач, готовых к выполнению"""
        yield from self.filter(lambda task: task.is_ready)

    def iter_completed(self) -> Iterator[Task]:
        """Ленивый обход завершённых задач"""
        yield from self.filter(lambda task: task.is_completed)