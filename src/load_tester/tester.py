import asyncio
import time
from http.client import responses
from typing import List

import httpx
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


async def run_workers(config: Config) -> List[HTTPResponseResult]:
    """
    Run concurrent HTTP requests according to config.
    Returns:
        List of HTTPResponseResult
    """
    results: List[HTTPResponseResult] = []

    number_of_requests = config.requests
    number_of_concurrent_requests = config.concurrency

    limits = httpx.Limits(
        max_keepalive_connections=number_of_concurrent_requests,
        max_connections=number_of_concurrent_requests,
    )

    async with httpx.AsyncClient(timeout=10, limits=limits) as client:
        tasks: List[asyncio.Task] = []
        for _ in range(number_of_requests):
            tasks.append(asyncio.create_task(send_request(client, config)))
            if len(tasks) >= number_of_concurrent_requests:
                batch = await asyncio.gather(*tasks)
                print("Patch Executed")
                results.extend(batch)
                tasks.clear()

        # Final batch
        if tasks:
            batch = await asyncio.gather(*tasks)
            results.extend(batch)

    return results


def run_test(config: Config):
    # TODO: add logs for starting the test
    results = asyncio.run(run_workers(config))
    return results
    # TODO: calculate a report on the result
