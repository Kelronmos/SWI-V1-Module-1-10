"""Adversarial schema tests for M00-M10 input contract."""
import pytest
import jsonschema


@pytest.mark.adversarial
@pytest.mark.m00_m10
def test_null_module_id_rejected(schema_validator, valid_zero_base_payload):
    payload = dict(valid_zero_base_payload)
    payload["module_id"] = None
    with pytest.raises(jsonschema.ValidationError):
        schema_validator.validate(payload)


@pytest.mark.adversarial
@pytest.mark.m00_m10
def test_empty_object_rejected(schema_validator):
    with pytest.raises(jsonschema.ValidationError):
        schema_validator.validate({})


@pytest.mark.adversarial
@pytest.mark.m00_m10
def test_m00_valid_boundary(schema_validator, valid_zero_base_payload):
    payload = dict(valid_zero_base_payload)
    payload["module_id"] = "M00"
    schema_validator.validate(payload)


@pytest.mark.adversarial
@pytest.mark.m00_m10
def test_m10_valid_boundary(schema_validator, valid_zero_base_payload):
    payload = dict(valid_zero_base_payload)
    payload["module_id"] = "M10"
    schema_validator.validate(payload)
