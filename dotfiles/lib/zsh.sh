source_directory_files "$HOME/.lib/zsh"

alias srczsh="source ~/.zshrc"
alias zshenv="source ~/.zshenv"

# Online help.
unalias run-help 2> /dev/null 1>/dev/null
autoload run-help
HELPDIR=/usr/local/share/zsh/helpfiles

function if_emacs_zsh {
    if [ -z $(echo "$INSIDE_EMACS" | grep comint) ]; then
        set_my_prompt
    else
        PS1="$ "
    fi
}

environment_variable_exists INSIDE_EMACS && if_emacs_zsh || set_default_prompt

environment_variable_exists INSIDE_EMACS && export PROMPT='$ '
