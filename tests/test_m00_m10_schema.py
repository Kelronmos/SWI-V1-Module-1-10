"""Schema contract tests for M00-M10 zero-base input.
Proves schema behaviour only. Does not claim CI, seal, or full implementation.
"""
import pytest
import jsonschema


@pytest.mark.contract
@pytest.mark.m00_m10
class TestSchemaContracts:
    def test_valid_payload_passes(self, schema_validator, valid_zero_base_payload):
        schema_validator.validate(valid_zero_base_payload)

    def test_reject_extra_top_level_property(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["unauthorized_side_effect"] = True
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_invalid_module_id(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["module_id"] = "M15"
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_future_module_m11(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["module_id"] = "M11"
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_invalid_execution_mode(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["data"] = {"execution_mode": "RANDOM", "strict_validation": True}
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_missing_required_field(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        del payload["payload_version"]
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_invalid_module_id_type(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["module_id"] = 100
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_unknown_data_property(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["data"] = {
            "execution_mode": "DETERMINISTIC",
            "strict_validation": True,
            "unexpected_state": "DRIFT",
        }
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)

    def test_reject_extra_parameter_key(self, schema_validator, valid_zero_base_payload):
        payload = dict(valid_zero_base_payload)
        payload["data"] = {
            "execution_mode": "DETERMINISTIC",
            "strict_validation": True,
            "parameters": {"secret": True},
        }
        with pytest.raises(jsonschema.ValidationError):
            schema_validator.validate(payload)
