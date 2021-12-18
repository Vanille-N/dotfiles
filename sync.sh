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
    into++ i3
      sym config i3/config
    into-- i3
    sym i3status-rust i3status-rust
  into-- .config
  from++ scripts
    run launcher
    run controls
    run sysmenu
  from-- scripts
from-- .env

close
