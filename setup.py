from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()
setup(
    name='Market',
    version='0.0.1',
    description='Market project',
    long_description=readme,
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['Flask>=0.12.1', 'Flask-API>=0.7.1', 'Flask-SQLAlchemy>=2.2',
                      'pytest>=3.0.7', 'SQLAlchemy>=1.2.0', 'PyJWT==1.4.2',
                      'Werkzeug>=0.12.1','bcrypt==3.1.3', 'Flask-Bcrypt==0.7.1',
                      'mysqlclient==1.3.13', 'flask-restful==0.3.6', 'flask-cors==3.0.6'],
    author='Kevin Zhao',
    author_email='mingyuezhao@gmail.com',
    url='https://github.com/rhtbapat/BasicStructure',
    license=license,
    packages=find_packages()
)
