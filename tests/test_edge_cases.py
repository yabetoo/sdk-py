import pytest
from yabetoo_py import Yabetoo
from yabetoo_py.models.payment import (
    CreateIntentRequest,
    PaymentMethodData,
    MomoData
)
from yabetoo_py.errors import NetworkError


@pytest.fixture
def sdk():
    return Yabetoo("sk_test_example")


class TestPaymentEdgeCases:
    def test_empty_description(self, sdk, mocker):
        mock_response = {
            "id": "pi_test", "amount": "1000", "currency": "xaf",
            "label": "test", "clientSecret": "cs_test",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }
        mocker.patch.object(sdk.payments._client, 'request', return_value=mock_response)

        result = sdk.payments.create(CreateIntentRequest(
            amount=1000,
            currency="xaf",
            description=""
        ))
        assert result.id == "pi_test"

    def test_special_characters_metadata(self, sdk, mocker):
        mock_response = {
            "id": "pi_test", "amount": "1000", "currency": "xaf",
            "label": "test", "clientSecret": "cs_test",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }
        mocker.patch.object(sdk.payments._client, 'request', return_value=mock_response)

        result = sdk.payments.create(CreateIntentRequest(
            amount=1000,
            currency="xaf",
            metadata={"key": "value!@#$%^"}
        ))
        assert result.id == "pi_test"


class TestMomoEdgeCases:
    def test_unsupported_operator_rejected_by_pydantic(self):
        with pytest.raises(Exception):
            MomoData(
                country="cg",
                msisdn="+242123456789",
                operator_name="unsupported"
            )

    def test_valid_momo_data(self):
        momo = MomoData(
            country="cg",
            msisdn="+242123456789",
            operator_name="mtn"
        )
        assert momo.operator_name == "mtn"
        assert momo.country == "cg"


class TestNetworkEdgeCases:
    def test_timeout_handling(self, sdk, mocker):
        mocker.patch.object(sdk.payments._client, 'request',
                            side_effect=NetworkError("Request timed out"))

        with pytest.raises(NetworkError) as exc_info:
            sdk.payments.retrieve("pi_test")
        assert "Request timed out" in str(exc_info.value)

    def test_network_error_handling(self, sdk, mocker):
        mocker.patch.object(sdk.payments._client, 'request',
                            side_effect=NetworkError("Connection failed"))

        with pytest.raises(NetworkError):
            sdk.payments.retrieve("pi_test")


class TestAuthenticationEdgeCases:
    def test_empty_api_key(self):
        with pytest.raises(ValueError) as exc_info:
            Yabetoo("")
        assert "Secret key is required" in str(exc_info.value)


class TestDataValidationEdgeCases:
    def test_null_values_in_metadata(self, sdk, mocker):
        mock_response = {
            "id": "pi_test", "amount": "1000", "currency": "xaf",
            "label": "test", "clientSecret": "cs_test",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }
        mocker.patch.object(sdk.payments._client, 'request', return_value=mock_response)

        result = sdk.payments.create(CreateIntentRequest(
            amount=1000,
            currency="xaf",
            metadata={"key": None}
        ))
        assert result.id == "pi_test"

    def test_create_intent_request_minimal(self):
        req = CreateIntentRequest(amount=1000, currency="xaf")
        assert req.amount == 1000
        assert req.currency == "xaf"
        assert req.description is None
        assert req.metadata is None

    def test_payment_method_data(self):
        pmd = PaymentMethodData(
            type="momo",
            momo=MomoData(
                country="cg",
                msisdn="+242123456789",
                operator_name="airtel"
            )
        )
        assert pmd.type == "momo"
        assert pmd.momo.operator_name == "airtel"
