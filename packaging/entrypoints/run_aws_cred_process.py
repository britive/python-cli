"""Frozen entry point for the `pybritive-aws-cred-process` helper.

Invoked by the AWS SDKs via the `credential_process` directive, so it runs on
every credential refresh. Kept as a thin shim over the pip console script.
"""

from pybritive.helpers.aws_credential_process import main

if __name__ == '__main__':
    main()
