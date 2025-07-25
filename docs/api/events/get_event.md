# GET API Event
## URL
```url
http://127.0.0.1:8000/eventos/public/v1/api/
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
      "name": "string",
      "start_date": "2025-07-25T21:40:20.859Z",
      "location": {
        "location_name": "string",
        "city": "string"
      },
      "category": [
        {
          "name": "string"
        }
      ],
      "sympla_id": "string",
      "batch": 0
    }
  ]
}
```

# GET API Csv
## URL
```url
http://127.0.0.1:8000/eventos/dump/v1/api/export-csv/
```

Irá gerar um arquivo CSV com a seguinte disposição de dados:
```csv
ID, Nome, Data de Início, Local, Cidade, Categorias (separadas por vírgula),Sympla, ID do Batch
```

# Swagger
Possível acessar a documentação do Swagger através do seguinte link:
- `http://127.0.0.1:8000/api/schema/swagger-ui/`
