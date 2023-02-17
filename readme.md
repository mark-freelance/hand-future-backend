# Hand-Future Backend

## todo

- [ ] nginx with build

## install

### dev start by step

```shell
# ensure python3
which python
which python3
python3 -V

# install and activate virtualenv
pip install virtualenv
virtualenv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run
uvicorn main:app --reload --host 0.0.0.0 --port 3001 --workers 4
```

### dev start by script

```shell
# list 
pm2 ls

# start
pm2 start run-hand-future-backend.sh

# stop
pm2 stop run-hand-future-backend.sh

# restart
pm2 restart run-hand-future-backend.sh
```

## tips

### 国内的服务器使用 smtp 服务时不要用 google 的，否则会连不上，用 qq 的就可以；本地可以翻的话倒无所谓

## bugfix

### solved: `AttributeError: module 'lib' has no attribute 'OpenSSL_add_all_algorithms'`

这个问题主要是因为ubuntu系统的openssl的某些依赖没有导致的。

解决方案就是 `pip install -U pyopenssl`

但是在 `virutualenv` 环境中这么装（由于没有系统权限）会不起作用

所以要先 `deactivate` 退出到系统环境中安装，安装之前要

```shell
sudo apt remove python3-pip 
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

参考：https://stackoverflow.com/questions/73830524/attributeerror-module-lib-has-no-attribute-x509-v-flag-cb-issuer-check