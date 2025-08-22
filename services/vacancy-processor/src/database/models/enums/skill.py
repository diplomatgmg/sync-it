from database.models.enums import BaseAliasEnum


__all__ = ["SkillEnum"]


class SkillEnum(BaseAliasEnum):
    __validate_ordering__ = True

    UNKNOWN = "Неизвестно"

    AGILE = "Agile"
    AIRFLOW = "Airflow"
    ANGULAR = "Angular"
    ANSIBLE = "Ansible"
    AWS = "AWS"
    BASH = "Bash"
    CPP = "C++"
    CELERY = "Celery"
    CI_CD = "CI/CD"
    CLICKHOUSE = "ClickHouse"
    CSS = "CSS", ("css3",)
    CYPRESS = "Cypress"
    DEVOPS = "DevOps"
    DJANGO = "Django", ("drf",)
    DOCKER = "Docker"
    DOCKER_COMPOSE = "Docker Compose"
    ELASTICSEARCH = "Elasticsearch", ("elk",)
    FAST_API = "FastAPI"
    FIGMA = "Figma"
    GIT = "Git"
    GITLAB = "GitLab"
    GO = "Go"
    GRAFANA = "Grafana"
    HTML = "HTML", ("html5",)
    HTTP = "HTTP"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"
    JENKINS = "Jenkins"
    JEST = "Jest"
    JIRA = "Jira"
    JUNIT = "JUnit"
    KAFKA = "Kafka"
    KOTLIN = "Kotlin"
    KUBERNETES = "Kubernetes"
    LARAVEL = "Laravel"
    LINUX = "Linux"
    MLFLOW = "MLflow"
    MONGODB = "MongoDB"
    MS_SQL = "MS SQL"
    MYSQL = "MySQL"
    NEXT_JS = "Next.js"
    NGINX = "Nginx"
    NODE_JS = "Node.js"
    PANDAS = "pandas"
    PHP = "PHP"
    POSTGIS = "PostGIS"
    POSTGRESQL = "PostgreSQL"
    POSTMAN = "Postman"
    PROMETHEUS = "Prometheus"
    PYTHON = "Python"
    PYTORCH = "PyTorch"
    RABBITMQ = "RabbitMQ"
    REACT = "React"
    REDIS = "Redis"
    REDUX = "Redux"
    REQUESTS = "requests"
    REST_API = "REST API", ("rest", "api")
    SCRUM = "SCRUM"
    SCSS = "SCSS"
    SELENIUM = "Selenium"
    SQL = "SQL"
    SQLALCHEMY = "SQLAlchemy"
    SWAGGER = "Swagger"
    SWIFT = "Swift"
    SYMFONY = "Symfony"
    TCP_IP = "TCP/IP"
    TERRAFORM = "Terraform"
    TYPESCRIPT = "TypeScript"
    VUE_JS = "Vue.js", ("vue",)
    WEBSOCKET = "WebSocket"
    WINDOWS = "Windows"
