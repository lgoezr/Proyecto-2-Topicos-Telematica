# ST0263 Tópicos Especiales en Telemática
- **Estudiante(s)**: Samuel Valencia Loaiza, svalenci41@eafit.edu.co; Lorena Goez Ruiz, lgoezr1@eafit.edu.co
- **Profesor:** Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co

# Videos de sustentación
- **Objetivo 1 y 2**
[Ver video](https://youtu.be/tY857t0eJJc)
- **Objetivo 3 y 4**
[Ver video](https://www.youtube.com/watch?v=Ze5RKBz3oGE)

# Proyecto 2 - Aplicación Escalable BookStore
## 1. Descripción de la Actividad
Implementación de una aplicación BookStore escalable en AWS, evolucionando desde un despliegue monolítico hasta una arquitectura de microservicios en Kubernetes, aplicando diferentes patrones de escalamiento y mejores prácticas en la nube.

### 1.1. Aspectos CUMPLIDOS de la actividad propuesta
#### Objetivo 1 - Despliegue Monolítico:**
-   Aplicación Flask + MySQL en 2 VMs separadas
-   NGINX como proxy reverso configurado
-   Dominio DuckDNS funcionando
-   Security Groups AWS configurados correctamente
-   Todas las funcionalidades de BookStore operativas
-   Comunicación entre VMs vía red privada AWS

#### Objetivo 2 - Escalamiento en AWS:
- Amazon RDS MySQL implementado y funcional
- Amazon EFS configurado y montado en instancias
- AMI personalizada creada con aplicación pre-instalada
- Launch Template y Auto Scaling Group operativos
- Application Load Balancer configurado
- Target Group con health checks
- Políticas de auto-scaling basadas en CPU
- Comunicación aplicación-RDS-EFS 

#### Objetivo 3 - Kubernetes EKS:
- Despliegue funcional de app BookStore monolítica en clúster EKS
- Almacenamiento persistente para MySQL
- Exposición del servicio mediante NodePort
- Imagen Docker publicada en Amazon ECR
- Recursos Kubernetes: Namespace, PersistentVolume, Deployments, Services
- Comunicación interna por red de Kubernetes

#### Objetivo 4 - Opción 2: Microservicios:
- Despliegue exitoso de Sock Shop (e-commerce microservicios)
- 13 microservicios desplegados en EKS
- Comunicación REST y mensajería asíncrona (RabbitMQ)
- Bases de datos distribuidas (MySQL, MongoDB, Redis)
- Patrón CQRS/CDRS con consistencia eventual
- Exposición mediante NodePort accesible vía navegador
- Orquestación completa mediante Kubernetes

### 1.2. Aspectos NO cumplidos de la actividad propuesta
#### Objetivo 1:
- Certificado SSL/TLS no implementado
#### Razón: Limitaciones técnicas con DuckDNS para validación DNS de Let's Encrypt

#### Objetivo 2:
- Application Load Balancer no enruta tráfico correctamente
#### Razón: Problema de configuración en Security Groups o health checks

#### Objetivo 4:
- Integración con servicios administrados EFS o RDS
#### Razón: Fallas en AWS que impidieron la creación de estos servicios

## 2. Diseño de Alto Nivel y Arquitectura
### Objetivo 1 - Arquitectura Monolítica:
```Internet → IP Elástica → VM2 (NGINX + Flask) → VM1 (MySQL)```
#### Patrones aplicados:

- Separación de capas (presentación, aplicación, datos)

- Proxy reverso para manejo de tráfico

- Comunicación interna por red privada

###  Objetivo 2 - Arquitectura Escalable:
```Internet → ALB → Auto Scaling Group (2-4 instancias) → RDS + EFS```
#### Patrones aplicados:

- Auto-scaling horizontal basado en métricas

- Base de datos administrada (RDS)

- Almacenamiento compartido (EFS)

- Load balancing a nivel de aplicación

- Instancias stateless

### Objetivo 3 - Kubernetes Monolítico:
```Internet → NodePort → Flask Pod → MySQL Pod (Persistent Volume)```
#### Arquitectura:

- Frontend y backend Flask monolítico
- Base de datos MySQL en contenedor separado
- Comunicación interna por red de Kubernetes
- Exposición externa mediante NodePort Service
- Despliegue sobre Amazon EKS

#### Buenas prácticas aplicadas:

- Separación de servicios en Pods distintos
- Uso de namespace para aislar recursos
- Volúmenes persistentes para MySQL
- Versionamiento y despliegue reproducible

### Objetivo 4 - Arquitectura Microservicios:
```Internet → NodePort → Frontend → [13 Microservicios] → [Bases de Datos] ```
#### Componentes:

- Front-end (interfaz web)
- User, Orders, Catalogue, Carts, Payment, Shipping services
- RabbitMQ, Redis, MongoDB, MySQL
- Comunicación REST + mensajería asíncrona

#### Patrones aplicados:

- Database per Service
- CQRS/CDRS para consistencia eventual
- Comunicación asíncrona con RabbitMQ
- Desacoplamiento completo entre componentes

#### Buenas prácticas aplicadas:

- Aislamiento lógico por namespace
- Escalabilidad independiente por microservicio
- Persistencia nativa en contenedores
- Monitoreo distribuido

## 3. Ambiente de Desarrollo y Técnico
### 3.1. Tecnologías y Versiones:
#### Objetivo 1 & 2:
- Python: 3.9+
- Flask: 2.3.3
- MySQL: 8.0.35
- Docker: 24.0+
- Docker Compose: 2.20+
- NGINX: 1.18+

#### Objetivo 3:
- Python: 3.10
- Flask: 2.3.3
- MySQL: 8.0
- Kubernetes: 1.28+
- AWS EKS: Managed
- AWS ECR: Container Registry

#### Objetivo 4:
- Lenguajes: Go, Java, Node.js (según microservicio)
- Bases de datos: MySQL 8, MongoDB, Redis
- Mensajería: RabbitMQ
- Kubernetes: 1.28+
- AWS EKS: Managed

### 3.2. Compilación y Ejecución:
#### Objetivo 3 - BookStore en EKS:
```
# Clonar el repositorio
git clone https://github.com/Yatogami201/Tele-lab2.git
cd Tele-lab2/BookStore-monolith

# Ejecutar localmente con docker-compose
docker-compose up

# Construir imagen Docker
docker build -t bookstore:v1 .

# Crear clúster EKS
eksctl create cluster \
  --name bookstore \
  --region us-east-1 \
  --nodegroup-name bookstore-nodes \
  --nodes 2 \
  --node-type t3.micro \
  --with-oidc \
  --managed

# Configurar ECR y subir imagen
aws ecr create-repository --repository-name bookstore --region us-east-1
docker tag bookstore:v1 <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/bookstore:v1
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/bookstore:v1

# Desplegar en Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/persistent-volume.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/flask-deployment.yaml

# Verificar despliegue
kubectl get pods -n bookstore
kubectl get svc -n bookstore

# Acceder a la aplicación
# http://<EXTERNAL-IP>:<NODEPORT>
```
#### Objetivo 4-Sock Shop Microservicios:
```
# Crear namespace
kubectl create namespace sock-shop

# Desplegar aplicación completa
kubectl apply -f https://raw.githubusercontent.com/microservices-demo/microservices-demo/master/deploy/kubernetes/complete-demo.yaml -n sock-shop

# Verificar despliegue
kubectl get pods -n sock-shop
kubectl get svc -n sock-shop

# Acceder a la aplicación
# http://<EXTERNAL-IP>:30001
```
### 3.3. Configuración de Parámetros:
#### Objetivo 1 & 2:
#### Archivo .env:
```
SECRET_KEY=production-secret-key
DB_HOST=172.31.X.X
DB_USER=bookstore_user
DB_PASS=password123
DB_NAME=bookstore
DB_PORT=3306
FLASK_ENV=production
```
#### Objetivo 3:
#### Variables de entorno Kubernetes:
```
env:
  - name: MYSQL_USER
    value: "bookstore_user"
  - name: MYSQL_PASSWORD
    value: "bookstore_pass"
  - name: MYSQL_ROOT_PASSWORD
    value: "root_pass"
```
### 3.4. Estructura de Directorios:
```
proyecto2/
├── objetivo1/
│   ├── aplicacion/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── requirements.txt
│   │   └── app/
│   ├── nginx/
│   └── scripts/
├── objetivo2/
│   ├── terraform/
│   ├── cloudformation/
│   └── scripts/
├── objetivo3/
│   ├── k8s/
│   │   ├── namespace.yaml
│   │   ├── persistent-volume.yaml
│   │   ├── mysql-deployment.yaml
│   │   └── flask-deployment.yaml
│   └── Dockerfile
└── objetivo4/
    └── sock-shop/
        └── complete-demo.yaml
```
## 4. Ambiente de Ejecución (Producción)
### 4.1. Especificaciones Técnicas - Producción:
#### Objetivo 1 (2 VMs):
- VM App: t2.small, Ubuntu 22.04, Docker 24.0+
- VM DB: t2.micro, Ubuntu 22.04, MySQL 8.0.35
- Dominio: proyecto2-[nombre].duckdns.org
- Protocolo: HTTP (puerto 80)

#### Objetivo 2 (Arquitectura Escalable):
- Instancias: t3.micro (2-4 instancias)
- RDS: db.t3.micro, MySQL 8.0.35
- EFS: General Purpose, 3 mount targets
- ALB: Application Load Balancer internet-facing
- Auto Scaling: 2-4 instancias, CPU-based

#### Objetivo 3 (Kubernetes):
- EKS Cluster: 2 nodos t3.micro
- Namespace: bookstore
- Storage: Persistent Volumes para MySQL
- Exposición: NodePort Service
- Registry: Amazon ECR

#### Objetivo 4 (Microservicios):
- EKS Cluster: 2+ nodos t3.small
- Namespace: sock-shop
- Microservicios: 13 servicios independientes
- Bases de datos: MySQL, MongoDB, Redis contenedorizados
- Messaging: RabbitMQ para comunicación asíncrona
- Exposición: NodePort (puerto 30001)

### 4.2. Configuración en Producción:
#### Objetivo 3 - Kubernetes:
```
# Service exposición
apiVersion: v1
kind: Service
metadata:
  name: flask-service
  namespace: bookstore
spec:
  type: NodePort
  ports:
    - port: 5000
      nodePort: 30694
  selector:
    app: flask
```
#### Objetivo 4 - Sock Shop:
```
# Frontend service
apiVersion: v1
kind: Service
metadata:
  name: front-end
  namespace: sock-shop
spec:
  type: NodePort
  ports:
  - port: 80
    nodePort: 30001
  selector:
    name: front-end
```
### 4.3. Despliegue en Producción:
#### Objetivo 3:
```
# Configurar kubectl para EKS
aws eks update-kubeconfig --region us-east-1 --name bookstore

# Aplicar todos los manifiestos
kubectl apply -f k8s/

# Monitorear despliegue
kubectl get all -n bookstore
```
#### Objetivo 4:
```
# Despliegue con un solo comando
kubectl apply -f complete-demo.yaml -n sock-shop

# Verificar estado
kubectl get pods -n sock-shop --watch
```
### 4.4. Guía de Usuario:
#### BookStore (Objetivos 1, 2, 3):
- Acceso: Navegar a la URL proporcionada (IP:Puerto)
- Registro: Crear nueva cuenta de usuario
- Catálogo: Explorar libros disponibles
- Compra: Seleccionar libros y proceder al checkout
- Gestión: Para usuarios vendedores, agregar nuevos libros

#### Sock Shop (Objetivo 4):
- Acceso: http://<IP-EXTERNA>:30001
- Navegación: Explorar catálogo de productos
- Carrito: Agregar productos al carrito de compras
- Checkout: Completar proceso de compra
- Usuarios: Registrarse y gestionar perfil

## 5. Información Relevante Adicional
### 5.1. Decisiones de Diseño Clave:
- Separación de responsabilidades: Cada objetivo aborda un patrón arquitectónico diferente
- Evolución progresiva: Desde monolito hasta microservicios
- Tolerancia a fallos: Estrategias de respaldo para componentes críticos
- Monitorización: Health checks y métricas de performance implementadas

### 5.2. Métricas de Performance:
- BookStore: Tiempo de respuesta < 200ms, CPU 20-40% bajo carga normal
- Sock Shop: Comunicación asíncrona, consistencia eventual, alta disponibilidad
- Kubernetes: Auto-recovery de pods, escalamiento horizontal disponible

### 5.3. Lecciones Aprendidas:
- Configuración AWS: Los Security Groups son críticos para la conectividad
- Kubernetes: Los namespaces ayudan en el aislamiento y organización
- Microservicios: La comunicación asíncrona es esencial para la resiliencia
- Persistencia: Los volúmenes persistentes son necesarios para stateful applications
- CI/CD: La automatización del despliegue acelera el desarrollo

### 5.4. Retos Superados:
- Configuración de redes en diferentes ambientes AWS
- Comunicación entre servicios en arquitecturas distribuidas
- Persistencia de datos en contenedores efímeros
- Balanceo de carga y auto-scaling en diferentes capas

## Referencias

### Código Base y Aplicaciones:
- BookStore Monolítica: https://github.com/st0263eafit/st0263-252/blob/main/proyecto2/BookStore.zip
- Sock Shop Microservices: https://github.com/microservices-demo/microservices-demo

### Documentación Oficial:
- AWS EKS: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html
- Kubernetes: https://kubernetes.io/docs/home/
- Docker Documentation: https://docs.docker.com/
- Flask Framework: https://flask.palletsprojects.com/

### Herramientas y Utilidades:
- eksctl: https://eksctl.io/
- kubectl: https://kubernetes.io/docs/reference/kubectl/
- Docker Compose: https://docs.docker.com/compose/
