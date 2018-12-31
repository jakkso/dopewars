"""
Contain utility functions used by multiple classes
"""


def fmt_money(amount: int) -> str:
    """
    Formats amount into a more human readable amount.
    To Americans, anyways
    :param amount:
    :return:
    """
    string = str(amount)
    if len(string) < 4:
        return f"${string}"
    chunks = []
    indices = range(3, 100, 3)  # Every 4th character should be a comma
    for index, char in enumerate(reversed(string)):
        if index in indices:
            chunks.append(",")
            chunks.append(char)
        else:
            chunks.append(char)
    return "$" + "".join(chunks[::-1])
