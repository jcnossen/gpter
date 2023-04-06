from setuptools import setup, find_packages

setup(
    name='gpter',
    version='0.1.0',
    description='A Jupyter Notebook integration for OpenAI GPT API',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/gpter',
    packages=find_packages(),
    install_requires=[
        'openai',
        'IPython',
        'ipywidgets'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
