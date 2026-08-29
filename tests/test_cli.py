from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "price-bond" in result.stdout
    assert "build-curve" in result.stdout
    assert "risk-report" in result.stdout
    assert "scenario-risk" in result.stdout
