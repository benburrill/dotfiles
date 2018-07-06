[[ -r "/usr/share/bash-completion/bash_completion" ]] &&
    . "/usr/share/bash-completion/bash_completion" || :

[[ -r "$HOME/.prompt" ]] &&
    . "$HOME/.prompt" || :


# Pretty colors
if command -v dircolors > /dev/null
then
    if [[ -r "$HOME/.dir_colors" ]]
    then
        eval "$(dircolors -b "$HOME/.dir_colors")"
    else
        eval "$(dircolors -b)"
    fi

    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias egrep='egrep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias diff='diff --color=auto'
else
    export CLICOLOR=true
fi


# Generally when I type import potato in my shell, I don't intend on
# using the ImageMagick tool to create a PostScript screenshot named
# potato.  This function helpfully insults me if I use import like that.
function import {
    printf "You're trying to import a Python module, aren't you? [y/N] "
    read -rN 1 answer
    echo

    if [[ "${answer,,}" = "y" ]]; then
        echo dumbass
        python -ic "import $*"
    else
        env import "$@"
    fi
}

# Make and move to a directory
function md {
    mkdir -p -- "$1" && cd -- "$1"
}

# Sync the history, optionally around a command
function hist-sync {
    history -a
    "$@"
    local err="$?"
    history -n
    return "$err"
}


# Sync when using commands that involve starting a new shell, but do
# more than just that.
alias inve='hist-sync inve'
alias tmux='hist-sync tmux'

# Prompt before overwrite
alias cp='cp -i'
alias mv='mv -i'

# less with ANSI colors
alias cless='less -R'

# REcursive SEARCH (--color=always for cless)
alias research='grep --color=always --recursive'

# Colorized dmesg search
alias dgrep='dmesg --color=always | grep --color=always'

# Search the POSIX Programmer's Manual, useful for checking POSIX
# compatibility.  This alias is ironically not POSIX.
alias posixman='man -e p'

# Don't let confidential information fall into the wrong hands.
# Really I should just unset HISTFILE, but that's no fun.
alias suicide='kill -9 $$'

# Middle ground between `clear` and `reset`
alias cls='echo -ne "\ec\e[3J"'

# ls aliases which might be convenient if I remembered to use them
alias ll='ls -l'
alias la='ls -lA'

# tree alias similar to la
# ~requires tree
alias tra='tree -a'

# Load extra configuration, typically stuff that slows things down and
# isn't used regularly.
alias extra='. ~/.bash_extra'


# Store unlimited history in ram and persist a lot of it.  When changing
# history options, think about potential effects on the prompt/title.
HISTSIZE=-1
HISTFILESIZE=100000
HISTCONTROL=ignoredups
shopt -s histappend
shopt -s cmdhist

shopt -s checkwinsize
shopt -s expand_aliases


# TODO: put this somewhere better
xhost +local:root > /dev/null 2>&1


# Semicolon at the end so we can easily append no_prompt_style to it.
PROMPT_COMMAND='prompt_conf;'
# fc doesn't work with PS0, but history does!
# ~requires bash>=4.4
PS0='$(status_info "$('\
"HISTTIMEFORMAT=$'\n' history 1 | tail -n1"\
')" | title)'
PS1='\[$(status_info | title)\]\[$PROMPT_BASE_STYLE\]'\
'\[$PROMPT_STATUS_STYLE\]$PROMPT_STATUS\[$PROMPT_BASE_STYLE\]'\
'\[$PROMPT_USER_STYLE\]\u@\H\[$PROMPT_BASE_STYLE\]'\
'\[$PROMPT_STRUCT_STYLE\]:\[$PROMPT_BASE_STYLE\]'\
'\[$PROMPT_PATH_STYLE\]\w\[$PROMPT_BASE_STYLE\]'\
'\[$PROMPT_GIT_STYLE\]$PROMPT_GIT\[$PROMPT_BASE_STYLE\]\n'\
'\[$PROMPT_VENV_STYLE\]$PROMPT_VENV\[$PROMPT_BASE_STYLE\]'\
'\[$PROMPT_USER_STYLE\]$PROMPT_JOBS\$\[$PROMPT_BASE_STYLE\] '
PS2='\[$PROMPT_BASE_STYLE$PROMPT_USER_STYLE\]>\[$PROMPT_BASE_STYLE\] '

# Platform-specific .bashrc
[[ -r "$HOME/.bashrc.plat" ]] &&
    . "$HOME/.bashrc.plat" || :
