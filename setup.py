from distutils.core import setup


setup(
    name='django-googleauth',
    version='1.0',
    description='',
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    license='WTFPL',
    url='http://github.com/sdfsdhgjkbmnmxc/django-googleauth',
    packages=[
        'googleauth',
    ],
    requires=open('requirements.txt').readlines(),
)
