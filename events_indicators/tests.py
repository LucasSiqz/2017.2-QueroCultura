from datetime import datetime
from .api_connections import RequestEventsRawData
from .api_connections import RequestEventsInPeriod
from .api_connections import EmptyRequest
from .models import EventData
from .models import EventLanguage
from .models import LastUpdateEventDate
from .views import populate_event_data
from quero_cultura.views import ParserYAML
import requests_mock
import json


class TestLastUpdateEventDate(object):

    def test_last_update_event_date(self):
        LastUpdateEventDate.drop_collection()
        update_date = LastUpdateEventDate()
        create_date = datetime.now().__str__()
        update_date.create_date = create_date
        update_date.save()
        query = LastUpdateEventDate.objects.first()
        assert query.create_date == create_date


class TestEventLanguage(object):

    def test_event_language(self):
        EventLanguage.drop_collection()
        event_language = EventLanguage()
        instance = "SP"
        event_language.instance = instance
        language = "Cinema"
        event_language.language = language
        event_language.save()
        query = EventLanguage.objects.first()
        assert query.instance == instance
        assert query.language == language


class TestEventData(object):

    def test_event_data(self):
        EventData.drop_collection()
        event_data = EventData()
        instance = "SP"
        event_data.instance = instance
        occurrences = [
            {
                "id": 1147,
                "space": {
                    "id": 14191,
                    "acessibilidade": "Sim"
                }
            }
        ]
        event_data.occurrences = occurrences
        date = datetime(2017, 11, 14, 3, 5, 55, 88000)
        event_data.date = date
        age_range = "Livre"
        event_data.age_range = age_range
        event_data.save()
        query = EventData.objects.first()
        assert query.instance == instance
        assert query.occurrences == occurrences
        assert query.date == date
        assert query.age_range == age_range


class TestPopulateEventData(object):

    @requests_mock.Mocker(kw='mock')
    def test_populate_event_data(self, **kwargs):
        parser_yaml = ParserYAML()
        urls = parser_yaml.get_multi_instances_urls

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre",
                   "occurrences":
                   [{"id": 1147, "space": {"id": 14191,
                                           "acessibilidade": "Sim"}}]}]

        for url in urls:
            kwargs['mock'].get(url + "event/find/", text=json.dumps(result))

        LastUpdateEventDate.drop_collection()
        EventLanguage.drop_collection()
        EventData.drop_collection()

        populate_event_data()

        assert LastUpdateEventDate.objects.count() != 0
        assert EventData.objects.count() != 0
        assert EventLanguage.objects.count() != 0


class TestClassRequestEventsRawData(object):

    @requests_mock.Mocker(kw='mock')
    def test_success_request(self, **kwargs):
        current_time = datetime.now().__str__()
        url = "http://mapas.cultura.gov.br/api/"

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        kwargs['mock'].get(url + "event/find/", text=json.dumps(result))

        request_events_raw_data = RequestEventsRawData(current_time, url)
        response_events_raw_data = request_events_raw_data.response
        response_status_code = response_events_raw_data.status_code
        assert response_status_code == 200

    @requests_mock.Mocker(kw='mock')
    def test_data_content(self, **kwargs):
        current_time = datetime.now().__str__()

        url = "http://mapas.cultura.gov.br/api/"

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        kwargs['mock'].get(url + "event/find/", text=json.dumps(result))

        request_events_raw_data = RequestEventsRawData(current_time, url)
        events_raw_data = request_events_raw_data.data
        type_events_raw_data = type(events_raw_data)
        empty_list = []
        assert type_events_raw_data == type(empty_list)

    @requests_mock.Mocker(kw='mock')
    def test_data_lenght(self, **kwargs):
        current_time = datetime.now().__str__()
        url = "http://mapas.cultura.gov.br/api/"

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        kwargs['mock'].get(url + "event/find/", text=json.dumps(result))
        request_events_raw_data = RequestEventsRawData(current_time, url)
        events_raw_data = request_events_raw_data.data_length
        type_events_raw_data = type(events_raw_data)
        intenger = 1
        assert type_events_raw_data == type(intenger)


class TestClassRequestEventsInPeriod(object):

    @requests_mock.Mocker(kw='mock')
    def test_success_request_in_period(self, **kwargs):
        year = 2013
        url = "http://spcultura.prefeitura.sp.gov.br/api/"

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        kwargs['mock'].get(url + "event/find/", text=json.dumps(result))

        request_events_in_period = RequestEventsInPeriod(year, url)
        response_events_in_period = request_events_in_period.response
        response_status_code = response_events_in_period.status_code
        assert response_status_code == 200

    @requests_mock.Mocker(kw='mock')
    def test_data_content(self, **kwargs):
        year = 2013
        url = "http://spcultura.prefeitura.sp.gov.br/api/"

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        kwargs['mock'].get(url + "event/find/", text=json.dumps(result))

        request_events_in_period = RequestEventsInPeriod(year, url)
        events_in_period = request_events_in_period.data
        type_events_in_period = type(events_in_period)
        empty_list = []
        assert type_events_in_period == type(empty_list)

    @requests_mock.Mocker(kw='mock')
    def test_data_lenght(self, **kwargs):
        year = 2013
        url = "http://spcultura.prefeitura.sp.gov.br/api/"

        result = [{"createTimestamp": {"date": "2012-01-01 00:00:00.000000"},
                   "terms": {"linguagem": "Cinema"},
                   "classificacaoEtaria": "livre"}]

        kwargs['mock'].get(url + "event/find/", text=json.dumps(result))
        request_events_in_period = RequestEventsInPeriod(year, url)
        events_in_period = request_events_in_period.data_length
        type_events_in_period = type(events_in_period)
        intenger = 1
        assert type_events_in_period == type(intenger)


class TestEmptyRequest(object):

    def test_request_data(self):
        request = EmptyRequest()

        event_request = request.data
        type_event_request = type(event_request)
        empty_list = []
        assert type_event_request == type(empty_list)

    def test_request_lenght(self):
        request = EmptyRequest()
        events_request = request.data_length
        type_request = type(events_request)
        intenger = 1
        assert type_request == type(intenger)
