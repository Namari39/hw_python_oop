from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return (distance / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(type(self).__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Running"""
        speed: float = super().get_mean_speed()
        duration_min: float = self.duration * self.H_IN_M
        calories: float = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * speed + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM * duration_min
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_WEIGHT_MULTIPLIER = 0.035
    CALORIES_MEAN_WEIGHT_SHIFT = 0.029
    M_IN_S = 0.278
    CENTIMETR_IN_METR = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. SportsWalking"""
        speed_sec: float = self.get_mean_speed() * self.M_IN_S
        duration_min: float = self.duration * self.H_IN_M
        height_m: float = self.height / self.CENTIMETR_IN_METR
        calories: float = (
                          (
                              self.CALORIES_MEAN_WEIGHT_MULTIPLIER
                              * self.weight
                              + (
                                  speed_sec**2 / height_m
                              )
                              * self.CALORIES_MEAN_WEIGHT_SHIFT * self.weight
                          )
            * duration_min
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_MULTIPLIER_SWM = 1.1
    CALORIES_MEAN_WEIGHT_SHIFT_SWM = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения. Swimming"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Swimming"""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        calories: float = ((speed + self.CALORIES_MEAN_SPEED_MULTIPLIER_SWM)
                           * self.CALORIES_MEAN_WEIGHT_SHIFT_SWM
                           * self.weight * self.duration)
        return calories


TRAINING_TYPE = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking
                 }


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_TYPE:
        raise ('Данная тренировка не предусмотренна')
    return TRAINING_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(InfoMessage.get_message(Training.show_training_info(training)))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
