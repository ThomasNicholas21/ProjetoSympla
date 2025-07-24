import requests
from pprint import pprint


def sympla_service(url: str, s_token: str) -> list[dict]:
    headers = {'s_token': s_token}
    data_event = []

    try:
        response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status()

        try:
            response_json = response.json()
        except ValueError:
            raise ValueError(
                "Erro ao fazer parse do Json"
            )

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f'Erro na requisição: {e}'
        )

    for data in response_json.get('data', []):
        try:
            event_name = str(data.get('name', '')).strip().title()
            start_date = data.get('start_date')

            address = data.get('address', {})
            location = {
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
                        'Evento Online' if
                        address.get('address_num') == '0'
                        else
                        address.get('city', 'Cidade não informada')
                        ).strip().title()
                )
            }

            category_prim = (
                str(data.get('category_prim', {}).get('name', '')).title()
            )
            category_sec = (
                str(data.get('category_sec', {}).get('name', '')).title()
            )

            sympla_id = (
                str(data.get('id')).strip().lower()
            )

            data_event.append(
                {
                    'name': event_name,
                    'start_date': start_date,
                    'location': location,
                    'category_prim': category_prim,
                    'category_sec': category_sec,
                    'sympla_id': sympla_id
                }
            )

        except Exception as e:
            raise Exception(
                f'Erro ao processar: {e}'
            )

    return data_event


if __name__ == "__main__":
    url = 'https://api.sympla.com.br/public/v1.5.1/events'
    s_token = 'a28e68e547aacfa3426548a989e41e39f3db9d43a2cfe0ab4a261eec6f240b39' # noqa
    data_event = sympla_service(url, s_token) # noqa
    for event in data_event:
        pprint(event)
