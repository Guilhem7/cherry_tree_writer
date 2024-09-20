from setuptools import find_packages, setup

setup(name='cherrytree_writer',
      version='0.3',
      description='Minimalist Python Librairie for writting cherrytree document',
      author='Guilhem RIOUX',
      packages=find_packages(where="src"),
      package_dir={"": "src"}
     )
