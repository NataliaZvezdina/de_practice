import logging
import requests

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator


class NZvezdina21RamTopLocationsOperator(BaseOperator):

    api_url = 'https://rickandmortyapi.com/api/location'

    template_fields = ("top_cnt",)
    ui_color = '#ccc4f5'

    def __init__(self, top_cnt: int = 3, **kwargs) -> None:
        super().__init__(**kwargs)
        self.top_cnt = top_cnt

    def execute(self, context):
        r = requests.get(self.api_url)
        if r.status_code == 200:
            locations = []
            for record in r.json()['results']:
                location = (record['id'], record['name'], record['type'], record['dimension'], len(record['residents']))
                locations.append(location)

            locations.sort(key=lambda arr: arr[-1], reverse=True)
            return ','.join(map(str, locations[:self.top_cnt]))
        else:
            logging.warning(f"HTTP STATUS {r.status_code}")
            raise AirflowException('Error in load page count')
