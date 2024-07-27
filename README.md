# fastapi-sentinel2
API to query sentinel2 data


## REQUIREMENTS
* docker compose

## 0. About

**FastAPI boilerplate** creates an extendable async API using FastAPI, Pydantic V2, SQLAlchemy 2.0 and PostgreSQL:

- [`FastAPI`](https://fastapi.tiangolo.com): modern Python web framework for building APIs
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/): the most widely used data Python validation library, rewritten in Rust [`(5x-50x faster)`](https://docs.pydantic.dev/latest/blog/pydantic-v2-alpha/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html): Python SQL toolkit and Object Relational Mapper
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database
- [`Redis`](https://redis.io): Open source, in-memory data store used by millions as a cache, message broker and more.
- [`ARQ`](https://arq-docs.helpmanual.io) Job queues and RPC in python with asyncio and redis.
- [`Docker Compose`](https://docs.docker.com/compose/) With a single command, create and start all the services from your configuration.
- [`NGINX`](https://nginx.org/en/) High-performance low resource consumption web server used for Reverse Proxy and Load Balancing.

> \[!TIP\] 
> If you want the `SQLModel` version instead, head to [SQLModel-boilerplate](https://github.com/igorbenav/SQLModel-boilerplate).

## 1. Features

- ⚡️ Fully async
- 🚀 Pydantic V2 and SQLAlchemy 2.0
- 🔐 User authentication with JWT
- 🍪 Cookie based refresh token
- 🏬 Easy redis caching
- 👜 Easy client-side caching
- 🚦 ARQ integration for task queue
- ⚙️ Efficient and robust queries with <a href="https://github.com/igorbenav/fastcrud">fastcrud</a>
- ⎘ Out of the box offset and cursor pagination support with <a href="https://github.com/igorbenav/fastcrud">fastcrud</a>
- 🛑 Rate Limiter dependency
- 👮 FastAPI docs behind authentication and hidden based on the environment
- 🦾 Easily extendable
- 🤸‍♂️ Flexible
- 🚚 Easy running with docker compose
- ⚖️ NGINX Reverse Proxy and Load Balancing

## 2. Running the app

1. Make sure docker and docker compose is installed.

2. Take the clone of the repo
    ```bash
    $ git clone https://github.com/CoderOO7/fastapi-sentinel2
    $ cd fastapi-sentinel2
    ```

3. Create a `.env` file by copying existing `.env.sample` in src folder.
    ```bash
    $ cp ./src/.env.sample ./src/.env
    ```
4. Run docker compose up
    ```bash
    $ docker compose up
    ```

It serve the api on http://localhost:8000 and for api docs visit http://localhost:8000/docs
 