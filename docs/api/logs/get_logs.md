# GET API Event
## URL
```url
http://127.0.0.1:8000/logs/public/v1/api/
```

## Value Response
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "batch": 0,
      "message": "string",
      "imported_amount": 2147483647,
      "status": "success",
      "created_at": "2025-07-25T21:42:27.314Z"
    }
  ]
}
```
# Swagger
Possível acessar a documentação do Swagger através do seguinte link:
- `http://127.0.0.1:8000/api/schema/swagger-ui/`
