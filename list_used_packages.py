"""
Run only if both pipreqs and pip-chill are installed.
pip-chill only lists packages that were explicitly installed by you using pip install, and not those installed as
dependencies of other packages or via requirements.txt
"""


import subprocess

def get_imported_packages():
    # Run pipreqs with --print and capture output
    result = subprocess.run(["pipreqs", ".", "--print"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running pipreqs:", result.stderr)
        return set()
    return set(line.strip().lower() for line in result.stdout.splitlines() if line.strip())

def get_explicit_packages():
    # Run pip-chill and capture output
    result = subprocess.run(["pip-chill"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running pip-chill:", result.stderr)
        return {}
    packages = {}
    for line in result.stdout.splitlines():
        if "==" in line:
            name, version = line.strip().split("==")
            packages[name.lower()] = f"{name}=={version}"
    return packages

def main():
    imported = get_imported_packages()
    print(f"Running 'pipreqs . --print' in the terminal we get Imported packages:\n{imported}")
    installed = get_explicit_packages()
    print(f"Running 'pip-chill' in the terminal we get Installed packages:\n{installed}")

    # Use the commented line when you want to populate only the explicitly installed packages with pip in the terminal
    # used_with_versions = [installed[pkg] for pkg in imported if pkg in installed]
    used_with_versions = [pkg for pkg in imported if pkg in list(installed.values())]

    print("☑️ Used packages with versions:")
    for pkg in sorted(used_with_versions):
        print(pkg)

if __name__ == "__main__":
    main()
