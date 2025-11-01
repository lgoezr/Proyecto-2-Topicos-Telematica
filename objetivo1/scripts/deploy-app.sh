#!/bin/bash
# Script para desplegar la aplicación BookStore
# Ejecutar en VM2 después de configuración inicial

echo "======================================"
echo "Desplegando BookStore"
echo "======================================"

# Clonar repositorio
cd /home/ubuntu
git clone https://github.com/st0263eafit/st0263-252.git
cd st0263-252/proyecto2
unzip BookStore.zip
cd BookStore-monolith

# Crear archivo .env (debe ser editado manualmente)
cat > .env <<EOF
SECRET_KEY=CAMBIAR_ESTO
DB_HOST=CAMBIAR_POR_IP_PRIVADA_DB
DB_USER=bookstore_user
DB_PASS=bookstore_pass
DB_NAME=bookstore
FLASK_ENV=production
EOF

echo "======================================"
echo "⚠️  IMPORTANTE: Edita el archivo .env con los valores correctos"
echo "======================================"
echo "nano .env"
echo ""
echo "Después ejecuta:"
echo "docker-compose -f docker-compose.prod.yml build"
echo "docker-compose -f docker-compose.prod.yml up -d"