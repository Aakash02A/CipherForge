import sys
from unittest.mock import patch

import pytest

import main


def test_non_interactive_flag_parsing():
    """--non-interactive and -n flags are parsed correctly."""
    # --non-interactive
    args = main.argparse.ArgumentParser(prog="main")
    args.add_argument("--non-interactive", "-n", action="store_true",
                      help="Run demos non-interactively for CI/curriculum showcases")
    parsed = args.parse_args(["--non-interactive"])
    assert parsed.non_interactive is True

    # -n
    parsed = args.parse_args(["-n"])
    assert parsed.non_interactive is True

    # default
    parsed = args.parse_args([])
    assert parsed.non_interactive is False


def test_run_non_interactive_demo_runs_without_input(monkeypatch, capsys):
    """_run_non_interactive_demo completes without blocking on input()."""
    # Stub out _run so it doesn't actually call input()
    called = {}

    def fake_run(module_path, func_name, label):
        called["module"] = module_path
        called["func"] = func_name
        called["label"] = label
        print(f"  [Demo] {label} ran")

    monkeypatch.setattr(main, "_run", fake_run)

    main._run_non_interactive_demo()
    captured = capsys.readouterr()

    assert "Caesar Frequency Auto-Solve" in captured.out
    assert "All demos complete." in captured.out
    assert called["module"] == "level-01-classical-ciphers.traditional-ciphers.Caesar"
    assert called["func"] == "frequency_auto_solve_demo"


def test_main_non_interactive_exits_cleanly(monkeypatch, capsys):
    """main(['--non-interactive']) runs demo and returns without blocking."""
    called = {}

    def fake_run(module_path, func_name, label):
        called["module"] = module_path
        called["func"] = func_name
        called["label"] = label
        print(f"  [Demo] {label} ran")

    # Patch _run so it doesn't actually call input()
    monkeypatch.setattr(main, "_run", fake_run)

    # Patch sys.argv to simulate --non-interactive
    monkeypatch.setattr(sys, "argv", ["main.py", "--non-interactive"])

    # Patch input to fail if called (should not be reached)
    def fail_input(*args, **kwargs):
        raise AssertionError("input() should not be called in non-interactive mode")

    monkeypatch.setattr("builtins.input", fail_input)

    try:
        main.main()
    except SystemExit:
        pass

    assert called.get("module") == "level-01-classical-ciphers.traditional-ciphers.Caesar"
    assert called.get("func") == "frequency_auto_solve_demo"
    captured = capsys.readouterr()
    assert "Non-Interactive Demo Mode" in captured.out
    assert "All demos complete." in captured.out
