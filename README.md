# Overview

## What It Is

The **Real-Time Analytics Dashboard** is a web application designed to
collect, process, and visualize real-time user behavior data (e.g., page
views, sessions, conversions) from a website. It provides live metrics
such as active users, page views, conversions, and conversion rates,
updated every 5 seconds via WebSocket. The dashboard is built using a
Python stack with Django, Django Channels, Redis, and PostgreSQL,
ensuring scalability for large data volumes and fast updates.

## Purpose

-   **Track User Behavior**: Captures events like page views and
    conversions in real-time.

-   **Real-Time Visualization**: Displays live metrics through a
    WebSocket-connected dashboard.

-   **Scalability**: Handles high data volumes using PostgreSQL for
    storage and Redis for real-time messaging.

# How It Works

## Architecture

-   **Frontend**: A simple HTML dashboard (`dashboard.html`) connects to
    a WebSocket endpoint (`ws://localhost:8000/ws/analytics/`) to
    receive live metrics updates. It uses Tailwind CSS for styling and
    JavaScript for WebSocket communication.

-   **Backend**:

    -   **Django**: Handles HTTP requests for event tracking (e.g., POST
        requests to `/track/event/`).

    -   **Django Channels**: Manages WebSocket connections for real-time
        updates, using Redis as the channel layer.

    -   **PostgreSQL**: Stores event data (page views, conversions) in a
        relational database.

    -   **Redis**: Facilitates real-time messaging between the backend
        and WebSocket clients.

-   **Data Flow**:

    1.  Clients send events (e.g., page views) via POST requests to
        `/track/event/`.

    2.  Django processes and stores events in PostgreSQL.

    3.  Django Channels aggregates metrics every 5 seconds and
        broadcasts them to connected WebSocket clients.

    4.  The frontend (`dashboard.html`) displays updated metrics.

## Key Components

-   **Models** (`analytics/models.py`): Defines `PageView` and
    `Conversion` models for storing events.

-   **Views** (`analytics/views.py`): Handles event tracking via the
    `track_event` view.

-   **Consumers** (`analytics/consumers.py`): Manages WebSocket
    connections and sends periodic metric updates.

-   **Routing** (`analytics/routing.py`): Defines the WebSocket endpoint
    `/ws/analytics/`.

-   **ASGI** (`real_time_analystics_Dashboard/asgi.py`): Configures the
    ASGI application for HTTP and WebSocket handling.

-   **Dashboard** (`dashboard.html`): Displays metrics (active users,
    page views, conversions, conversion rate).

# Prerequisites and Installation

## Software Requirements

-   **Python**: Version 3.8--3.11 (your setup uses Python 3.13.1, which
    is compatible but newer than recommended).

-   **PostgreSQL**: Version 10 or higher (e.g., 16).

