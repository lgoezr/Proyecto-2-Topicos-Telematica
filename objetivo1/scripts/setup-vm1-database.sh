#!/bin/bash
# Script para configurar VM1 - Base de Datos MySQL

echo "======================================"
echo "Configurando VM1 - Base de Datos MySQL"
echo "======================================"

# Actualizar sistema
echo "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar MySQL
echo "Instalando MySQL..."
sudo apt install mysql-server -y

# Verificar instalación
sudo systemctl status mysql

# Configurar MySQL para conexiones remotas
echo "Configurando MySQL para conexiones remotas..."
sudo sed -i 's/bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Reiniciar MySQL
sudo systemctl restart mysql

# Crear base de datos y usuario
echo "Creando base de datos y usuario..."
sudo mysql <<EOF
CREATE DATABASE bookstore;
CREATE USER 'bookstore_user'@'%' IDENTIFIED BY 'bookstore_pass';
GRANT ALL PRIVILEGES ON bookstore.* TO 'bookstore_user'@'%';
FLUSH PRIVILEGES;
EXIT;
EOF

echo "======================================"
echo "VM1 configurada exitosamente"
echo "======================================"