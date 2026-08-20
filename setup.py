from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="branboos_erp",
    version="0.1.0",
    description="Branboos ERP customizations for Frappe / ERPNext",
    author="Branboos",
    author_email="dev@branboos.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
