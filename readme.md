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
pm2 start run.sh

# stop
pm2 stop run.sh

# restart
pm2 restart run.sh
```
