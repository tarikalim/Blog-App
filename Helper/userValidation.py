import re
import dns.resolver


def validate_password(password):
    if len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[0-9]", password):
        return True
    return False


def validate_username(username):
    if len(username) >= 4:
        return True
    return False


def validate_mx_record(email):
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if mx_records:
            return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

    return False


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(email_regex, email):
        return False

    if not validate_mx_record(email):
        return False

    return True
