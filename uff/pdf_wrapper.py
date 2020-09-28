import subprocess


def from_string(input, path):
    subprocess.run(["wkhtmltopdf", "-", path], input=input.encode("utf-8"), stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
