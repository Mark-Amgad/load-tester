from typing import List

from rich.console import Console
from rich.table import Table

from load_tester.models.http import HTTPResponseResult


class Report:
    def __init__(self, results: List[HTTPResponseResult]):
        print("add log 3")
        self.results = results
        self.success_count = 0
        self.failure_count = 0
        self.avg_time = 0
        self.min_time = float("inf")
        self.max_time = 0
        self._generate_basic_report()

    def _generate_basic_report(self):
        sum_ = 0
        for r in self.results:
            if r.is_success:
                self.success_count += 1
            else:
                self.failure_count += 1

            self.max_time = max(self.max_time, r.response_time)
            self.min_time = min(self.min_time, r.response_time)
            sum_ += r.response_time

        if len(self.results) > 0:
            self.avg_time = sum_ / len(self.results)
        else:
            self.avg_time = 0

    def print_summary(self):
        table = Table(
            title="Test Summary", show_header=True, header_style="bold magenta"
        )
        table.add_column("Metric", style="dim")
        table.add_column("Value")

        table.add_row("Total Requests", str(len(self.results)))
        table.add_row("Success", str(self.success_count))
        table.add_row("Failures", str(self.failure_count))
        table.add_row("Average Time (s)", f"{self.avg_time:.3f}")
        table.add_row("Min Time (s)", f"{self.min_time:.3f}")
        table.add_row("Max Time (s)", f"{self.max_time:.3f}")
        console = Console()
        console.print(table)
