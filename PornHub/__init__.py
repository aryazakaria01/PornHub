from subprocess import run


__version__ = "2.0.1b4"
__version_code__ = (
    run(["git", "rev-list", "--count", "HEAD"], capture_output=True)
    .stdout.decode()
    .strip()
    or "0"
)
