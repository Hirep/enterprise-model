
# Not used since I managed validation with 'pattern' attrib in HTML


def phone_number(str):
    return (str[1:].isnumeric() and str[0] == '+')


def email(emailaddress):
    import re
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", emailaddress) is not None:
        return True
    else:
        return False
