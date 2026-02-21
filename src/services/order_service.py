def order_confirmation_text(order_id: int) -> str:
    return f'Спасибо! Ваш заказ №{order_id} принят. Мы скоро свяжемся с вами.'


def admin_order_text(order, items) -> str:
    lines = [
        f"🆕 Новый заказ #{order['id']}",
        f"Клиент: {order['customer_name']}",
        f"Телефон: {order['phone']}",
        f"Адрес: {order['address']}",
        f"Комментарий: {order['comment']}",
        'Позиции:',
    ]
    for item in items:
        lines.append(f"- {item['name']} x{item['quantity']} ({item['price']} ₽)")
    lines.append(f"Итого: {order['total_amount']} ₽")
    return '\n'.join(lines)
