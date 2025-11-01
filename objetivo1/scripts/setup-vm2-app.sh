#!/bin/bash
# Script para configurar VM2 - Aplicación

echo "======================================"
echo "Configurando VM2 - Aplicación"
echo "======================================"

# Actualizar sistema
echo "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar Docker
echo "Instalando Docker..."
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# Instalar NGINX
echo "Instalando NGINX..."
sudo apt install nginx -y

# Instalar Certbot
echo "Instalando Certbot..."
sudo apt install certbot python3-certbot-nginx -y

# Instalar Git
echo "Instalando Git..."
sudo apt install git -y

echo "======================================"
echo "Dependencias instaladas"
echo "======================================"
echo ""
echo "Pasos siguientes:"
echo "1. Cerrar sesión y volver a conectar (para aplicar grupo docker)"
echo "2. Clonar repositorio de BookStore"
echo "3. Configurar variables de entorno (.env)"
echo "4. Ejecutar docker-compose"
echo "5. Configurar NGINX"
echo "6. Obtener certificado SSL con Certbot"