"""Trainer must stop visibly on Module 02 kernel contract failure."""
import pytest

from swi_core.module00_trainer import Trainer
from swi_core.module_kernel import ModuleKernelError


def test_trainer_halts_on_non_string_input(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    with pytest.raises(ModuleKernelError) as exc:
        trainer.process(12345)  # type: ignore[arg-type]
    assert "halted_by_module_02_kernel" in str(exc.value) or "pre-check" in str(
        exc.value
    )


def test_trainer_does_not_continue_after_kernel_halt(tmp_path):
    trainer = Trainer(str(tmp_path / "audit.log"))
    before = trainer._turn_counter
    with pytest.raises(ModuleKernelError):
        trainer.process(["not", "a", "string"])  # type: ignore[arg-type]
    # turn was counted, but process did not return a successful PipelineResult
    assert trainer._turn_counter == before + 1
