from setuptools import setup, find_packages
import os
from pip.req import parse_requirements

about = {}
with open("smarthome/__about__.py") as fp:
    exec(fp.read(), about)


readme = open('README.rst').read()
history = open('CHANGES').read().replace('.. changelog:', '')
install_reqs = parse_requirements(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")), session=False)
reqs = [str(req.req) for req in install_reqs]

setup(name='__package_name__',
      version=about['__version__'],
      description='__description__',
      long_description="{}\n\n{}".format(readme, history),
      author='__author__',
      author_email='__email__',
      url='https://github.com/jraynor910/SmartHome',
      license=about['__license__'],
      packages=find_packages(exclude=['docs']),
      install_requires=reqs,
      keywords=about['__title__'],
      zip_safe=False)
