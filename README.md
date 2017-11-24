# trender - a template-renderer

This repository contains a template renderer.

The template renderer can be configured via the command line.

## Installation

Setup a virtualenv, jump into the virtualenv and install trender:

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .
```

Now you should be able to call trender's help:

```
$ trender --help
Usage: trender [OPTIONS]

Options:
  --services TEXT    path to json file containing a list of services
  --template TEXT    the template that is to render for each service; can be
                     passed multiple times
  --output-dir TEXT  the directory to store rendered templates
  --help             Show this message and exit.
```

## Testing
In order to test the package simply run
```
pytest
```

## Sample Usage

Assume we have the following file `services.json`:
```
[
    {
        "id": "service-1",
        "hostname": "host-1",
        "port": "8080"
    },
    {
        "id": "service-2",
        "hostname": "host-2",
        "port": "9090"
    }
]
```

And Ninja2 templates `template-1`:
```
Template 1
{{ hostname }}
{{ port }}
```

and `template-2`:
```
Template 2
{{ hostname }}
{{ port }}
```

The next call would then render each template for each service:
```
trender.py \
    --services=services.json \
    --template=template-1 \
    --template=template-2 \
    --output-dir=output
```

After this call the `output` directory has the following structure:
```
$ tree output/
output/
├── service-1
│   ├── template-1
│   └── template-2
└── service-2
    ├── template-1
    └── template-2

2 directories, 4 files
```

All the `template-{1|2}` files there are rendered versions of the
files listed above. The values for rendering were taken from
`services.json`.
