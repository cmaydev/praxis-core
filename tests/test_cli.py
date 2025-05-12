"""Basic smoke test for CLI."""
from click.testing import CliRunner
from praxis.cli import main

def test_cli_quits():
    runner = CliRunner()
    result = runner.invoke(main, input="exit\n")
    assert result.exit_code == 0
