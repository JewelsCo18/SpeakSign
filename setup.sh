#!/bin/bash

DIV="$(python -c "print '\n'+'-'*60+'\n'")"
GIT_REMOTE=""
REPO_NAME=""


if [ -n "$(uname -o | grep Linux)" ]; then
    echo mac only
    exit 1
fi

if [ -z "$(which brew)" ]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

if [ -z "$(which python3)" ]; then
    brew install python3 
fi

if [ -z "$(which virtualenv)" ]; then
    pip3 install virtualenv
fi

[ -d env ] && echo "deleting old virtualenv" && rm -rf env 

echo $DIV
cat << EOF
         _   _   _                             _     _             _
 ___ ___| |_| |_(_)_ _  __ _   _  _ _ __  __ _(_)_ _| |_ _  _ __ _| |___ _ ___ __
(_-</ -_)  _|  _| | ' \/ _\` | | || | '_ \ \ V / | '_|  _| || / _\` | / -_) ' \ V /
/__/\___|\__|\__|_|_||_\__, |  \_,_| .__/  \_/|_|_|  \__|\_,_\__,_|_\___|_||_\_/
                       |___/       |_|
EOF
echo $DIV

pip install virtualenv
virtualenv -p $(which python3) env
source ./env/bin/activate

echo $DIV
cat <<EOF
 _         _        _ _ _                _                       _             _
(_)_ _  __| |_ __ _| | (_)_ _  __ _   __| |___ _ __  ___ _ _  __| |___ _ _  __(_)___ ___
| | ' \(_-<  _/ _\` | | | | ' \/ _\` | / _\` / -_) '_ \/ -_) ' \/ _\` / -_) ' \/ _| / -_|_-<
|_|_||_/__/\__\__,_|_|_|_|_||_\__, | \__,_\___| .__/\___|_||_\__,_\___|_||_\__|_\___/__/
                              |___/           |_|
EOF
echo $DIV

pip install -r requirements.txt

echo $DIV
cat <<EOF
 ___   ___  _  _ ___
|   \ / _ \| \| | __|
| |) | (_) | .\` | _|
|___/ \___/|_|\_|___|

EOF
echo $DIV

cat <<EOF >> ~/.bash_profile
export PS1="\[\033[38;5;196m\]\u\[$(tput sgr0)\]\[\033[38;5;10m\]@\[$(tput sgr0)\]\[\033[38;5;196m\]\h\[$(tput sgr0)\]\[\033[38;5;15m\]:\[$(tput sgr0)\]\[\033[38;5;14m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]\\$\[$(tput sgr0)\]"
EOF

echo "now run \"source activate\" to activate virtualenv"
