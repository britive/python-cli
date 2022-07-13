## Local Install

~~~
pip install --editable .
~~~

## Build

* Update version in `setup.cfg`
* Push code to GitHub
* Cut a new PR and merge when appropriate
* Run below commands


~~~
python -m pip install --upgrade build
python -m build
~~~

* Cut a new release in GitHub with the version tag
* Add the assets from `dist` directory to the release