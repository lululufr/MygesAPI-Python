# MYGES API HANDLER

## 1 - renseigner vos identifiants
Modifier le fichier [.env](.env.example)

```
cp .env.example .env
nano .env

```

## 2 - Go request 

```python
api = MyGesAPI()
print(api.get_profile())

```
