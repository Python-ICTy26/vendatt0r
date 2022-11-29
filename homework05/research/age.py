import datetime as dt
import re
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    def calculate_age(date):
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        today = dt.date.today()
        ages = today.year - year
        if (today.month, today.day) < (month, day):
            ages -= 1
        return ages

    friends = get_friends(user_id, fields=["bdate"]).items
    res = []
    for i in friends:
        if "bdate" in i:
            if re.findall(r"\d[.]\d[.]\d", i["bdate"]):
                born = i["bdate"].split(".")
                res.append(calculate_age(born))
    return statistics.median(res) if res else None
