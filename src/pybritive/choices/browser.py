import os
import click

# eval example: eval $(pybritive checkout test -m env)

browser_choices = click.Choice(
    [
        c
        for c in [
            'mozilla',
            'firefox',
            'windows-default',
            'macosx',
            'safari',
            'chrome',
            'chromium',
            os.getenv('PYBRITIVE_BROWSER'),
        ]
        if c
    ],
    case_sensitive=False,
)
