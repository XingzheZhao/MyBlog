import timeit


setup_1 = """
import hashlib
import secrets
pw = secrets.token_urlsafe(20)
"""
statement_1 = """
hashlib.sha256(str.encode(pw))
"""

# t1 = timeit.timeit(stmt=statement_1, setup=setup_1, number=1000000)
# t1 = timeit.repeat(stmt=statement, setup=setup_1, number=1000000, repeat=5)
# print(f'Time to complete 1 million SHA256 (Byte data) = {t1} seconds')


setup_2 = """
import hashlib
import secrets
pw = 'password'
pw_salt = secrets.token_urlsafe(10)
pepper = 'c'
"""
statement_2 = """
hashlib.pbkdf2_hmac('sha256', str.encode(pw), str.encode(pw_salt+pepper), 100000).hex()
"""
t2 = timeit.timeit(stmt=statement_2, setup=setup_2, number=52)
t3 = timeit.timeit(stmt=statement_2, setup=setup_2, number=26)

print(f'Time of the worst case {t2}')
print(f'Time of the average case {t3}')