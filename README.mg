# IFTS 29 - Programación Sobre Redes  
## Práctica Formativa N° 3 - Sistema de Gestión de Tareas con API - Rediseño como sistema distribuido

###  Alumno: Andrea Purriños
###  Comisión: 3A1C26

---

## Descripción de la PFO 3 
Esta entrega transforma el sistema monolítico anterior en una arquitectura distribuida de alta disponibilidad. Se reemplazó el protocolo HTTP y el framework Flask por una comunicación basada en **Sockets TCP nativos**, delegando el procesamiento de datos a un **Pool de Hilos (Workers)** para simular un entorno escalable y asincrónico.

---

## Diagrama de la Arquitectura


```mermaid
flowchart TD
    subgraph Clientes [Capa de Clientes]
        A[Cliente Web]
        B[Cliente Móvil]
    end

    subgraph Entrada [Capa de Entrada y Red]
        C[Balanceador de Carga<br>Nginx / HAProxy]
    end

    subgraph Procesamiento [Capa de Servidores / Workers]
        W1[Servidor Worker 1<br>Pool de Hilos]
        W2[Servidor Worker 2<br>Pool de Hilos]
    end

    subgraph Mensajeria [Capa de Mensajería]
        RMQ[Cola de Mensajes<br>RabbitMQ]
    end

    subgraph Almacenamiento [Capa de Persistencia Distribuida]
        DB[(DB <br>PostgreSQL)]
        S3[Almacenamiento Objetos<br>Amazon S3]
    end

    %% Flujos simplificados para evitar superposición de texto
    A & B -->|Sockets TCP| C
    C --> W1 & W2
    
    %% Envío y consumo de la cola
    W1 & W2 ===>|1. Publica / 2. Consume| RMQ
    
    %% Guardado en persistencia
    W1 & W2 --->|3. Guarda Datos| DB
    W1 & W2 --->|3. Guarda Archivos| S3
```
---
## Nuevas Tecnologías e Implementación
Sockets (TCP/IP): Protocolo de comunicación directo y bidireccional en texto plano (JSON serializado).

Concurrent Futures (ThreadPoolExecutor): Manejo de un pool de hilos del lado del servidor para procesar las peticiones de los trabajadores (Workers) en paralelo sin bloquear el socket principal.


## Historial - Práctica Formativa N° 2 (Flask + SQLite)

## 🌐 CAPTURAS DE PANTALLA DE PRUEBAS EN THUNDER CLIENT
🔗 https://acpurrinos.github.io/pfo2-gestion-tareas/

---

## Descripción

Este proyecto consiste en el desarrollo de una API REST utilizando Flask que permite gestionar usuarios y tareas.  
El sistema incluye registro de usuarios, autenticación mediante inicio de sesión y gestión básica de tareas almacenadas en una base de datos SQLite.

Las contraseñas se almacenan de forma segura utilizando hashing, evitando su almacenamiento en texto plano.

El sistema se interactúa mediante un cliente en consola que consume los endpoints de la API.

---

##  Funcionalidades

- Registro de usuarios  
- Inicio de sesión con autenticación  
- Cierre de sesión  
- Protección de rutas mediante sesiones  
- Visualización de tareas mediante un endpoint HTML protegido  
- Creación de tareas  
- Eliminación de tareas  
- Persistencia de datos mediante SQLite  

---

##  Tecnologías utilizadas

- Python 3  
- Flask  
- Flask-SQLAlchemy  
- SQLite  
- Werkzeug (hash de contraseñas)  
- Requests (cliente en consola)  

---

##  Estructura del proyecto

```bash
gestion/
├── servidor.py
├── cliente.py
├── README.md
├── images/
│   ├── post_registro_registroExitoso.jpg
│   ├── post_login_loginExitoso.jpg
│   ├── get_usuarioAutorizado.jpg
├── app.db
├── .gitignore


## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/ACPurrinos/pfo2-gestion-tareas.git
cd gestion
````

### 2. Crear entorno virtual (opcional)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias

```bash
pip install flask flask_sqlalchemy werkzeug requests
```

---

## Ejecución

### 1. Ejecutar el servidor

```bash
python servidor.py
```

### 2. Ejecutar el cliente

```bash
python cliente.py
```

---

## Endpoints

### Registro de usuario

```http
POST /registro
```

```json
{
  "usuario": "nombre",
  "password": "1234"
}
```

### Inicio de sesión

```http
POST /login
```

```json
{
  "usuario": "nombre",
  "password": "1234"
}
```

### Cierre de sesión

```http
POST /logout
```

### Obtener tareas (HTML)

```http
GET /tareas
```

Devuelve un HTML con mensaje de bienvenida y listado de tareas.
Requiere sesión iniciada.

---

## Cliente en consola

El cliente permite:

1. Registrar usuario
2. Iniciar sesión
3. Ver tareas
4. Crear tareas
5. Eliminar tareas
6. Cerrar sesión
7. Salir

---

## Seguridad

* Las contraseñas se almacenan utilizando hashing con `werkzeug.security`
* Funciones utilizadas:

  * `generate_password_hash`
  * `check_password_hash`

---

## Notas

* La autenticación se maneja mediante sesiones de Flask
* La base de datos SQLite se genera automáticamente al ejecutar el servidor
* El endpoint `/tareas` devuelve HTML como requisito del trabajo práctico