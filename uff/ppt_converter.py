import subprocess


def convert_to_pdf(ppt_input, pdf_output):
    try:
        subprocess.run(["unoconv", "-o", pdf_output, ppt_input], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        # If unoconv is not installed, just ignore it
        pass
