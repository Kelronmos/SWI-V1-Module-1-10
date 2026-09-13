# Testing and Verification

## Run tests

```bash
python -m pytest -q
python -m pytest --cov=swi_core --cov-report=term-missing
```

## Kernel-specific

```bash
python -m pytest test/test_module_kernel.py test/test_security_probe_kernel.py -q
```

## Full script (local)

```bash
./scripts/verify.sh
```

## Adversarial classes (target coverage)

For each security-relevant module: **NORMAL**, **EDGE**, **ATTACK**, **FALSE POSITIVE**.

Adversarial suites under `test/adversarial/` are expanded over time; absence of a file means that class is not yet automated.

## Mutation sanity

Occasionally break a check (e.g. invert a threshold) and confirm tests fail, then restore.

## Seal note

`pytest` green alone is not Seal 5. See Volume 1 Part 2 manual for seal levels and foundation gate.
