## IFTS 29 - Programación Sobre Redes  
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

    subgraph Clientes["Capa de Clientes"]
        A["Cliente Web"]
        B["Cliente Móvil"]
    end

    subgraph Entrada["Capa de Entrada y Red"]
        C["Balanceador de Carga<br/>Nginx / HAProxy"]
    end

    subgraph Procesamiento["Capa de Servidores / Workers"]
        W1["Servidor Worker 1<br/>Pool de Hilos"]
        W2["Servidor Worker 2<br/>Pool de Hilos"]
    end

    subgraph Mensajeria["Capa de Mensajería"]
        RMQ["Cola de Mensajes<br/>RabbitMQ"]
    end

    subgraph Almacenamiento["Capa de Persistencia Distribuida"]
        DB["PostgreSQL"]
        S3["Amazon S3"]
    end

    A -->|Sockets TCP| C
    B -->|Sockets TCP| C

    C --> W1
    C --> W2

    W1 <-->|Publica / Consume| RMQ
    W2 <-->|Publica / Consume| RMQ

    W1 -->|Guarda Datos| DB
    W2 -->|Guarda Datos| DB

    W1 -->|Guarda Archivos| S3
    W2 -->|Guarda Archivos| S3
```