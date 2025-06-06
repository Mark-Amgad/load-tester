from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from load_tester.models.config import Config
from load_tester.models.config import HTTPMethod
from load_tester.report import Report
from load_tester.tester import run_test

app = typer.Typer(help="Simple REST API Load Tester")


def validate_status_code(value: int):
    if value < 100 or value > 599:
        raise typer.BadParameter("Invalid HTTP status code.")
    return value


@app.command()
def run(
    url: str = typer.Option(..., help="Target URL to test."),
    method: HTTPMethod = typer.Option("GET", help="HTTP method to use."),
    expected_status: int = typer.Option(
        200, callback=validate_status_code, help="Expected HTTP status code."
    ),
    concurrency: int = typer.Option(10, help="Number of concurrent users."),
    requests: int = typer.Option(100, help="Total number of requests to send."),
    headers: Optional[str] = typer.Option(None, help="Custom headers as JSON string."),
    data: Optional[str] = typer.Option(None, help="Data to send in POST/PUT requests."),
):
    import json

    try:
        headers_dict = json.loads(headers) if headers else None
    except Exception as e:
        typer.echo(f"Invalid headers JSON: {e}")
        raise typer.Exit(code=1)

    try:
        config = Config(
            url=url,
            method=method,
            expected_status=expected_status,
            concurrency=concurrency,
            requests=requests,
            headers=headers_dict,
            data=data,
        )
    except Exception as e:
        typer.echo(f"Configuration error: {e}")
        raise typer.Exit(code=1)

    print("configs:", config)
    print("Start Testing .. ")
    results = run_test(config)
    print("End Testing .. ")
    # success_count: int = sum(1 for r in results if r.is_success)
    # failure_count: int = len(results) - success_count
    report = Report(results=results)
    report.print_summary()
