from database.models.enums import BaseAliasEnum


__all__ = ["SkillEnum"]


class SkillEnum(BaseAliasEnum):
    __validate_ordering__ = True

    UNKNOWN = "Неизвестно"

    ACTIVE_DIRECTORY = "Active Directory"
    AGILE = "Agile"
    AIOGRAM = "aiogram"
    AIOHTTP = "aiohttp"
    AIRFLOW = "Airflow", ("apache airflow",)
    ALEMBIC = "Alembic"
    ALLURE = "Allure"
    ANDROID = "Android"
    ANGULAR = "Angular"
    ANSIBLE = "Ansible"
    ARGOCD = "ArgoCD"
    ASP_NET = "ASP.NET"
    ASYNCIO = "asyncio"
    AXIOS = "Axios"
    AZURE = "Azure", ("azure devops",)
    BAN = "Ban", ("banjs", "ban.js")
    BASH = "Bash"
    BIG_DATA = "Big Data", ("работа с большим объемом информации",)
    BITRIX = "Bitrix", ("битрикс", "битрикс 24", "битрикс24")
    BPMN = "BPMN"
    C_SHARP = "C#"
    CASSANDRA = "Cassandra"
    CELERY = "Celery"
    CI_CD = "CI/CD", ("gitlab ci", "gitlab ci/cd", "github actions")
    CLICKHOUSE = "ClickHouse"
    CMS = "CMS"
    CONFLUENCE = "Confluence", ("atlassian confluence",)
    CPP = "C++"
    CRM = "CRM"
    CSS = "CSS", ("css3",)
    CYPRESS = "Cypress"
    DART = "DART"
    DAX = "DAX"
    DEVOPS = "DevOps"
    DHCP = "DHCP"
    DJANGO = "Django", ("drf", "django orm", "django rest framework")
    DNS = "DNS"
    DOCKER = "Docker"
    DOCKER_COMPOSE = "Docker Compose", ("docker-compose",)
    DOT_NET = ".NET"
    ELASTICSEARCH = "Elasticsearch", ("elk", "elk stack")
    ENGLISH = "Английский язык"
    ETL = "ETL"
    EXCEL = "Excel"
    FAST_API = "FastAPI"
    FIDDLER = "Fiddler"
    FIGMA = "Figma"
    FLASK = "Flask"
    FLUTTER = "Flutter"
    GIT = "Git"
    GITHUB = "GitHub"
    GITLAB = "GitLab"
    GO = "Go", ("golang",)
    GRAFANA = "Grafana"
    GRAPHQL = "GraphQL"
    GRPC = "gRPC"
    GULP = "Gulp"
    GUNICORN = "Gunicorn"
    HADOOP = "Hadoop"
    HELM = "Helm"
    HTML = "HTML", ("html5",)
    HTTP = "HTTP", ("https", "http/https")
    HYPER_V = "Hyper-V"
    IOS = "iOS"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"
    JENKINS = "Jenkins"
    JEST = "Jest"
    JIRA = "Jira", ("atlassian jira",)
    JQUERY = "jQuery"
    JSON = "JSON"
    JUNIT = "JUnit"
    JWT = "JWT"
    KAFKA = "Kafka", ("apache kafka",)
    KANBAN = "Kanban"
    KIBANA = "Kibana"
    KOTLIN = "Kotlin"
    KUBERNETES = "Kubernetes"
    LANGCHAIN = "LangChain"
    LARAVEL = "Laravel"
    LINUX = "Linux", ("ubuntu", "debian", "centos")
    LLM = "LLM"
    MAVEN = "Maven"
    MICROSERVICES = "Микросервисы"
    MIKROTIK = "MikroTik"
    ML = "ML"
    MLFLOW = "MLflow"
    MOBX = "MobX"
    MONGODB = "MongoDB"
    MS_EXCEL = "MS Excel"
    MS_SQL = "MS SQL", ("ms sql server", "mssql")
    MYSQL = "MySQL"
    NESTJS = "NestJS"
    NEXT_JS = "Next.js"
    NGINX = "Nginx"
    NODE_JS = "Node.js", ("nodejs",)
    NOSQL = "NoSQL"
    NUMPY = "Numpy"
    OFFICE = "MS Office", ("ms powerpoint", "word", "microsoft excel")
    ONE_C = "1С", ("1c",)
    OOP = "ООП", ("oop",)
    OPENAI = "OpenAI", ("openai api",)
    OPENSHIFT = "OpenShift"
    OPENSTACK = "OpenStack"
    PANDAS = "pandas"
    PHP = "PHP"
    POSTGIS = "PostGIS"
    POSTGRESQL = "PostgreSQL", ("postgres",)
    POSTMAN = "Postman"
    POWER_BI = "Power BI"
    POWERSHELL = "PowerShell"
    PROMETHEUS = "Prometheus"
    PYDANTIC = "Pydantic"
    PYTEST = "pytest"
    PYTHON = "Python", ("python 3.x", "python 3")
    PYTORCH = "PyTorch"
    QA = "QA"
    RABBITMQ = "RabbitMQ"
    REACT = "React", ("reactjs", "react hooks")
    REDIS = "Redis"
    REDUX = "Redux"
    REQUESTS = "requests"
    REST_API = "REST API", ("rest", "api", "restful api", "restful")
    RPC = "RPC", ("grpc",)
    RUBY = "Ruby"
    RXJS = "RxJS"
    S3 = "S3", ("aws s3", "aws")
    SCALA = "Scala"
    SCRUM = "SCRUM"
    SCSS = "SCSS", ("sass",)
    SELENIUM = "Selenium"
    SENTRY = "Sentry"
    SEO = "SEO"
    SOAP = "SOAP"
    SOLID = "SOLID"
    SPA = "SPA"
    SPARK = "Spark", ("apache spark", "pyspark")
    SPRING = "Spring", ("spring framework",)
    SPRING_BOOT = "Spring Boot"
    SQL = "SQL"
    SQLALCHEMY = "SQLAlchemy"
    SWAGGER = "Swagger"
    SWIFT = "Swift"
    SYMFONY = "Symfony"
    TAILWIND = "Tailwind"
    TCP_IP = "TCP/IP"
    TENSORFLOW = "TensorFlow"
    TERRAFORM = "Terraform"
    TYPESCRIPT = "TypeScript"
    UML = "UML"
    UNITTEST = "unittest"
    UX_UI = "UX/UI", ("ui/ux", "ui", "ux")
    VITE = "Vite"
    VPN = "VPN"
    VUE_JS = "Vue.js", ("vue", "vuejs")
    VUEX = "Vuex"
    WEBPACK = "Webpack"
    WEBSOCKET = "WebSocket", ("websockets",)
    WINDOWS = "Windows"
    WINDOWS_SERVER = "Windows Server"
    XML = "XML"
    YANDEX_CLOUD = "Yandex Cloud"
    ZABBIX = "Zabbix"
    ZUSTAND = "Zustand"

    # TODO: добавить проверку, что паттерны не совпадают с алиасами
    __ignore_patterns__ = (
        "adobe",
        "администр",
        "аналитик",
        "анализ",
        "управл",
        "делов",
        "развитие",
        "организатор",
        "продаж",
        "переговор",
        "перепис",
        "продвиж",
        "привлечен",
        "обуч",
        "ответств",
        "настрой",
        "постанов",
        "финанс",
        "работа",
        "моделир",
        "статист",
        "тестир",
        "визуализ",
        "прототип",
        "инвестиц",
        "объем",
        "маркет",
    )
