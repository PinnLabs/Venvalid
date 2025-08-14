<p align="center">
  <img src="./public/logo.png" alt="Venvalid logo" width="200"/>
</p>
<p align="center">
  <a href="https://pepy.tech/projects/venvalid">
    <img src="https://static.pepy.tech/badge/venvalid" alt="PyPI Downloads">
  </a>
</p>
<p align="center">Minimalist environment variable validation for Python, inspired by <a href="https://github.com/af/envalid">envalid</a></p>

---

## About

**Venvalid** is a minimalist and developer-friendly environment variable validator for Python — inspired by the simplicity and clarity of [`envalid`](https://github.com/af/envalid) from the Node.js world.

It lets you define a schema for your environment variables and ensures they are present, well-formed, and ready to use — before your app even starts.

---

## Why Venvalid?

Venvalid was designed with Python developers in mind, offering a modern, clean, and extensible API to handle `.env` configurations. It stands out from other libraries by:

- ✅ Using **Python native types** (`str`, `bool`, `int`, `list`, `Path`, `Decimal`, `datetime`, etc.)
- ✅ Supporting **default values**, **enum constraints**, and **custom validation**
- ✅ Allowing **custom dotenv loading** with override support
- ✅ Raising clear and styled error messages that prevent app boot on misconfig
- ✅ Having zero external dependencies — just Python

---

## Installation

```bash
pip install venvalid
```

or

```bash
uv add venvalid
```

---

## Quick Example

```python
from venvalid import str_, int_, bool_, venvalid
from venvalid.dotenv import load_env_file

# Define schema
config = venvalid({
    "DEBUG": bool_(default=False),
    "PORT": int_(default=8000),
    "SECRET_KEY": str_(),
    "ENVIRONMENT": str_(allowed=["dev", "prod", "test"], default="dev"),
})

print(config["DEBUG"])        # -> False
print(config["PORT"])         # -> 8000
print(config["ENVIRONMENT"])  # -> "dev"
```

---

## Usage

You can use `venvalid` to validate configuration before mounting the app:

```python
from fastapi import FastAPI
from venvalid import str_, int_, bool_, venvalid
from venvalid.dotenv import load_env_file

config = venvalid({
    "DEBUG": bool_(default=False),
    "PORT": int_(default=8000),
    "ENVIRONMENT": str_(allowed=["dev", "prod", "test"], default="dev"),
})

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "env": config["ENVIRONMENT"],
        "debug": config["DEBUG"],
        "port": config["PORT"],
    }
```

---

## Supported Types

You can use both built-in types and helper functions:

- `str`, `int`, `bool`, `list`
- `path_()` → for `pathlib.Path`
- `decimal_()` → for `Decimal`
- `datetime_()` → for `datetime`
- `json_()` → for JSON/dict strings

All helpers accept:

- `default=...`
- `allowed=[...]`
- `validate=callable`

---

## Advanced Options

```python
"ENVIRONMENT": str_(allowed=["dev", "prod"], default="dev"),
"FEATURE_FLAG": bool_(default=False),
"API_KEY": str_(validate=lambda v: v.startswith("sk-")),
```

If any variable is missing or invalid, `venvalid` will stop execution and print a meaningful error message.

---

## .env Loading

If you want to load variables from a `.env` file (without relying on `python-dotenv`), use:

```python
from venvalid.dotenv import load_env_file

load_env_file(".env")             # default
load_env_file(".env.prod", override=True)  # optional override
```
