from setuptools import setup, find_packages

setup(
    name="fastapi-blog",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "gunicorn",
        "psycopg2-binary",
        "sqlalchemy",
        "alembic",
    ],
)
