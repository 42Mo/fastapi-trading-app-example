class OrderNotFoundError(Exception):
    """Exception raised when an order is not found."""
    def __init__(self, order_id: str, message: str = "Order not found"):
        self.order_id = order_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.order_id} -> {self.message}'
