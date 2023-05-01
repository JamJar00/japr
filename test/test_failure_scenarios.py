import json
import os
import subprocess


def pytest_generate_tests(metafunc):
    scenarios = os.listdir("test/scenarios/failures")
    metafunc.parametrize("scenario", scenarios)


def test_scenario_fails_correct_rule(scenario):
    result = subprocess.run(
        [
            "poetry",
            "run",
            "japr",
            "test/scenarios/failures/" + scenario,
            "--json",
            "-t",
            "open-source",
        ],
        capture_output=True,
    )
    assert result.returncode == 1

    result_json = json.loads(result.stdout)

    assert any(
        test
        for test in result_json["results"]
        if test["id"] == scenario and test["result"] == "FAILED"
    )
