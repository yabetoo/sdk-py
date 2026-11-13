import json

import pytest
from yabetoo_py import Yabetoo, YabetooError
from yabetoo_py.models.payment import (
    ConfirmIntentRequest,
    MomoData,
    PaymentMethodData,
)
from yabetoo_py.models.disbursement import CreateDisbursementRequest
from yabetoo_py.models.checkout import CreateCheckoutSession


# Response bodies captured from the sandbox on 2026-11-13.
FAILED_CHARGE = {
    "id": "ch_756juX8pOvt1xHzUj0i7Q4Ozpp0tiX4sDJU8", "object": "charge",
    "intentId": "pi_AsjUuERRtuGcjyqonHd9zHlYS5rh0YNCcyD5", "financialTransactionId": None,
    "transactionId": "e08be1b0-8275-4fd6-bc89-8e98e311d5d3", "amount": 500, "captured": False,
    "currency": "xaf", "status": "failed", "failureCode": "payer_declined",
    "failureMessage": "APPROVAL_REJECTED", "externalId": "ext_SXUgjeBZTsaUjQkg",
    "paymentMethodId": "pm_YTVqeXqvRmhS7mfnQKxt5gQSjYh9Svsy2JfY",
    "createdAt": "2026-11-13T13:06:25.957+00:00", "updatedAt": "2026-11-13T13:06:26.602+00:00",
}
CREATED_DISBURSEMENT = {
    "id": "dis_d1sqRF2jyhAbcVTIBQBZdWMKPLwjrfIoDcKJ", "status": "failed", "amount": 98.5,
    "currency": "xaf", "transactionId": None, "financialTransactionId": None,
    "failureMessage": "Airtel transfer is only available in live mode",
    "executedAt": "2026-11-13T13:06:24.293Z",
}
CREATED_SESSION = {
    "id": "cs_NfwEyGcU0RZi1I5K8HeYfTpw", "successUrl": "https://example.com/ok",
    "cancelUrl": "https://example.com/ko", "url": "https://pay.yabetoo.com/c/cs_NfwEyGcU0RZi1I5K8HeYfTpw",
    "expiresAt": 1794660714,
}
UNAUTHORIZED = {
    "status": 401, "path": "/v1/payment-intents", "code": "E_UNAUTHORIZED",
    "message": "Unauthorized", "detail": "You are not authorized to access this resource.",
}


class FakeResponse:
    def __init__(self, status_code, body=None, text=None):
        self.status_code = status_code
        self._body = body
        self._text = text

    def json(self):
        if self._text is not None:
            return json.loads(self._text)
        return self._body


@pytest.fixture
def sdk():
    return Yabetoo("sk_test_example")


def momo():
    return PaymentMethodData(type="momo", momo=MomoData(msisdn="46733123451", country="cg", operator_name="mtn"))


def test_an_api_error_carries_the_api_message_and_code(sdk, mocker):
    mocker.patch.object(sdk.payments._client.session, "get", return_value=FakeResponse(401, UNAUTHORIZED))

    with pytest.raises(YabetooError) as exc_info:
        sdk.payments.retrieve("pi_test")

    assert exc_info.value.message == "Unauthorized"
    assert exc_info.value.code == "E_UNAUTHORIZED"


def test_a_not_found_error_carries_the_api_message(sdk, mocker):
    mocker.patch.object(sdk.payments._client.session, "get",
                        return_value=FakeResponse(404, {"message": "Row not found"}))

    with pytest.raises(YabetooError) as exc_info:
        sdk.payments.retrieve("pi_unknown")

    assert exc_info.value.message == "Row not found"


def test_a_response_that_is_not_json_raises_a_yabetoo_error(sdk, mocker):
    mocker.patch.object(sdk.payments._client.session, "get",
                        return_value=FakeResponse(404, text="Cannot GET:/v1/sessions"))

    with pytest.raises(YabetooError) as exc_info:
        sdk.payments.retrieve("pi_test")

    assert exc_info.value.message == "Invalid JSON response from API"


def test_listing_payments_needs_no_filters(sdk, mocker):
    get = mocker.patch.object(sdk.payments._client.session, "get",
                              return_value=FakeResponse(200, {"items": [], "totalCount": 0}))

    sdk.payments.all()

    assert get.called


def test_a_declined_payment_is_returned_not_raised(sdk, mocker):
    mocker.patch.object(sdk.payments._client.session, "post", return_value=FakeResponse(200, FAILED_CHARGE))

    charge = sdk.payments.confirm("pi_AsjUuERRtuGcjyqonHd9zHlYS5rh0YNCcyD5", ConfirmIntentRequest(
        client_secret="cs_test", payment_method_data=momo()))

    assert charge.status == "failed"
    assert charge.financial_transaction_Id is None


def test_a_created_disbursement_is_returned_as_the_api_sends_it(sdk, mocker):
    mocker.patch.object(sdk.disbursements._client.session, "post",
                        return_value=FakeResponse(200, CREATED_DISBURSEMENT))

    disbursement = sdk.disbursements.create(CreateDisbursementRequest(
        amount=100, currency="xaf", first_name="Test", last_name="Sdk", payment_method_data=momo()))

    assert disbursement.id == "dis_d1sqRF2jyhAbcVTIBQBZdWMKPLwjrfIoDcKJ"
    assert disbursement.amount == 98.5
    assert disbursement.status == "failed"


def test_a_created_checkout_session_is_returned_as_the_api_sends_it(sdk, mocker):
    mocker.patch.object(sdk.sessions._client.session, "post", return_value=FakeResponse(201, CREATED_SESSION))

    session = sdk.sessions.create(CreateCheckoutSession(
        account_id="acct_test", total=1500, currency="xaf",
        success_url="https://example.com/ok", cancel_url="https://example.com/ko"))

    assert str(session.url) == "https://pay.yabetoo.com/c/cs_NfwEyGcU0RZi1I5K8HeYfTpw"


def test_checkout_sessions_are_sent_to_the_checkout_api_in_sandbox():
    assert Yabetoo("sk_test_example").sessions._client.base_url == "https://buy.api.yabetoopay.com/v1"


def test_a_key_that_is_not_a_secret_key_is_refused():
    with pytest.raises(ValueError):
        Yabetoo("pk_test_example")