-   **Redis**: Windows-compatible version (e.g., 5.0.14.1 from
    MSOpenTech or tporadowski's fork).

-   **Node.js** (optional): For testing WebSocket connections with
    `wscat`.

## Installation Steps

1.  **Install Python**:

    -   Download and install Python 3.13.1 from
        <https://www.python.org/downloads/windows/>.

    -   Add `C:\Users\hp omen\AppData\Local\Programs\Python\Python313`
        and
        `C:\Users\hp omen\AppData\Local\Programs\Python\Python313\Scripts`
        to your PATH.

    -   Verify: `python –version`.

2.  **Install PostgreSQL**:

    -   Download from <https://www.postgresql.org/download/windows/>
        (EnterpriseDB installer).

    -   During installation:

        -   Set a password for the `postgres` user.

        -   Use default port `5432`.

    -   Add `C:\Program Files\PostgreSQL\16\bin` to PATH.

    -   Verify: `psql –version`.

3.  **Install Redis**:

    -   Download from <https://github.com/tporadowski/redis/releases>
        (e.g., Redis-x64-5.0.14.1).

    -   Extract to `C:\Program Files\Redis`.

    -   Add `C:\Program Files\Redis` to PATH.

    -   Verify: `redis-server –version`.

4.  **Set Up Virtual Environment**:

    ``` {.bash language="bash"}
    cd D:\intern\real_time_analystics_Dashboard
    python -m venv venv
    .\venv\Scripts\activate
    ```

5.  **Install Python Dependencies**:

    -   Create `requirements.txt`:

        ``` {.text language="text"}
        Django==4.2.16
        channels==4.1.0
        redis==5.0.1
        psycopg2-binary==2.9.9
        asgiref==3.7.2
        channels-redis==4.1.0
        daphne==4.1.0
        ```

    -   Install:

        ``` {.bash language="bash"}
        pip install -r requirements.txt
        ```

# Configuration

## Project Structure

Ensure the following structure:

``` {.text language="text"}
D:\intern\real_time_analystics_Dashboard\
├── analytics\
│   ├── __init__.py
│   ├── consumers.py
│   ├── models.py
│   ├── routing.py
│   ├── urls.py
│   ├── views.py
│   ├── templates\analytics\dashboard.html
├── real_time_analystics_Dashboard\
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
├── requirements.txt
```

## Configure PostgreSQL

1.  **Create Database**:

    ``` {.bash language="bash"}
    psql -U postgres
    ```

    In the `psql` prompt:

    ``` {.sql language="sql"}
    CREATE DATABASE analytics_db;
    \q
    ```

2.  **Update `settings.py`**:

    ``` {.python language="python"}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'analytics_db',
            'USER': 'postgres',
            'PASSWORD': 'your-postgres-password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

## Configure Redis

-   Ensure Redis uses port 6379 (or update `settings.py` if using a
    different port).

-   Update `settings.py`:

    ``` {.python language="python"}
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [('127.0.0.1', 6379)],
            },
        },
    }
    ```

## Configure Django Settings

Update `real_time_analystics_Dashboard/settings.py`:

``` {.python language="python"}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'analytics',
]

ASGI_APPLICATION = 'real_time_analystics_Dashboard.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## Update `asgi.py`

Ensure `real_time_analystics_Dashboard/asgi.py` avoids early model
imports:

``` {.python language="python"}
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_time_analystics_Dashboard.settings')

django_asgi_app = get_asgi_application()
import analytics.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(analytics.routing.websocket_urlpatterns)
    ),
})
```

## Configure URLs

-   `real_time_analystics_Dashboard/urls.py`:

    ``` {.python language="python"}
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('track/', include('analytics.urls')),
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ```

-   `analytics/urls.py`:

    ``` {.python language="python"}
    from django.urls import path
    from . import views

    urlpatterns = [
        path('event/', views.track_event, name='track_event'),
        path('dashboard/', views.dashboard, name='dashboard'),
    ]
    ```

## Configure Views

Update `analytics/views.py`:

``` {.python language="python"}
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import PageView, Conversion
import json

@csrf_exempt
def track_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event_type = data.get('event_type')
        session_id = data.get('session_id')
        
        if event_type == 'page_view':
            PageView.objects.create(
                session_id=session_id,
                page_url=data.get('page_url', ''),
                user_agent=data.get('user_agent', ''),
                ip_address=request.META.get('REMOTE_ADDR')
            )
        elif event_type == 'conversion':
            Conversion.objects.create(
                session_id=session_id,
                conversion_type=data.get('conversion_type', ''),
                value=data.get('value', None)
            )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def dashboard(request):
    return render(request, 'analytics/dashboard.html')
```

## Configure Dashboard Template

Place `dashboard.html` in `analytics/templates/analytics/`:

