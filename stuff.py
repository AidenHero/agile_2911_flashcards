from werkzeug.security import generate_password_hash, check_password_hash


hashed_password = generate_password_hash("aiden123")

print(hashed_password)

if check_password_hash("scrypt:32768:8:1$kbFucH2SKnaRF3K9$167b9855d7ef998754a84b27dbdc3aac3155df3958a72e6c5db7b26dd4ffc610a4f3b72a54dd0dcc9ab6570c07405bff6b6a98fdf52e97f7d4648993a77f4a37","aiden123"):
    print("it works")
else:
    print("it failed")