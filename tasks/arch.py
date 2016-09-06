from invoke import task

from .util import RESOURCES_DIRECTORY


ARCH_PACKAGES = [
    "synergy", "adobe-source-code-pro-fonts", "pyenv", "rbenv", "alsa-utils",
    "patch", "spotify", "google-chrome", "autoconf", "automake", "cask", "emacs25-git",
    "xmobar", "the_silver_searcher", "jdk8-openjdk", "openjdk8-doc", "openjdk8-src",
    "scala", "clojure", "go", "ruby", "node", "ghc", "rust",
]


@task
def install_pacaur(ctx):
    ctx.run(os.path.join(RESOURCES_DIRECTORY, "install_pacaur.sh"))