``` {.html language="html"}
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Analytics Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Real-Time Analytics Dashboard</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded shadow">
                <h2 class="text-lg font-semibold">Active Users</h2>
                <p id="active_users" class="text-2xl">0</p>
            </div>
            <div class="bg-white p-4 rounded shadow">
                <h2 class="text-lg font-semibold">Page Views</h2>
                <p id="page_views" class="text-2xl">0</p>
            </div>
            <div class="bg-white p-4 rounded shadow">
                <h2 class="text-lg font-semibold">Conversions</h2>
                <p id="conversions" class="text-2xl">0</p>
            </div>
            <div class="bg-white p-4 rounded shadow">
                <h2 class="text-lg font-semibold">Conversion Rate</h2>
                <p id="conversion_rate" class="text-2xl">0%</p>
            </div>
        </div>
    </div>
    <script>
        const socket = new WebSocket('ws://localhost:8000/ws/analytics/');
        
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            document.getElementById('active_users').textContent = data.active_users;
            document.getElementById('page_views').textContent = data.page_views;
            document.getElementById('conversions').textContent = data.conversions;
            document.getElementById('conversion_rate').textContent = data.conversion_rate + '%';
        };

        socket.onclose = function(event) {
            console.error('WebSocket closed unexpectedly');
        };
    </script>
</body>
</html>
```

# Starting the Application

1.  **Activate Virtual Environment**:

    ``` {.bash language="bash"}
    cd D:\intern\real_time_analystics_Dashboard
    .\venv\Scripts\activate
    ```

2.  **Start Redis**:

    ``` {.bash language="bash"}
    redis-server
    ```

    Verify:

    ``` {.bash language="bash"}
    redis-cli ping
    ```

    Should return `PONG`.

3.  **Start PostgreSQL**: Ensure the PostgreSQL service is running:

    ``` {.bash language="bash"}
    net start postgresql-x64-16
    ```

4.  **Apply Migrations**:

    ``` {.bash language="bash"}
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Start the Django Server**:

    ``` {.bash language="bash"}
    $env:DJANGO_SETTINGS_MODULE = "real_time_analystics_Dashboard.settings"
    daphne -b 0.0.0.0 -p 8000 real_time_analystics_Dashboard.asgi:application
    ```

6.  **Access the Dashboard**:

    -   Open <http://127.0.0.1:8000/track/dashboard/> in a browser.

    -   Verify WebSocket connection in the Network tab (F12).

7.  **Test Event Tracking**: Send a POST request to
    `http://localhost:8000/track/event/`:

    ``` {.bash language="bash"}
    curl -X POST http://localhost:8000/track/event/ -H "Content-Type: application/json" -d '{"event_type":"page_view","session_id":"test123","page_url":"https://example.com","user_agent":"test"}'
    ```

    Check the dashboard for updated metrics.

# Troubleshooting

-   **Redis Issues**:

    -   If port 6379 is occupied:

        ``` {.bash language="bash"}
        netstat -aon | findstr :6379
        taskkill /PID <PID> /F
        ```

    -   Use a different port if needed (update `settings.py`).

-   **PostgreSQL Issues**:

    -   Verify connection: `psql -U postgres -d analytics_db`.

    -   Check credentials in `settings.py`.

-   **TemplateDoesNotExist**:

    -   Ensure `dashboard.html` is in `analytics/templates/analytics/`.

    -   Verify `’APP_DIRS’: True` in `TEMPLATES`.

-   **WebSocket 404**:

    -   Check `analytics/routing.py` and `asgi.py`.

    -   Ensure `daphne` is used, not `runserver`.

# Enhancements

-   **Add Authentication**: Secure the dashboard with Django's
    authentication.

-   **Visualizations**: Use Chart.js for graphical metrics.

-   **Scalability**: Add indexing to `PageView` and `Conversion` models,
    use a load balancer for high traffic.

-   **Production**: Use a WSGI/ASGI server like Gunicorn with Daphne,
    configure `DEBUG=False`, and set up Redis as a service.

# Conclusion

The Real-Time Analytics Dashboard provides a robust solution for
tracking and visualizing website user behavior in real-time. By
following the installation, configuration, and startup steps, you can
deploy a scalable analytics system. Address any errors using the
troubleshooting guide, and consider enhancements for production use.
