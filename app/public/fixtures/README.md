# Dump

```shell
python app/manage.py dumpdata public.question --indent 2 --output app/public/fixtures/questions.json
```

# Load

```shell
python app/manage.py loaddata app/public/fixtures/questions.json
```
