from setuptools import setup, find_packages

setup(
  name='SanauAutomationSDK',
  version='0.0.1',
  author='L1eN',
  author_email='notfakel1en@gmail.com',
  description='For now the TEST',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/sanau-kz/python-automation-sdk.git',
  packages=find_packages(),
  # install_requires=['requests>=2.25.1'], дополнительные библиотеки которые будут установлены вместе с либой
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='bot automation ',   # Надо изменить
  # project_urls={
  #   'GitHub': 'your_github'
  # },
  python_requires='>=3.6'
)
