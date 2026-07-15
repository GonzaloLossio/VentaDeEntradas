# API de Venta de Entradas para Eventos Masivos

Este proyecto consiste en el desarrollo del backend para un sistema de venta de boletos en línea destinado a conciertos y eventos de alta demanda. Está construido utilizando FastAPI y PostgreSQL.

El objetivo principal de este desarrollo no era limitarse a la creación de un CRUD para gestionar eventos, sino resolver el desafío arquitectónico que supone la alta concurrencia. El sistema está diseñado para evitar la sobreventa de inventario bajo picos extremos de tráfico y gestionar el flujo transaccional de pagos de manera segura y eficiente.

## Stack Tecnológico

* **Framework:** FastAPI
* **Base de Datos:** PostgreSQL
* **ORM y Validación:** SQLModel (Integración de SQLAlchemy y Pydantic)
* **Pasarela de Pagos:** Stripe SDK
* **Seguridad:** OAuth2 con JSON Web Tokens (JWT) y encriptación Bcrypt
* **Migraciones:** Alembic
* **Servidor ASGI:** Uvicorn
* **Contenedorización:** Docker y Docker Compose
* **Testing:** Pytest y HTTPX
  
## Funcionalidades Principales

* **Autenticación y control de acceso:** Sistema de inicio de sesión basado en tokens JWT. Implementa roles diferenciados (cliente y administrador) para proteger y restringir el acceso a la gestión operativa del sistema.
* **Gestión de eventos e inventario:** Módulo para que los administradores puedan crear eventos y configurar distintas zonas (VIP, Preferencial, General), definiendo capacidades máximas y precios por boleto.
* **Flujo de reservas y pagos (Núcleo del sistema):** Al iniciar una compra, el backend valida la disponibilidad y genera una orden en estado pendiente integrándose con la API de Stripe para inicializar la intención de pago.
* **Control de concurrencia masiva:** Para evitar condiciones de carrera (Race Conditions) y sobreventa, se implementaron bloqueos transaccionales a nivel de fila (`WITH FOR UPDATE` en PostgreSQL). Las llamadas de red hacia Stripe se ejecutan en hilos secundarios (`asyncio.to_thread`) para no bloquear el flujo asíncrono del servidor mientras la base de datos se libera en milisegundos.
* **Webhooks, resiliencia e idempotencia:** El sistema expone un webhook público para escuchar las confirmaciones de Stripe. Cuenta con validaciones estrictas para ignorar eventos duplicados de la red y no corromper la base de datos. Además, integra un sistema de rollback que devuelve los boletos al inventario global si el pago falla.
* **Suite de pruebas automatizadas:** El proyecto cuenta con 33 tests implementados con Pytest y httpx, cubriendo los flujos principales de autenticación, gestión de eventos, zonas y órdenes de compra.

## Ejecución Local

Para levantar este proyecto en un entorno de desarrollo, siga los siguientes pasos:

1. Clonar el repositorio localmente.
2. Crear un entorno virtual de Python: `python -m venv venv`.
3. Activar el entorno virtual correspondiente a su sistema operativo.
4. Instalar las dependencias requeridas ejecutando: `pip install -r requirements.txt`.
5. Crear un archivo `.env` en la raíz del proyecto para definir las variables de entorno (URL de conexión a la base de datos, clave secreta de JWT y las credenciales de la API y Webhook de Stripe).
6. Ejecutar las migraciones para estructurar la base de datos: `alembic upgrade head`.
7. Iniciar el servidor de desarrollo: `uvicorn app.main:app --reload`.

Para ejecutar la suite de pruebas:
`pytest tests/ -v`.

## Ejecución con Docker

La forma más sencilla de levantar el proyecto es usando Docker Compose:

1. Clonar el repositorio
2. Crear un archivo `.env` en la raíz del proyecto con las variables de entorno necesarias
3. Ejecutar: `docker-compose up --build`
4. La documentación estará disponible en `http://localhost:8000/docs`

## Deuda Técnica y Áreas de Mejora

A pesar de que el núcleo transaccional es robusto y funcional, existen oportunidades de mejora para acercar la arquitectura a un estándar corporativo:

* **Tipado estricto en estados transaccionales:** Actualmente, los estados de las órdenes de compra (como "Pending" o "Completed") se manejan como cadenas de texto plano. El sistema debe refactorizarse para utilizar Enumeraciones (`Enum` de Python) para evitar errores de tipeo y mejorar la consistencia a nivel de base de datos.
* **Liberación de carritos abandonados:** Si un usuario inicia el proceso de compra, el sistema retiene los boletos. Sin embargo, si el cliente abandona la página sin pagar, esos boletos quedan bloqueados indefinidamente. Es necesario implementar un trabajador en segundo plano (utilizando Celery o BackgroundTasks) que cancele automáticamente las órdenes pendientes tras 10 minutos y libere el inventario.
* **Cobertura de tests al 100%:** Actualmente el proyecto cuenta con 33 tests cubriendo los flujos principales. Como área de mejora, se pueden agregar tests específicos para la lógica de concurrencia y las respuestas del webhook de Stripe bajo condiciones de carga simulada.
