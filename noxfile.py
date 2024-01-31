"""All the process that can be run using nox.

The nox run are build in isolated environment that will be stored in .nox. to force the venv update, remove the .nox/xxx folder.
"""

import nox

nox.options.sessions = ["lint", "test", "docs", "mypy"]


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commits."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(reuse_venv=True)
def test(session):
    """Run the selected tests and report coverage in html."""
    session.install(".[test]")
    test_files = session.posargs or ["tests"]
    session.run("pytest", "--color=yes", "--cov", "--cov-report=html", *test_files)


@nox.session(reuse_venv=True, name="ci-test")
def ci_test(session):
    """Run all the test and report coverage in xml."""
    session.install(".[test]")
    session.posargs[0] if session.posargs else "default"
    session.run("pytest", "--color=yes", "--cov", "--cov-report=xml")


@nox.session(reuse_venv=True, name="dead-fixtures")
def dead_fixtures(session):
    """Check for dead fixtures within the tests."""
    session.install(".[test]")
    session.run("pytest", "--dead-fixtures")


@nox.session(reuse_venv=True)
def docs(session):
    """Build the documentation."""
    build = session.posargs.pop() if session.posargs else "html"
    session.install(".[doc]")
    dst, warn = f"docs/_build/{build}", "warnings.txt"
    session.run("sphinx-build", "-v", "-b", build, "docs", dst, "-w", warn)
    session.run("python", "tests/check_warnings.py")


@nox.session(name="mypy", reuse_venv=True)
def mypy(session):
    """Run a mypy check of the lib."""
    session.install("mypy")
    test_files = session.posargs or ["sphinxcontrib/skeleton"]
    session.run("mypy", *test_files)