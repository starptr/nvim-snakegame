source ~/.vimrc
let &runtimepath.=','.escape(expand('<sfile>:p:h'), '\,')
