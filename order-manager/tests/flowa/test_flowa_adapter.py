from src.infrastructure import FlowaSimpleOrderAdapter



class TestFlowaAdapter:
    def setup_method(self):
        self.flowa_adapter = FlowaSimpleOrderAdapter()

    def test_create_manage_order(self):
        order_data = {
            "broker": "935",
            "account": "84855",
            "symbol": "BITH11",
            "side": "BUY",
            "quantity": 1,
            "price": 30,
            "order_type": "LIMIT",
            "time_in_force": "GTC"
        }
        order_id = self.flowa_adapter.send_order(order_data)

        order = self.flowa_adapter.get_order(order_id)
        assert isinstance(order, dict)

        update = self.flowa_adapter.update_order(
            order_id, price=34, quantity=3
        )
        assert update

        delete = self.flowa_adapter.cancel_order(order_id)
        assert delete
