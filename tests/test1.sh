mkdir $HOME/.local
mkdir $HOME/.local/{bin,etc,dev,usr,var}

alias /bin=$HOME/.local/bin
alias /etc=$HOME/.local/etc
alias /dev=$HOME/.local/dev
alias /usr=$HOME/.local/usr
alias /var=$HOME/.local/var

touch /bin/test.test
ls $HOME/.local/bin
