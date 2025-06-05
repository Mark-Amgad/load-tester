import asyncio
from http.client import responses

import httpx
import time
from rich.console import Console
from rich.table import Table

from load_tester.models.config import Config
from load_tester.models.http import HTTPResponseResult

console = Console()


async def send_request(client: httpx.AsyncClient, config: Config) -> HTTPResponseResult:
    """
    Sends a single HTTP request using the given configuration.

    Returns:
        (is_success, status_code, response_time, error message)
    """
    start = time.monotonic()
    try:
        response = await client.request(
            method=str(config.method.value),
            url=str(config.url),
            headers=config.headers,
            data=config.data,
        )
        return HTTPResponseResult(
            is_success=response.status_code == config.expected_status,
            status_code=response.status_code,
            response_time=time.monotonic() - start,
            error_message=(
                response.json()["detail"]
                if response.status_code != config.expected_status
                else None
            ),
        )

    except Exception as e:
        return HTTPResponseResult(
            is_success=False,
            status_code=400,
            error_message=str(e),
            response_time=time.monotonic() - start,
        )


def run_test(config: Config):
    res = asyncio.run(send_request(httpx.AsyncClient(), config))
    return res
