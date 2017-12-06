from setuptools import setup


setup(
    name='grow-ext-build-server',
    version='1.0.3',
    license='MIT',
    author='Grow Authors',
    author_email='hello@grow.io',
    packages=[
        'grow_build_server',
    ],
    package_data={
        'grow_build_server': [
            'templates/dist/css/*.css',
            'templates/dist/js/*.js',
            'templates/*.html',
        ],
    },
    install_requires=[
        'bs4',
        'google-api-python-client',
        'google-auth',
        'html2text',
        'jinja2',
        'premailer',
        'requests',
        'requests-toolbelt',
    ],
)
