import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as rp:
    req = rp.read().splitlines()

setuptools.setup(
    name="wagtail2docx",
    version="0.1",
    author="Samuel MEYNARD",
    author_email="samuel@meyn.fr",
    description="Wagtail app - convert page to docx document",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olopost/wagtail2docx",
    install_requires=req,
    packages=setuptools.find_packages(),
    package_dir={'wagtail2docx': 'wagtail2docx'},
    package_data={
        'wagtail2docx': [
            'templates/*.html',
            'templates/base/*.html'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: OSL-3.0",
        "Operating System :: OS Independent",
    ],
)