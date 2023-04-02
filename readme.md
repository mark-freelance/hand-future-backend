# Hand-Future Backend

## todo

-[ ] fix init notion avatar key error
-[ ] reconstruct user based on hero model

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
