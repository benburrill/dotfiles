# Ultimately, my hope for this file is for it to define prompt
# components that can be used with multiple shells.  Currently, I am
# assuming bash though since that's all I use, but probably most if not
# all of this will work in zsh (so long as you properly define the
# prompts/terminal title for zsh in the zshrc)

if ! command -v __git_ps1 &> /dev/null
then
    if [[ -r "$HOME/.local/lib/git-prompt.sh" ]]
    then
        . "$HOME/.local/lib/git-prompt.sh"
    else
        alias __git_ps1=:
    fi
fi

# Since prompt_conf contains our own venv indicator, assume that anyone
# sourcing this file does not want the default indicator that `activate`
# provides.
VIRTUAL_ENV_DISABLE_PROMPT=true

# Show extra information in git prompt.
# TODO: Is it possible to make this more concise (like by mixing dirty
# state and untracked files into one symbol)?
GIT_PS1_SHOWDIRTYSTATE=true
GIT_PS1_SHOWUNTRACKEDFILES=true
GIT_PS1_SHOWSTASHSTATE=true

function prompt_conf {
    # Run before each prompt is drawn, defining the components that make
    # up the prompt.

    # Don't run any commands before defining LAST_EXIT!
    # This also means that prompt_conf should always come before
    # no_prompt_style in the PROMPT_COMMAND
    LAST_EXIT="$?"
    LAST_CMD="$(fc -ln -1 | sed 's/^[[:space:]]*//')"

    if [ "$LAST_EXIT" != "0" ]
    then
        PROMPT_STATUS="[$LAST_CMD: $LAST_EXIT]"$'\n'
    else
        PROMPT_STATUS=""
    fi

    if [ -n "$VIRTUAL_ENV" ]
    then
        PROMPT_VENV="{$(basename "$VIRTUAL_ENV")} "
    else
        PROMPT_VENV=""
    fi

    # By running jobs twice in a subshell, we clear away the "Done" jobs
    # without affecting "Done" job notifications from the perspective of
    # the user.  It's a kinda weird hack though.  I wish there was a
    # better way to check for jobs.
    if [ -n "$(jobs > /dev/null; jobs)" ]
    then
        PROMPT_JOBS="&"
    else
        PROMPT_JOBS=""
    fi

    PROMPT_GIT="$(__git_ps1)"

    ####################################################################

    # These styles don't necessarily need to be re-run every time we
    # re-draw the prompt, but putting them here allows us to set colors
    # based on status if we so desire in the future.  Also, if some UNIX
    # deity decided to bless/curse me with root powers somehow without
    # starting a new shell, this would ensure that the style switches
    # appropriately.
    
    # TODO: PROMPT_BASE_STYLE is inadequate for setting an actual base
    # style like a background or something since that style won't get
    # reset at the end of the prompt.

    # reset colors
    PROMPT_BASE_STYLE="$(tput sgr0)"
    # red
    PROMPT_STATUS_STYLE="$(tput setaf 1)"
    # cyan
    PROMPT_GIT_STYLE="$(tput setaf 6)"
    # purple
    PROMPT_VENV_STYLE="$(tput setaf 5)"

    if [ "$EUID" = "0" ]
    then
        # bold red
        PROMPT_USER_STYLE="$(tput bold)$(tput setaf 1)"
        # bold yellow
        PROMPT_STRUCT_STYLE="$(tput bold)$(tput setaf 3)"
        # yellow (usually more orange looking)
        PROMPT_PATH_STYLE="$(tput setaf 3)"
    else
        # bold green
        PROMPT_USER_STYLE="$(tput bold)$(tput setaf 2)"
        # bold cyan
        PROMPT_STRUCT_STYLE="$(tput bold)$(tput setaf 6)"
        # bright blue (the goal is to look like a non-bold version of my
        # ls directory styling, bold generally implies bright)
        # Not all terminals support 16-colors, so ymmv
        PROMPT_PATH_STYLE="$(tput setaf 12)"
    fi
}

function no_prompt_style {
    # Can be added to PROMPT_COMMAND to disable all styling
    # TODO: Is there a dynamic way to do this?
    PROMPT_BASE_STYLE=
    PROMPT_STATUS_STYLE=
    PROMPT_GIT_STYLE=
    PROMPT_VENV_STYLE=
    PROMPT_USER_STYLE=
    PROMPT_STRUCT_STYLE=
    PROMPT_PATH_STYLE=
}

function status_info {
    # Outputs a string representing the current status.  Optionally
    # takes an argument that indicates the currently running command.
    # status_info is mostly (if not exclusively) used to determine what
    # the terminal title should be set to.

    # Use all the arguments just in case
    local cmd="$(echo -n "$*" | sed 's/[[:space:]]*$//')"

    [ -n "$SSH_CONNECTION" ] && echo -n "ssh: "
    [ -n "$cmd" ] && echo -n "($cmd) "
    echo -n "${PWD/#$HOME/\~}"
}
