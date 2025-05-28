import json
import os
import subprocess


def pytest_generate_tests(metafunc):
    scenarios = os.listdir("test/scenarios/passes")
    metafunc.parametrize("scenario", scenarios)


def test_scenario_passes_correct_rule(scenario):
    print("To run this test locally, use the command:\n  poetry run japr test/scenarios/passes/" + scenario + " --json -t open-source | jq '.results[] | select(.id == \"" + scenario + "\")'")

    result = subprocess.run(
        [
            "poetry",
            "run",
            "japr",
            "test/scenarios/passes/" + scenario,
            "--json",
            "-t",
            "open-source",
        ],
        capture_output=True,
    )
    assert result.returncode == 1

    result_json = json.loads(result.stdout)
    scenario_id = scenario.split("_")[0]

    assert any(
        test
        for test in result_json["results"]
        if test["id"] == scenario_id and test["result"] == "PASSED"
    )
