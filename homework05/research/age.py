import datetime as dt
import statistics
import typing as tp

from homework05.vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    friends_response = get_friends(user_id).items
    friends_age = []
    year = dt.datetime.now().year
    for friend in friends_response:
        try:
            friends_age.append(year - int(friend["bdate"][5:]))
        except:
            pass
    if friends_age:
        return statistics.median(friends_age)
    else:
        None

