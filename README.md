# python-hydra

python-hydra is a python library based on hydra.


## USE

### ssh 

```python

from hydra.services.ssh import SSHBrute

ssh = SSHBrute(host='127.0.0.1', port=2222)

result = ssh.start(user='root', pwd_file='/var/wordlist/ssh_pass.txt')

# {'host': '127.0.0.1', 'login':'root', 'password': '123456', 'port': 22, 'service': 'ssh'}

```

**Docker Test**

* https://hub.docker.com/r/panubo/sshd


### vnc

```python

from hydra.services.vnc import VNCBrute

vnc = VNCBrute(host='127.0.0.1', port=5900)

result = vnc.start(pwd_file='/var/wordlist/vnc_pass.txt')

# {'host': '127.0.0.1', 'password': '123456', 'port': 5900, 'service': 'vnc'}

```

**Docker Test**

* https://hub.docker.com/r/kaixhin/vnc


### ftp

```python

from hydra.services.ftp import FtpBrute

ftp = FtpBrute(host='127.0.0.1', port=21)

result = ftp.start(user='ftp', pwd_file='/var/wordlist/ftp_pass.txt')

# {'host': '127.0.0.1', 'login':'ftp', 'password': '123456', 'port': 21, 'service': 'ftp'}
```

**Docker Test**

* https://hub.docker.com/r/hauptmedia/proftpd


## SERVICES

* ftp
* ssh
* vnc

