

## Notebooks

I am working on a dockerized container for this
[here](https://github.com/eric-downes/jupyter_coq_cpp_py_hs_scala)
until that is ready, the following at least works on my system.

To get the multilanguage notebooks running on MacOS, we will be using
the software below; I have gathered everything together for my system
(MacOS silicon Ventura), but if you run into an issue on your system
you can refer here.

- [homebrew](https://brew.sh/)
- [pyenv](https://github.com/pyenv/pyenv)
- [jupyter-lab](https://jupyter.org/install)
- [scala](https://www.scala-lang.org/download/)
- [almond](https://almond.sh/docs/quick-start-install)
- [Haskell](https://www.haskell.org/downloads/)
- [coq](https://coq.inria.fr/download)

### system setup
1. install homebrew (`which brew` on command line tells if you already have it)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
1. install many packages
```
brew install zeromq libmagic cairo pkg-config haskell-stack pango nodejs openjdk scala
brew link coursier
```

### Python setup

If you're already happy with your python setup, in this directory:
```
python3 -m pip install -r requirements.txt
```
Then skip to next section.

Otherwise, I recommend `pyenv`.
1. install pyenv for managing all python versions without depending on python itself.
```bash
brew install pyenv
pyenv init
```
- this will tell you to add (something like) the following to your shell profiles:
```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```
- Your current `system` python version can be seen by executing
`pyenv versions`; you can always rerturn to it with `pyenv shell system`

- Then execute `source ~/.bashrc` or whatever your shell profile is

1. Install python 3.10.0 `pyenv install 3.10.0`

- You can set it as the default globally
`echo 3.10.0 > ~/.pyenv/version`
- or in the current shell `pyenv shell 3.10.0`


### Jupyter Multi-language

1. From the requirements.txt above you should already have `jupyter`
and `jupyter-lab`; you may need to refresh your shell or open a new
one; you should now see something like
```
which jupyter
# ~/.pyenv/shims/jupyter
```

1. Setup and configure jupyter for multi-language
```
jupyter contrib nbextension install 
jupyter nbextensions_configurator enable
jupyter labextension install transient-display-data
jupyter labextension install jupyterlab-sos
```

### Languages - Scala - Haskell - Coq

1. Install `almond` the jupyter scala-kernel, using `coursier` which
we installed and linked with `brew`:
```coursier launch --fork almond -- --install```

1. install `iHaskell` telling stack to pay attention to homebrew directories
```
stack install --fast --extra-include-dirs ${HOMEBREW_PREFIX}/include \
      --extra-lib-dirs ${HOMEBREW_PREFIX}/lib
```
1. Configure `coq-jupyter` package
```python3 -m coq_jupyter.install```

###  Test

