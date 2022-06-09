import bcrypt
import getpass


while True:

    password = getpass.getpass(prompt='Por favor, introduce la contraseña que quieres que sea encriptada: ') 
    ckeck_password = getpass.getpass(prompt='Por favor, repite la contraseña: ') 

    if password == ckeck_password:
        
        password = password.encode('utf-8')

        # Generate salt
        salt = bcrypt.gensalt()

        # Hash password
        hash = bcrypt.hashpw(password, salt)

        # Save salt and hash
        f = open("encript_password.txt","w+")

        f.write("Salt: " + salt.decode("utf-8") + "\n")
        f.write("Hash: " + hash.decode("utf-8") + "\n") 

        print("La contraseña ha sido encriptada correctamente. Se ha generado el archivo encript_password.txt")

        f.close()
        break

    else:
        print("Las contraseñas no han coincidido. Por favor, inténtelo otra vez.")

# print(bcrypt.checkpw(b"k1rl4sf3l35", b'$2b$12$8grSVALUCAUkbq.7JR8Ahex58CUZsAlSEoIJYIv0Ojgbv.3wwDnLy'))