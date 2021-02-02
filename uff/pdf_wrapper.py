import subprocess


def from_string(input, path):
    try:
        subprocess.run(["wkhtmltopdf", "-", path], input=input.encode("utf-8"), stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        # If wkhtmltopdf is not installed, just ignore it
        pass
