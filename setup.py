from setuptools import find_packages, setup


def requirements():
    req_path = 'requirements.txt'
    with open(req_path) as f:
        reqs = f.read().splitlines()
    return reqs


setup(name='betfund',
      version='1.0.0',
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False,
      install_requires=requirements())
