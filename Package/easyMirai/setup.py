import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyMirai",
    version="1.0.39",
    author="HexMikuMax",
    author_email="sfnco-miku@outlook.com",
    description="帮助QBot开发新手者快速构建简单的QQ机器人",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ExMikuPro/easyMirai",
    packages=find_packages(include=["requests", "rich"]),
    install_requires=[  # 添加了依赖的 package
        "requests",
        "rich",
    ]
)
