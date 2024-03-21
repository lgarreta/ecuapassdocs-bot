from setuptools import setup, find_packages

setup(
    name='ecuapassdocs',  # Package name
    version='0.56',  # Package version
    url="https://github.com/lgarreta/ecuapassdocs",
    author='Luis Garreta',
    author_email='lgarreta@gmail.com',
    description='Utils for creating PDFs, loading resources and extracting info from fields in ECUAPASS docs: cartaportes, manifiestos, declaraciones',
    packages=find_packages(),  # Automatically finds packages within the directory
	include_package_data=True, 
	package_data={"ecuapassdocs": ["resources/images/*", 
	                               "resources/data_cartaportes/*",
	                               "resources/data_manifiestos/*",
	                               "resources/data_declaracion/*",
	                               "resources/docs/*"]},
	# List any dependencies here
    install_requires = [
		"PyPDF2==3.0.1",
		"reportlab==4.0.8",
		"Pillow==10.1.0"
	], 
	logs = {"0.56" : "Changed resource names from 'data-XXX' to data_XXX'"},
)
