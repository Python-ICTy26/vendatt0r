import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = None

    def get(self, url: str, params=None, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        timeout = self.timeout
        max_retries = self.max_retries
        backoff_factor = self.backoff_factor
        session = self.request_retry_session(max_retries, backoff_factor)
        return session.get(self.base_url + f"/{url}", params=params, timeout=timeout)

    def post(self, url, data=None, params=None, **kwargs: tp.Any) -> requests.Response:
        timeout = kwargs.get("timeout", None) or self.timeout
        max_retries = kwargs.get("max_retries", None) or self.max_retries
        backoff_factor = kwargs.get("backoff_factor", None) or self.backoff_factor
        session = self.request_retry_session(max_retries, backoff_factor)
        return session.post(self.base_url + f"/{url}", data=data, params=params, timeout=timeout)

    def request_retry_session(self, max_retries, backoff_factor) -> requests.Session:
        if not self.session:
            self.session = requests.Session()
            retry = Retry(
                 total=max_retries,
                 backoff_factor=backoff_factor,
                 raise_on_status=True,
                 status_forcelist=[500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("https://", adapter)
        return self.session
