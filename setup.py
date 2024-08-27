from setuptools import setup, find_packages

# PyPIの説明文にREADME.mdを使うように読み込みをする
with open("README.md", "r", encoding="utf-8") as fp:
    readme = fp.read()

setup(
    name='voxelamming',
    version='0.3.4',
    description='Convert Python code to JSON and send it to the Voxelamming app.',
    author='creativival',
    packages=find_packages(exclude=['.pytest_cache', 'tests', 'test_pypi']),  # 除外するフォルダを指定
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[
        'websocket-client',  # 依存ライブラリをここに指定
    ],
    python_requires='>=3.9',  # Python 3.9 以上を要求
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
