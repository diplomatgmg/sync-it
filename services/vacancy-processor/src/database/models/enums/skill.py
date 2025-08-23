from database.models.enums import BaseAliasEnum


__all__ = ["SkillEnum"]


class SkillEnum(BaseAliasEnum):
    __validate_ordering__ = True

    UNKNOWN = "Неизвестно"

    ACTIVE_DIRECTORY = "Active Directory"
    AGILE = "Agile"
    AIOHTTP = "aiohttp"
    AIRFLOW = "Airflow", ("apache airflow",)
    ALLURE = "Allure"
    ANGULAR = "Angular"
    ANSIBLE = "Ansible"
    ARGOCD = "ArgoCD"
    ASP_NET = "ASP.NET"
    ASYNCIO = "asyncio"
    AWS = "AWS"
    AXIOS = "Axios"
    AZURE = "Azure"
    BASH = "Bash"
    BIG_DATA = "Big Data", ("работа с большим объемом информации",)
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
    DEVOPS = "DevOps"
    DJANGO = "Django", ("drf", "django orm")
    DOCKER = "Docker"
    DOCKER_COMPOSE = "Docker Compose"
    ELASTICSEARCH = "Elasticsearch", ("elk", "elk stack")
    ENGLISH = "Английский язык"
    ETL = "ETL"
    EXCEL = "Excel"
    FAST_API = "FastAPI"
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
    HADOOP = "Hadoop"
    HELM = "Helm"
    HTML = "HTML", ("html5",)
    HTTP = "HTTP", ("https", "http/https")
    IOS = "iOS"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"
    JENKINS = "Jenkins"
    JEST = "Jest"
    JIRA = "Jira", ("atlassian jira",)
    JQUERY = "jQuery"
    JSON = "JSON"
    JUNIT = "JUnit"
    KAFKA = "Kafka", ("apache kafka",)
    KANBAN = "Kanban"
    KIBANA = "Kibana"
    KOTLIN = "Kotlin"
    KUBERNETES = "Kubernetes"
    LARAVEL = "Laravel"
    LINUX = "Linux", ("ubuntu", "debian")
    LLM = "LLM"
    MAVEN = "Maven"
    MICROSERVICES = "Микросервисы"
    ML = "ML"
    MLFLOW = "MLflow"
    MOBX = "MobX"
    MONGODB = "MongoDB"
    MS_EXCEL = "MS Excel"
    MS_SQL = "MS SQL"
    MYSQL = "MySQL"
    NEXT_JS = "Next.js"
    NGINX = "Nginx"
    NODE_JS = "Node.js", ("nodejs",)
    NOSQL = "NoSQL"
    NUMPY = "Numpy"
    ONE_C = "1С", ("1c",)
    OOP = "ООП", ("oop",)
    OPENSHIFT = "OpenShift"
    PANDAS = "pandas"
    PHP = "PHP"
    POSTGIS = "PostGIS"
    POSTGRESQL = "PostgreSQL", ("postgres",)
    POSTMAN = "Postman"
    POWER_BI = "Power BI"
    PROMETHEUS = "Prometheus"
    PYDANTIC = "Pydantic"
    PYTEST = "pytest"
    PYTHON = "Python"
    PYTORCH = "PyTorch"
    QA = "QA"
    RABBITMQ = "RabbitMQ"
    REACT = "React", ("reactjs", "react hooks")
    REDIS = "Redis"
    REDUX = "Redux"
    REQUESTS = "requests"
    REST_API = "REST API", ("rest", "api", "restful api", "restful")
    RUBY = "Ruby"
    RXJS = "RxJS"
    SCALA = "Scala"
    SCRUM = "SCRUM"
    SCSS = "SCSS"
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
    UX_UI = "UX/UI", ("ui/ux", "ui", "ux")
    VITE = "Vite"
    VUE_JS = "Vue.js", ("vue", "vuejs")
    VUEX = "Vuex"
    WEBPACK = "Webpack"
    WEBSOCKET = "WebSocket"
    WINDOWS = "Windows"
    XML = "XML"
    YANDEX_CLOUD = "Yandex Cloud"
    ZABBIX = "Zabbix"
    ZUSTAND = "Zustand"

    # TODO: добавить проверку, что паттерны не совпадают с алиасами
    __ignore_patterns__ = (
        "аналитика",
        "аналитическое",
        "управление",
        "деловая",
        "развитие",
        "организатор",
        "деловое",
        "продаж",
        "переговор",
        "переписка",
        "продвижение",
        "аналитика",
        "привлечение",
        "обучение",
        "ответствен",
    )
