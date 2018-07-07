My pale blue dotfiles
=====================

*That's here, that's us, that's $HOME...*

I manage my dotfiles with `symlink-gardener`_, which is a tool I made
because I was unhappy with existing tools that people use for dotfile
management (like GNU stow).

I use keybase's encrypted git repo hosting to store my private dotfiles
(which contain things like passwords).

Currently, my vim configuration is in a separate repo (see
https://github.com/benburrill/.vim).  Eventually, I would like to
transfer it here while preserving the version history.

Installation
------------

The setup script depends on ``bash``, ``coreutils``, ``python>=3.6``,
``perl``, and ``wget``.

The setup script installs the base dotfile packages (common and
optionally secrets) in addition to any platform-specific package passed
as a command line argument.  So setting up dotfiles for a platform that
uses xfce would look like this:

.. code:: shell

    $ ./setup xfce

The setup is (or should be) non-destructive.  When there are conflicts,
old files will be backed up to ``~/.symlink-garden/weeds/``, creating
weed packages which can be re-installed with gardener to shadow the new
dotfiles.

When the setup is finished, a list of requirements is generated (and
saved to ``requires.list``) based on ``# ~requires`` comments I scatter
throughout my dotfiles.  This is a human-readable reminder of things to
install, although the names are often similar to those used by actual
package managers.  The importance of installing these "requirements"
varies.  You can grep around for ``~requires x`` to get an idea for how
each package is used.

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. Links
.. _symlink-gardener: https://github.com/benburrill/gardener
