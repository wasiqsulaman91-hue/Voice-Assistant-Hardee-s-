from livekit.agents import Agent, function_tool, RunContext
from rag import search_menu_items, find_menu_item

ADVANCE_PAYMENT_THRESHOLD = 5000
MINIMUM_ADVANCE_PAYMENT = 1500


class RestaurantAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a phone voice assistant for Hardee's restaurant. "
                "Listen carefully to what the caller wants and follow one of two paths:\n\n"

                "PATH 1 — PLACING AN ORDER:\n"
                "1. Use search_menu if the customer is unsure what to order.\n"
                "2. Use add_item whenever they confirm an item.\n"
                "3. When they finish ordering, use view_order.\n"
                "4. Ask if it's delivery or pickup and call set_order_type.\n"
                "5. Ask for payment method and call set_payment_method.\n"
                "6. If COD requires an advance payment, ask for the amount and call record_advance_payment.\n"
                "7. Finally call confirm_order.\n\n"

                "PATH 2 — RESERVATION:\n"
                "1. Ask ONLY for the customer's name first.\n"
                "2. After receiving the name, ask ONLY for the reservation date.\n"
                "3. After receiving the date, ask ONLY for the reservation time.\n"
                "4. After receiving the time, ask ONLY for the number of people.\n"
                "5. Never ask for more than one missing piece of information in the same response.\n"
                "6. Once all four details are collected, call make_reservation.\n\n"

                "Always use tools instead of pretending you performed an action."
            )
        )

        self.cart = []
        self.order_type = None
        self.payment_method = None
        self.advance_paid = 0.0

    # ---------------- MENU ----------------

    @function_tool(description="Search the restaurant menu")
    async def search_menu(self, context: RunContext, query: str) -> str:
        results = search_menu_items(query, top_k=3)

        if not results:
            return "Sorry, we don't have anything matching that."

        lines = [
            f"{r['name']} ({r['price_text']}): {r['description']}"
            for r in results
        ]

        return "Here are some menu items:\n" + "\n".join(lines)

    # ---------------- CART ----------------

    @function_tool(description="Add an item to the customer's order")
    async def add_item(
        self,
        context: RunContext,
        item_name: str,
        quantity: int = 1,
    ) -> str:

        item = find_menu_item(item_name)

        if not item:
            return f"I couldn't find {item_name}."

        self.cart.append(
            {
                "name": item["name"],
                "price_text": item["price_text"],
                "quantity": quantity,
            }
        )

        return f"Added {quantity} x {item['name']}."

    @function_tool(description="View the current order")
    async def view_order(self, context: RunContext) -> str:

        if not self.cart:
            return "The order is empty."

        lines = []

        for item in self.cart:
            lines.append(
                f"{item['quantity']} x {item['name']} ({item['price_text']})"
            )

        total = self._estimate_total()

        return (
            "Current order:\n"
            + "\n".join(lines)
            + f"\nEstimated total: {total} PKR"
        )

    def _estimate_total(self):
        total = 0

        for item in self.cart:
            price = "".join(
                c
                for c in item["price_text"].split(",")[0]
                if c.isdigit() or c == "."
            )

            try:
                total += float(price) * item["quantity"]
            except ValueError:
                pass

        return total

    # ---------------- ORDER TYPE ----------------

    @function_tool(description="Set order type")
    async def set_order_type(
        self,
        context: RunContext,
        order_type: str,
    ) -> str:

        order_type = order_type.lower()

        if order_type not in ("delivery", "reservation"):
            return "Order type must be delivery or reservation."

        self.order_type = order_type

        return f"Order type set to {order_type}."

    # ---------------- RESERVATION ----------------

    @function_tool(description="Make a table reservation")
    async def make_reservation(
        self,
        context: RunContext,
        date: str,
        time: str,
        party_size: int,
        customer_name: str,
    ) -> str:

        self.order_type = "reservation"

        return (
            f"Reservation confirmed for {customer_name}, "
            f"{party_size} people on {date} at {time}."
        )

    # ---------------- PAYMENT ----------------

    @function_tool(description="Set payment method")
    async def set_payment_method(
        self,
        context: RunContext,
        method: str,
    ) -> str:

        method = method.lower()

        if method not in ("cod", "card"):
            return "Payment must be COD or card."

        self.payment_method = method

        total = self._estimate_total()

        if (
            method == "cod"
            and total >= ADVANCE_PAYMENT_THRESHOLD
        ):
            return (
                f"Orders above {ADVANCE_PAYMENT_THRESHOLD} PKR require "
                f"an advance payment of at least "
                f"{MINIMUM_ADVANCE_PAYMENT} PKR."
            )

        return f"Payment method set to {method}."

    @function_tool(description="Record advance payment")
    async def record_advance_payment(
        self,
        context: RunContext,
        amount: float,
    ) -> str:

        if amount < MINIMUM_ADVANCE_PAYMENT:
            return (
                f"Minimum advance is "
                f"{MINIMUM_ADVANCE_PAYMENT} PKR."
            )

        self.advance_paid = amount

        return f"Advance payment of {amount} PKR recorded."

    # ---------------- CONFIRM ----------------

    @function_tool(description="Confirm the order")
    async def confirm_order(self, context: RunContext) -> str:

        total = self._estimate_total()

        if self.order_type == "delivery":

            if (
                self.payment_method == "cod"
                and total >= ADVANCE_PAYMENT_THRESHOLD
                and self.advance_paid < MINIMUM_ADVANCE_PAYMENT
            ):
                return "Advance payment is still required."

            return (
                f"Order confirmed! "
                f"Total: {total} PKR."
            )

        return "Reservation confirmed."