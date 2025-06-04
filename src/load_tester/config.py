import typer
from typing import Optional

app = typer.Typer(help="Simple REST API Load Tester")

def validate_status_code(value: int):
    if value < 100 or value > 599:
        raise typer.BadParameter("Invalid HTTP status code.")
    return value

@app.command()
def run(
    url: str = typer.Option(..., help="Target URL to test."),
    method: str = typer.Option("GET", help="HTTP method to use."),
    expected_status: int = typer.Option(200, callback=validate_status_code, help="Expected HTTP status code."),
    concurrency: int = typer.Option(10, help="Number of concurrent users."),
    requests: int = typer.Option(100, help="Total number of requests to send."),
    headers: Optional[str] = typer.Option(None, help="Custom headers as JSON string."),
    data: Optional[str] = typer.Option(None, help="Data to send in POST/PUT requests."),
):
    config = {
        "url": url,
        "method": method.upper(),
        "expected_status": expected_status,
        "concurrency": concurrency,
        "requests": requests,
        "headers": headers,
        "data": data,
    }

    # TODO: run the load test
    print(config)
