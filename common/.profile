# ~/.profile -- Defines environment variables not specific to any shell.

export ENV="$HOME/.shrc"

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
export CPATH="$HOME/.local/include:$CPATH"
export LIBRARY_PATH="$HOME/.local/lib:$LIBRARY_PATH"
export LD_LIBRARY_PATH="$HOME/.local/lib:$LD_LIBRARY_PATH"
# MANPATH: we need to think about this again; whereis

export HOSTALIASES="$HOME/.local/etc/hosts"

# TODO: let's decide on these based on availability: vim, nano, vi
# ~requires vim
export VISUAL=vim
export EDITOR=vim

export PYTHONSTARTUP="$HOME/lib/python-startup-loader.py"

# Platform-specific .profile
[[ -r "$HOME/.profile.plat" ]] &&
    . "$HOME/.profile.plat" || :
