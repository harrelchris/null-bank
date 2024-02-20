# Dump

```shell
python app/manage.py dumpdata accounts --indent 2 --output app/accounts/fixtures/accounts.json
```

# Load

```shell
python app/manage.py loaddata app/accounts/fixtures/accounts.json
```
