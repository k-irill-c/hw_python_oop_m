"""Программный модуль фитнес-трекера,
   который обрабатывает данные для трех видов тренировок:
   для бега, спортивной ходьбы и плавания.
"""

from dataclasses import dataclass
from typing import ClassVar
from typing import List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        "Тип тренировки: {}; "
        "Длительность: {:.3f} ч.; "
        "Дистанция: {:.3f} км; "
        "Ср. скорость: {:.3f} км/ч; "
        "Потрачено ккал: {:.3f}."
    )

    def get_message(self) -> str:
        """Вывести результат тренировки."""
        return self.MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    HOUR: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIE_1: ClassVar[int] = 18
    COEF_CALORIE_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return (
            (self.COEF_CALORIE_1
             * self.get_mean_speed()
             - self.COEF_CALORIE_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CALORIE_01: ClassVar[float] = 0.035
    COEF_CALORIE_02: ClassVar[float] = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.COEF_CALORIE_01
             * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.COEF_CALORIE_02 * self.weight)
            * self.duration
            * self.HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEF_CALORIE_001: ClassVar[float] = 1.1
    COEF_CALORIE_002: ClassVar[int] = 2

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed()
             + self.COEF_CALORIE_001)
            * self.COEF_CALORIE_002
            * self.weight
        )

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    traning_types: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in traning_types:
        raise KeyError("Workout not found")
    return traning_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
