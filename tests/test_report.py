import pytest

from load_tester.models.http import HTTPResponseResult
from load_tester.report import Report

# TODO: docker
# TODO: docker-compose
# TODO: run test cases


def test_report_with_mixed_results():
    results = [
        HTTPResponseResult(is_success=True, response_time=0.2, status_code=200),
        HTTPResponseResult(is_success=True, response_time=0.3, status_code=200),
        HTTPResponseResult(is_success=False, response_time=0.5, status_code=400),
    ]
    report = Report(results)

    assert len(report.results) == 3
    assert report.success_count == 2
    assert report.failure_count == 1
    assert abs(report.avg_time - 0.3333) < 1e-3
    assert report.min_time == 0.2
    assert report.max_time == 0.5


def test_report_with_all_success():
    results = [
        HTTPResponseResult(is_success=True, response_time=0.1, status_code=200),
        HTTPResponseResult(is_success=True, response_time=0.4, status_code=200),
    ]
    report = Report(results)

    assert len(report.results) == 2
    assert report.success_count == 2
    assert report.failure_count == 0
    assert abs(report.avg_time - 0.25) < 1e-3
    assert report.min_time == 0.1
    assert report.max_time == 0.4


def test_report_with_all_failures():
    results = [
        HTTPResponseResult(is_success=False, response_time=1.1, status_code=400),
        HTTPResponseResult(is_success=False, response_time=0.9, status_code=400),
    ]
    report = Report(results)

    assert len(report.results) == 2
    assert report.success_count == 0
    assert report.failure_count == 2
    assert abs(report.avg_time - 1.0) < 1e-3
    assert report.min_time == 0.9
    assert report.max_time == 1.1


def test_report_with_empty_results():
    report = Report([])

    assert len(report.results) == 0
    assert report.success_count == 0
    assert report.failure_count == 0
    assert report.avg_time == 0.0
    assert report.min_time == 0.0
    assert report.max_time == 0.0
