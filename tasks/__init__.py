import os
import sys

from invoke import Collection, task as ctask

from . import arch
from . import linux
from . import imalison
from . import osx
from .util import DOTFILES_DIRECTORY, RESOURCES_DIRECTORY, TASKS_DIRECTORY, link_filenames


ns = Collection()
ns.add_collection(osx)
ns.add_collection(linux)
ns.add_collection(arch)
ns.add_collection(imalison.tasks_from_directory(
    os.path.join(TASKS_DIRECTORY, "shell"))
)


@ctask(default=True)
def setup(ctx):
    ctx.config['run']['pty'] = False
    ctx.config['run']['warn'] = True
    if 'darwin' in sys.platform:
        osx.setup(ctx)
    else:
        linux.setup(ctx)
    dotfiles(ctx)
    python(ctx)
    fix_pip(ctx)
    install_npm_libraries(ctx)
    change_shell(ctx)


@ctask
def dotfiles(ctx, flags=''):
    ctx.run('hash dotfiles || sudo pip install dotfiles')
    return ctx.run('dotfiles -s{1} -R {0}'.format(DOTFILES_DIRECTORY, flags))


@ctask
def dropbox_dotfiles(ctx, flags='f'):
    ctx.run('hash dotfiles || sudo pip install dotfiles')
    ctx.run('dotfiles -s{1} -R {0}'.format(
        os.path.join(
            os.path.expanduser('~'), 'Dropbox', 'configs', 'dotfiles'
        ),
        flags
    ))


@ctask
def link_emacs(ctx, flags='f'):
    link_filenames(ctx, [('~/Dropbox/configs/custom-before.el', '~/.emacs.d/custom-before.el'),
                         # ('~/Dropbox/configs/elpa', '~/.emacs.d/elpa'),
                         ('~/Dropbox/configs/custom-after.el', '~/.emacs.d/custom-after.el')],
                   force=True)


@ctask
def python(ctx):
    ctx.run('pyenv install 2.7.11')
    ctx.run('pyenv global 2.7.11')
    ctx.run('pip install setuptools --upgrade')
    ctx.run('pip install -r {0}'.format(
        os.path.join(RESOURCES_DIRECTORY, 'requirements.txt')
    ))


@ctask
def install_npm_libraries(ctx):
    ctx.run('source {0}'.format(
        os.path.join(RESOURCES_DIRECTORY, 'npm.sh')
    ))



@ctask
def change_shell(ctx):
    ctx.run('sudo chsh -s $(which zsh) $(whoami)')


@ctask
def link_dropbox_other(ctx, force=False):
    link_pairs = (
        ('~/Dropbox/Documents', '~/Documents'),
        ('~/Dropbox/Pictures', '~/Pictures'),
        ('~/Dropbox/org', '~/org'),
        ('~/Dropbox/Desktop', '~/Desktop'),
        ('~/Dropbox/ebooks', '~/ebooks'),
    )
    link_filenames(ctx, link_pairs, force)


@ctask
def customize_user_settings(ctx):
    input_function = input if sys.version_info.major == 3 else raw_input
    username = input_function("Enter the user's full name: ")
    email = input_function("Enter the user's email address: ")
    with open(os.path.expanduser('~/.gitconfig.custom'), 'w') as custom_file:
        custom_file.write("""[user]
        name = {0}
        email = {1}""".format(username, email))


@ctask
def fix_pip(ctx):
    ctx.run("sudo easy_install -U pip")
    ctx.run("sudo chown $(whoami) ~/.pip/download_cache -R")


@ctask
def fix_dropbox_permissions(ctx):
    ctx.run("sudo chown -R $(whoami) ~/.ssh")
    ctx.run("sudo chown -R $(whoami) $(readlink -f ~/.ssh)")
    ctx.run("sudo chmod -R 700 ~/.ssh")
    ctx.run("sudo chmod -R 700 $(readlink -f ~/.ssh)")
    ctx.run("sudo chmod -R 700 ~/Dropbox/auth/foolery.pem")
    ctx.run("sudo chmod -R 700 ~/Dropbox/configs/dotfiles/gnupg")


@ctask
def cabal_for_emacs(ctx):
    ctx.run("cabal install happy hasktags stylish-haskell present ghc-mod hlint hoogle structured-haskell-mode hindent")


ns.add_task(fix_pip)
ns.add_task(change_shell)
ns.add_task(customize_user_settings)
ns.add_task(dotfiles)
ns.add_task(dropbox_dotfiles)
ns.add_task(install_npm_libraries)
ns.add_task(python)
ns.add_task(link_dropbox_other)
ns.add_task(setup)
ns.add_task(fix_dropbox_permissions)
ns.add_task(link_emacs)
