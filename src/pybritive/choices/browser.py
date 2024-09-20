import os

import click

# eval example: eval $(pybritive checkout test -m env)

browser_choices = click.Choice(
    [
        c
        for c in [
            'chrome',
            'chromium',
            'firefox',
            'macosx',
            'mozilla',
            'safari',
            'windows-default',
            os.getenv('PYBRITIVE_BROWSER'),
        ]
        if c
    ],
    case_sensitive=False,
)
