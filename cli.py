import logging
from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_inputs
from bot.logging_config import setup_logger


def get_input():
    symbol = input("Enter Symbol (BTCUSDT): ").upper()
    side = input("Enter Side (BUY/SELL): ").upper()
    order_type = input("Enter Order Type (MARKET/LIMIT/STOP): ").upper()
    quantity = float(input("Enter Quantity: "))

    price = None
    stop_price = None

    if order_type == "LIMIT":
        price = float(input("Enter Price: "))

    elif order_type == "STOP":
        stop_price = float(input("Enter Stop Price: "))
        price = float(input("Enter Limit Price: "))

    return symbol, side, order_type, quantity, price, stop_price


def print_summary(symbol, side, order_type, quantity, price, stop_price):
    print("\n----------------------------------")
    print("📊 Order Summary")
    print("----------------------------------")
    print(f"Symbol   : {symbol}")
    print(f"Side     : {side}")
    print(f"Type     : {order_type}")
    print(f"Quantity : {quantity}")
    print(f"Price    : {price if price else '-'}")
    if stop_price:
        print(f"Stop     : {stop_price}")


def print_response(order):
    print("\n----------------------------------")
    print("📥 Response")
    print("----------------------------------")
    print(f"Order ID     : {order.get('orderId')}")
    print(f"Status       : {order.get('status')}")
    print(f"Executed Qty : {order.get('executedQty')}")
    print(f"Avg Price    : {order.get('avgPrice', 'N/A')}")


def main():
    setup_logger()
    client = get_client()

    while True:
        print("\n🚀 Binance Futures Trading Bot")
        print("----------------------------------")
        print("1. Place Order")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                symbol, side, order_type, quantity, price, stop_price = get_input()

                validate_inputs(symbol, side, order_type, quantity, price, stop_price)

                print_summary(symbol, side, order_type, quantity, price, stop_price)

                confirm = input("\nConfirm order? (y/n): ").lower()
                if confirm != "y":
                    print("❌ Order cancelled")
                    continue

                print("\nPlacing order...")

                order = place_order(
                    client,
                    symbol,
                    side,
                    order_type,
                    quantity,
                    price,
                    stop_price
                )

                if "error" in order:
                    print("❌ Failed:", order["error"])
                    logging.error(order["error"])
                else:
                    print_response(order)
                    print("\n✅ Order placed successfully!")
                    logging.info(order)

            except Exception as e:
                print("❌ Error:", str(e))
                logging.error(str(e))

        elif choice == "2":
            print("👋 Exiting...")
            break

        else:
            print("⚠️ Invalid choice")


if __name__ == "__main__":
    main()