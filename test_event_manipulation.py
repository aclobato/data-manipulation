import pandas as pd

from event_manipulation import EventManipulation


class TestEventManipulation:
    def test_result(self):
        data = {"events": [{"event": "comprou-produto", "timestamp": "2016-09-22T13:57:32.2311892-03:00",
                            "custom_data": [{"key": "product_name", "value": "Camisa Azul"},
                                            {"key": "transaction_id", "value": "3029384"},
                                            {"key": "product_price", "value": 100}]},
                           {"event": "comprou", "timestamp": "2016-09-22T13:57:31.2311892-03:00", "revenue": 250,
                            "custom_data": [{"key": "store_name", "value": "Patio Savassi"},
                                            {"key": "transaction_id", "value": "3029384"}]},
                           {"event": "comprou-produto", "timestamp": "2016-09-22T13:57:33.2311892-03:00",
                            "custom_data": [{"key": "product_price", "value": 150},
                                            {"key": "transaction_id", "value": "3029384"},
                                            {"key": "product_name", "value": "Calça Rosa"}]},
                           {"event": "comprou-produto", "timestamp": "2016-10-02T11:37:35.2300892-03:00",
                            "custom_data": [{"key": "transaction_id", "value": "3409340"},
                                            {"key": "product_name", "value": "Tenis Preto"},
                                            {"key": "product_price", "value": 120}]},
                           {"event": "comprou", "timestamp": "2016-10-02T11:37:31.2300892-03:00", "revenue": 120,
                            "custom_data": [{"key": "transaction_id", "value": "3409340"},
                                            {"key": "store_name", "value": "BH Shopping"}]}]}
        event_manipulation = EventManipulation(data);
        result = event_manipulation.transform_to_timeline();
        expected_result = {"timeline": [
            {"timestamp": "2016-10-02T11:37:31.2300892-03:00", "revenue": 120.0, "transaction_id": "3409340",
             "store_name": "BH Shopping", "products": [{"name": "Tenis Preto", "price": 120.0}]},
            {"timestamp": "2016-09-22T13:57:31.2311892-03:00", "revenue": 250.0, "transaction_id": "3029384",
             "store_name": "Patio Savassi",
             "products": [{"name": "Camisa Azul", "price": 100.0}, {"name": "Calça Rosa", "price": 150.0}]}]}
        expected_result_json = pd.DataFrame.from_dict(expected_result).to_json(orient='records')

        assert result == expected_result_json
