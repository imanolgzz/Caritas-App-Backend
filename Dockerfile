# Utiliza una imagen base (en este caso Ubuntu)
FROM ubuntu:22.04

# Actualiza el sistema e instala OpenSSH server y sudo
RUN apt-get update && \
    apt-get install -y openssh-server sudo python3-pip && \
    apt-get clean

# Crea el directorio necesario para el demonio SSH
RUN mkdir /var/run/sshd

# Crear un nuevo usuario no-root
RUN useradd -m -s /bin/bash user01

# Configura la contraseña para el nuevo usuario
RUN echo 'user01:123' | chpasswd
RUN echo 'root:123' | chpasswd

# Agrega el usuario imaxinio al grupo sudo para que tenga privilegios de administrador
RUN usermod -aG sudo user01 

# Permite la autenticación por contraseña
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config  # Cambiar a no para evitar el acceso root

# Asegúrate de que el usuario no-root pueda usar SSH
RUN mkdir /home/user01/.ssh && chmod 700 /home/user01/.ssh

# Exponer el puerto SSH
EXPOSE 22

RUN mkdir /home/user01/reto
WORKDIR /home/user01/reto

COPY ./src ./src
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Iniciar el servidor SSH
CMD ["/usr/sbin/sshd", "-D"]
