import requests
from django.utils.timezone import datetime


def sympla_service(
            url: str,
            s_token: str,
            page_size: int,
            page: int
        ) -> list[dict]:
    headers: dict[str] = {'s_token': s_token}

    try:
        paginated_url: str = f'{url}?page={page}&page_size={page_size}'
        response = requests.get(paginated_url, headers=headers, timeout=10)

        response.raise_for_status()

        try:
            response_json = response.json()

        except requests.exceptions.Timeout:
            raise TimeoutError(
                "A requisição expirou."
            )

        except requests.exceptions.HTTPError as e:
            raise ConnectionError(
                f"Erro HTTP: {e.response.reason}"
            )

        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Erro de conexão com a API Sympla: {str(e)}"
            )

        except ValueError:
            raise ValueError(
                "Erro ao fazer parse do Json"
            )

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f'Erro na requisição: {e}'
        )

    data_event: list = [
        normalize_data(data) for data in response_json.get('data', [])
    ]

    return data_event


def normalize_data(data: dict) -> dict[str | datetime]:
    event_name: str = str(data.get('name', '')).strip().title()
    start_date: datetime = data.get('start_date')

    address: dict = data.get('address', {})
    location: dict[str] = {
        'location_name': (
            str(
                'Evento Online' if
                address.get('address_num') == '0'
                else
                address.get('name', 'Local não informado')
                ).strip().title()
        ),
        'city': (
            str(
                None if
                address.get('address_num') == '0'
                else
                address.get('city', 'Cidade não informada')
                ).strip().title()
        )
    }

    category_prim: str = (
        str(data.get('category_prim', {}).get('name', '')).title()
    )
    category_sec: str = (
        str(data.get('category_sec', {}).get('name', '')).title()
    )

    sympla_id: str = (
        str(data.get('id')).strip().lower()
    )

    return {
        "name": event_name,
        "start_date": start_date,
        "location": location,
        "category_prim": category_prim,
        "category_sec": category_sec,
        "sympla_id": sympla_id
    }
