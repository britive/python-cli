# Britive CLI - Pure Python Implementation

PyBritive is intended to be used as a CLI application for communicating with the Britive Platform.

## Installation

`pybritive` will be installed via the Python package installer, `pip`.

```sh
pip install pybritive
```

> _NOTE: The end user is free to install the CLI into a virtual environment or in the global scope,_
> _so it is available everywhere._

## Alternate Installation

You can always pull the latest version directly from GitHub using one of the following commands:

```sh
pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest \
    | jq -r '.assets[] | select(.content_type == "application/x-gzip") | .browser_download_url')
```

Or

```sh
pip install $(curl -s https://api.github.com/repos/britive/python-cli/releases/latest \
    | grep "browser_download_url.*.tar.gz" | cut -d : -f 2,3 | tr -d \")
```

## Documentation

* [Britive CLI](https://britive.github.io/python-cli)

## Community Projects

> _NOTE:_
> _Britive, Inc. does not provide support for community projects._
> _Community projects are also not considered when ensuring backwards compatibility for releases._
> _The list below is provided as-is and use of these projects is subject to the licensing/restrictions of each_
> _individual project._

* [`vim-britive`](https://github.com/pbnj/vim-britive)
