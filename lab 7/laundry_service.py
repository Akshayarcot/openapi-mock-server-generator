def parse_order(text):
    if not isinstance(text, str):
        return None
    if ':' not in text:
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    garment = parts[0].strip()
    kg_str = parts[1].strip()
    if not garment:
        return None
    try:
        kg = float(kg_str)
    except (ValueError, TypeError):
        return None
    if kg < 0:
        return None
    return garment.title(), kg


def weight_average(weights_csv):
    if not isinstance(weights_csv, str):
        return None
    cleaned = weights_csv.strip()
    if not cleaned:
        return None
    parts = cleaned.split(',')
    values = []
    for r in parts:
        item = r.strip()
        if not item:
            return None
        try:
            val = int(item)
            if val < 0:
                return None
            values.append(val)
        except (ValueError, TypeError):
            return None
    if not values:
        return None
    return sum(values) // len(values)


def payable_charge(text):
    if not isinstance(text, str):
        return None
    if '|' not in text:
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    charge_str = parts[0].strip()
    discount_str = parts[1].strip()
    try:
        charge = float(charge_str)
        discount = float(discount_str)
    except (ValueError, TypeError):
        return None
    if charge < 0 or discount < 0:
        return None
    try:
        total = charge * 1.18 - discount
        return max(round(total, 2), 0.0)
    except OverflowError:
        return None


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    result = parse_order(user_input)
    print("Garment and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
