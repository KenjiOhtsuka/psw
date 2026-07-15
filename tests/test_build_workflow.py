"""Tests for the .github/workflows/build.yml GitHub Actions workflow."""

import os

import pytest

yaml = pytest.importorskip("yaml")

WORKFLOW_PATH = os.path.join(
    os.path.dirname(__file__), "..", ".github", "workflows", "build.yml"
)


@pytest.fixture(scope="module")
def workflow():
    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_workflow_file_exists():
    assert os.path.isfile(WORKFLOW_PATH)


def test_workflow_is_valid_yaml(workflow):
    assert isinstance(workflow, dict)


def test_workflow_name(workflow):
    assert workflow["name"] == "Build psw"


def test_workflow_triggers_on_push(workflow):
    # PyYAML parses the `on:` key as boolean True in YAML 1.1
    triggers = workflow.get("on") or workflow.get(True)
    assert triggers is not None
    assert "push" in triggers


def test_workflow_triggers_on_version_tags(workflow):
    triggers = workflow.get("on") or workflow.get(True)
    assert triggers["push"]["tags"] == ["v*"]


def test_workflow_triggers_on_main_branch(workflow):
    triggers = workflow.get("on") or workflow.get(True)
    assert triggers["push"]["branches"] == ["main"]


def test_workflow_has_build_job(workflow):
    assert "build" in workflow["jobs"]


def test_build_job_matrix_includes_all_platforms(workflow):
    matrix = workflow["jobs"]["build"]["strategy"]["matrix"]
    assert matrix["os"] == ["ubuntu-latest", "windows-latest", "macos-latest"]


def test_build_job_runs_on_matrix_os(workflow):
    assert workflow["jobs"]["build"]["runs-on"] == "${{ matrix.os }}"


def test_build_job_steps_present(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    assert isinstance(steps, list)
    assert len(steps) == 6


def test_checkout_step_present(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    uses_list = [step.get("uses") for step in steps if "uses" in step]
    assert any(u.startswith("actions/checkout@") for u in uses_list)


def test_setup_python_step_uses_expected_version(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    setup_python_steps = [
        step for step in steps if step.get("uses", "").startswith("actions/setup-python@")
    ]
    assert len(setup_python_steps) == 1
    assert setup_python_steps[0]["with"]["python-version"] == "3.12"


def test_install_dependencies_step(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    install_steps = [step for step in steps if step.get("name") == "Install dependencies"]
    assert len(install_steps) == 1
    run_script = install_steps[0]["run"]
    assert "pip install -r requirements.txt" in run_script
    assert "pip install pyinstaller" in run_script


def test_build_step_invokes_pyinstaller(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    build_steps = [step for step in steps if step.get("name") == "Build"]
    assert len(build_steps) == 1
    run_script = build_steps[0]["run"]
    assert "pyinstaller --onefile --name psw ./src/psw/__main__.py" in run_script


def test_upload_artifact_step(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    upload_steps = [step for step in steps if step.get("name") == "Upload artifact"]
    assert len(upload_steps) == 1
    step = upload_steps[0]
    assert step["uses"].startswith("actions/upload-artifact@")
    assert step["with"]["name"] == "psw-${{ matrix.os }}"
    assert step["with"]["path"] == "dist/psw*"


def test_release_step(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    release_steps = [step for step in steps if step.get("name") == "Release"]
    assert len(release_steps) == 1
    step = release_steps[0]
    assert step["uses"].startswith("softprops/action-gh-release@")
    assert step["with"]["files"] == "dist/psw*"


def test_step_order(workflow):
    steps = workflow["jobs"]["build"]["steps"]
    names_or_uses = [step.get("name") or step.get("uses") for step in steps]

    assert len(names_or_uses) == 6
    assert names_or_uses[0].startswith("actions/checkout@")
    assert names_or_uses[1].startswith("actions/setup-python@")
    assert names_or_uses[2] == "Install dependencies"
    assert names_or_uses[3] == "Build"
    assert names_or_uses[4] == "Upload artifact"
    assert names_or_uses[5] == "Release"


def test_pyinstaller_entrypoint_exists_in_repo():
    entrypoint = os.path.join(
        os.path.dirname(__file__), "..", "src", "psw", "__main__.py"
    )
    assert os.path.isfile(entrypoint)