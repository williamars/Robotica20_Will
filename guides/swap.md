# Como criar um arquivo de swap

Um arquivo de *swap* serve como memória virtual e complementa a memória do sistema.

Primeiro crie um arquivo vazio. Vamos criar um swap de 8GB

	sudo dd if=/dev/zero of=/swapfile bs=1m count=8192

Agora vamos transformar o arquivo em um arquivo de *swap*:

	sudo mkswap /swapfile

E por último vamos ativá-lo:

	sudo swapon swapfile

Caso você deseje usar o arquivo de swap sempre, edite o */etc/fstab* para que o *swap* seja ativado no *boot*:


	sudo code /etc/fstab

Adicione isto ao arquivo:

	/swapfile swap swap defaults 0 0


Salve e reinicie.

**Obs.:**: substitua o `code` no comando acima pelo editor que você quiser usar. Por exemplo `subl` se usar o [Sublime](https://woliveiras.com.br/posts/instalando-o-sublime-text-no-ubuntu/).
