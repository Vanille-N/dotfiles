#! /bin/bash -i

. $HOME/.env/macros-sync.sh

root $HOME

from++ .env
  from++ shell
    sym .bashrc bashrc
    sym .bash_profile profile
    sym .inputrc inputrc
    sym .vimrc vimrc
    sym .xinitrc xinitrc
  from-- shell
  from++ git
    sym .git-credentials credentials
    sym .git_template template
    sym .gitconfig config
  from-- git
  into++ .config
    sym starship.toml starship.toml
    sym alacritty alacritty
    sym bottom bottom
    sym dunst dunst
    sym zathura zathura
    sym mimeapps.list mimeapps.list
    into++ i3
      sym config i3/config
    into-- i3
    sym i3status-rust i3status-rust
  into-- .config
  into++ .mutt
    from++ mutt
      sym muttrc muttrc
    from-- mutt
  into-- .mutt
  from++ scripts
    run launcher/gen.py
    run controls/gen.py
    run sysmenu/gen.py
  from-- scripts
from-- .env

close
