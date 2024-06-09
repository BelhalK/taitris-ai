from functools import wraps
from typing import NamedTuple

from taitriscore.config import CONFIG, Singleton
from taitriscore.logs import logger
from taitriscore.utils.token_counter import TOKEN_COSTS


class RequestRateLimiter:
    """
    A class to enforce rate limits on API requests.

    Attributes:
        rpm (int): The number of requests allowed per minute.
        last_call_time (float): The time when the last request was made.
        interval (float): The minimum interval between requests in seconds.

    Methods:
        split_batches(batch):
            Splits a batch of requests into smaller batches according to the rate limit.
        wait_if_needed(num_requests):
            Waits if necessary to ensure the rate limit is not exceeded.
    """

    def __init__(self, rpm):
        """
        Initializes the RequestRateLimiter with the specified requests per minute (rpm).

        Args:
            rpm (int): The number of requests allowed per minute.
        """
        self.last_call_time = 0
        self.interval = 1.1 * 60 / rpm
        self.rpm = rpm

    def split_batches(self, batch):
        """
        Splits a batch of requests into smaller batches according to the rate limit.

        Args:
            batch (list): The list of requests to be split into batches.

        Returns:
            list: A list of smaller batches of requests.
        """
        return [batch[i : i + self.rpm] for i in range(0, len(batch), self.rpm)]

    async def wait_if_needed(self, num_requests):
        """
        Waits if necessary to ensure the rate limit is not exceeded.

        Args:
            num_requests (int): The number of requests to be made.

        Logs:
            Info: Logs the remaining time to sleep if rate limit is exceeded.
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time

        if elapsed_time < self.interval * num_requests:
            remaining_time = self.interval * num_requests - elapsed_time
            logger.info(f"sleep {remaining_time}")
            await asyncio.sleep(remaining_time)

        self.last_call_time = time.time()


class Costs(NamedTuple):
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost: float
    total_budget: float


class CostHandler(metaclass=Singleton):
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.total_budget = 0

    def update_cost(self, prompt_tokens, completion_tokens, model):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        cost = (
            prompt_tokens * TOKEN_COSTS[model]["prompt"]
            + completion_tokens * TOKEN_COSTS[model]["completion"]
        ) / 1000
        self.total_cost += cost
        logger.info(
            f"Total running cost: ${self.total_cost:.3f} | Max budget: ${CONFIG.max_budget:.3f} | "
            f"Current cost: ${cost:.3f}, {prompt_tokens}, {completion_tokens}"
        )
        CONFIG.total_cost = self.total_cost

    def get_total_prompt_tokens(self):
        return self.total_prompt_tokens

    def get_total_completion_tokens(self):
        return self.total_completion_tokens

    def get_total_cost(self):
        return self.total_cost

    def get_costs(self) -> Costs:
        return Costs(
            self.total_prompt_tokens,
            self.total_completion_tokens,
            self.total_cost,
            self.total_budget,
        )


def retry(max_retries):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return await f(*args, **kwargs)
                except Exception:
                    if i == max_retries - 1:
                        raise
                    await asyncio.sleep(2**i)

        return wrapper

    return decorator
