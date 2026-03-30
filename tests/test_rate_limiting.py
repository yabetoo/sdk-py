import pytest
from yabetoo_py import Yabetoo, YabetooError
from yabetoo_py.errors import APIError


@pytest.fixture
def sdk():
    return Yabetoo("sk_test_example")


class TestRateLimiting:
    def test_rate_limit_handling(self, sdk, mocker):
        mocker.patch.object(sdk.payments._client, 'request',
                            side_effect=YabetooError("Too many requests", code="rate_limit_error"))

        with pytest.raises(YabetooError) as exc_info:
            sdk.payments.retrieve("pi_test")

        assert "Too many requests" in str(exc_info.value)
        assert exc_info.value.code == "rate_limit_error"

    def test_quota_exceeded(self, sdk, mocker):
        mocker.patch.object(sdk.payments._client, 'request',
                            side_effect=APIError("Monthly API quota exceeded",
                                                 code="quota_exceeded"))

        with pytest.raises(APIError) as exc_info:
            sdk.payments.retrieve("pi_test")

        assert "Monthly API quota exceeded" in str(exc_info.value)
        assert exc_info.value.code == "quota_exceeded"

    def test_concurrent_requests(self, sdk, mocker):
        from concurrent.futures import ThreadPoolExecutor
        import threading

        lock = threading.Lock()
        call_count = [0]

        def mock_request(*args, **kwargs):
            with lock:
                call_count[0] += 1
                if call_count[0] > 5:
                    raise YabetooError("Too many concurrent requests", code="rate_limit_error")
            return {
                "id": "pi_test", "amount": 1000, "currency": "xaf",
                "status": "succeeded"
            }

        mocker.patch.object(sdk.payments._client, 'request',
                            side_effect=mock_request)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(sdk.payments.retrieve, "pi_test")
                for _ in range(10)
            ]

            results = []
            errors = []
            for future in futures:
                try:
                    results.append(future.result())
                except YabetooError:
                    errors.append("rate_limit")

        assert len(results) > 0
        assert len(errors) > 0
