### In system via env

```bash
python3 -m flask run --host=0.0.0.0 --port=5000
```

### Docker (POST don't work)

```bash
docker build -t tg-channel-class-backend .
docker run --name tg-channel-class-backend --restart=always -d -p 5000:5000 tg-channel-class-backend
```
