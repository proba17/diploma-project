from sqlalchemy.orm import Session

from app.models.defense_module import DefenseModule


def seed_defense_modules(db: Session):

    modules = [

        {
            "code": "router_acl",
            "name": "Router ACL",
            "description": (
                "Списки контроля доступа маршрутизатора. "
                "Фильтрация пакетов по IP-адресам, подсетям и протоколам."
            ),
            "osi_level": 3,
            "analyzes": [
                "protocol",
                "src_ip",
                "dst_ip",
                "icmp_type"
            ],
            "blocks": [
                "blocked_ip",
                "private_ip",
                "ip_spoofing"
            ],
            "cost": 100,
            "damage": 1,
            "range": 120,
        },

        {
            "code": "stateful_firewall",
            "name": "Stateful Firewall",
            "description": (
                "Межсетевой экран с контролем состояния соединений. "
                "Анализирует TCP/UDP, порты и состояние сессий."
            ),
            "osi_level": 4,
            "analyzes": [
                "protocol",
                "src_port",
                "dst_port",
                "tcp_flags",
                "connection_state"
            ],
            "blocks": [
                "unauthorized_port",
                "syn_flood"
            ],
            "cost": 150,
            "damage": 2,
            "range": 130,
        },

        {
            "code": "anti_ddos",
            "name": "Anti-DDoS",
            "description": (
                "Система защиты от атак типа отказ в обслуживании."
            ),
            "osi_level": 4,
            "analyzes": [
                "packet_rate",
                "connection_rate",
                "src_ip",
                "protocol"
            ],
            "blocks": [
                "syn_flood",
                "udp_flood",
                "icmp_flood",
                "http_flood"
            ],
            "cost": 200,
            "damage": 2,
            "range": 150,
        },

        {
            "code": "snort_ips",
            "name": "Snort IPS",
            "description": (
                "Система предотвращения вторжений на основе сигнатур."
            ),
            "osi_level": 7,
            "analyzes": [
                "signature",
                "payload",
                "protocol"
            ],
            "blocks": [
                "port_scan",
                "known_exploit",
                "malware_traffic",
                "botnet"
            ],
            "cost": 220,
            "damage": 3,
            "range": 140,
        },

        {
            "code": "dns_filter",
            "name": "DNS Filter",
            "description": (
                "Фильтрация DNS-запросов к вредоносным доменам."
            ),
            "osi_level": 7,
            "analyzes": [
                "domain",
                "dns_query",
                "application_protocol"
            ],
            "blocks": [
                "malicious_domain",
                "dns_tunneling",
                "c2_domain"
            ],
            "cost": 180,
            "damage": 2,
            "range": 130,
        },

        {
            "code": "waf",
            "name": "Web Application Firewall",
            "description": (
                "Защита веб-приложений от атак уровня приложения."
            ),
            "osi_level": 7,
            "analyzes": [
                "http_method",
                "url",
                "payload",
                "signature"
            ],
            "blocks": [
                "sql_injection",
                "xss",
                "path_traversal",
                "command_injection"
            ],
            "cost": 250,
            "damage": 3,
            "range": 120,
        },

        {
            "code": "email_gateway",
            "name": "Email Security Gateway",
            "description": (
                "Почтовый шлюз безопасности для проверки писем и вложений."
            ),
            "osi_level": 7,
            "analyzes": [
                "sender_email",
                "subject",
                "links",
                "attachment"
            ],
            "blocks": [
                "phishing",
                "malware_attachment",
                "spam"
            ],
            "cost": 230,
            "damage": 3,
            "range": 120,
        },
    ]

    for item in modules:

        exists = (
            db.query(DefenseModule)
            .filter(
                DefenseModule.code == item["code"]
            )
            .first()
        )

        if not exists:
            db.add(
                DefenseModule(**item)
            )

    db.commit()