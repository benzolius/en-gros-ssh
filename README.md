en-gros-ssh
===========

Run ssh comands on several machines in parallel


Requirements:
-------------

Python 2.7

pip install futures


Usage:
------


./en_gros_ssh.py -p 24000 -m user@machine -i 3-5 -e 4 -c "ls"
