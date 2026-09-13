# Testing and Verification

```bash
python -m pytest -q
python -m pytest --cov=swi_core --cov-report=term-missing
python -m pytest test/test_module_kernel.py test/test_security_probe_kernel.py -q
./scripts/verify.sh
```

Adversarial classes (target): NORMAL / EDGE / ATTACK / FALSE POSITIVE.

`pytest` green alone is not Seal 5. See Volume 1 Part 2 manual.
