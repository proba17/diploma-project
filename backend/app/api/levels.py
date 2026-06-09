from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.level import Level
from app.models.topic import Topic
from app.models.user import User
from app.schemas.level import LevelCreate, LevelRead, LevelUpdate
from app.api.auth import get_current_admin

router = APIRouter(prefix="/levels", tags=["Levels"])


@router.get("/", response_model=list[LevelRead])
def get_levels(db: Session = Depends(get_db)):
    return (
        db.query(Level)
        .filter(Level.is_active == True)
        .order_by(Level.order_number, Level.id)
        .all()
    )


@router.get("/{level_id}", response_model=LevelRead)
def get_level(level_id: int, db: Session = Depends(get_db)):
    level = (
        db.query(Level)
        .filter(Level.id == level_id, Level.is_active == True)
        .first()
    )

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found",
        )

    return level


@router.post("/seed")
def seed_levels(db: Session = Depends(get_db)):
    existing_levels = db.query(Level).count()

    if existing_levels > 0:
        return {
            "message": "Levels already exist",
            "count": existing_levels,
        }

    topic_packet = db.query(Topic).filter(Topic.title == "Сетевой пакет").first()
    topic_icmp = db.query(Topic).filter(Topic.title == "Протокол ICMP").first()
    topic_tcp = db.query(Topic).filter(Topic.title == "Протокол TCP").first()
    topic_udp = db.query(Topic).filter(Topic.title == "Протокол UDP").first()
    topic_syn = db.query(Topic).filter(Topic.title == "SYN-флуд").first()
    topic_firewall = db.query(Topic).filter(Topic.title == "Firewall").first()
    topic_http = db.query(Topic).filter(Topic.title == "Протокол HTTP").first()
    topic_dns = db.query(Topic).filter(Topic.title == "Протокол DNS").first()
    topic_port_scan = db.query(Topic).filter(Topic.title == "Сканирование портов").first()
    topic_ip_spoofing = db.query(Topic).filter(Topic.title == "IP Spoofing").first()
    topic_ids = db.query(Topic).filter(Topic.title == "IDS").first()
    topic_dpi = db.query(Topic).filter(Topic.title == "DPI").first()
    topic_payload = db.query(Topic).filter(Topic.title == "Malicious Payload").first()
    topic_botnet = db.query(Topic).filter(Topic.title == "Ботнет").first()

    def default_map(path_variant: int, difficulty: str = "easy"):
        single_paths = [
            [
                {"x": 0, "y": 250},
                {"x": 130, "y": 250},
                {"x": 220, "y": 150},
                {"x": 380, "y": 150},
                {"x": 470, "y": 310},
                {"x": 650, "y": 310},
                {"x": 770, "y": 220},
                {"x": 860, "y": 220},
            ],
            [
                {"x": 0, "y": 120},
                {"x": 160, "y": 120},
                {"x": 260, "y": 260},
                {"x": 420, "y": 260},
                {"x": 520, "y": 140},
                {"x": 700, "y": 140},
                {"x": 860, "y": 300},
            ],
            [
                {"x": 0, "y": 360},
                {"x": 140, "y": 360},
                {"x": 230, "y": 210},
                {"x": 390, "y": 210},
                {"x": 490, "y": 90},
                {"x": 650, "y": 90},
                {"x": 760, "y": 260},
                {"x": 860, "y": 260},
            ],
        ]

        medium_paths = [
            [
                {"x": 0, "y": 170},
                {"x": 150, "y": 170},
                {"x": 270, "y": 280},
                {"x": 470, "y": 280},
                {"x": 620, "y": 210},
                {"x": 860, "y": 220},
            ],
            [
                {"x": 0, "y": 330},
                {"x": 170, "y": 330},
                {"x": 280, "y": 210},
                {"x": 480, "y": 210},
                {"x": 630, "y": 300},
                {"x": 860, "y": 220},
            ],
        ]

        hard_paths = [
            [
                {"x": 0, "y": 110},
                {"x": 130, "y": 110},
                {"x": 230, "y": 210},
                {"x": 400, "y": 210},
                {"x": 540, "y": 120},
                {"x": 700, "y": 120},
                {"x": 860, "y": 220},
            ],
            [
                {"x": 0, "y": 390},
                {"x": 150, "y": 390},
                {"x": 250, "y": 300},
                {"x": 430, "y": 300},
                {"x": 560, "y": 390},
                {"x": 720, "y": 390},
                {"x": 860, "y": 220},
            ],
        ]

        if difficulty == "hard":
            selected_paths = hard_paths
            main_path = hard_paths[0]
            base = {"x": 860, "y": 220}
        elif difficulty == "medium":
            selected_paths = medium_paths
            main_path = medium_paths[0]
            base = {"x": 860, "y": 220}
        else:
            main_path = single_paths[path_variant % len(single_paths)]
            selected_paths = [main_path]
            base = main_path[-1]

        return {
            "path": main_path,
            "paths": selected_paths,
            "base": base,
            "width": 900,
            "height": 500,
        }

    router_acl = {
        "name": "Router ACL",
        "type": "router_acl",
        "module_code": "router_acl",
        "cost": 100,
        "range": 120,
        "damage": 1,
        "osi_level": 3,
        "analyzes": ["protocol", "src_ip", "dst_ip", "icmp_type"],
        "blocks": ["icmp_flood", "blocked_ip", "ip_spoofing"],
        "description": "Фильтрует трафик по IP-адресам, протоколам и ICMP.",
    }

    stateful_firewall = {
        "name": "Stateful Firewall",
        "type": "stateful_firewall",
        "module_code": "stateful_firewall",
        "cost": 150,
        "range": 135,
        "damage": 2,
        "osi_level": 4,
        "analyzes": [
            "protocol",
            "src_ip",
            "dst_ip",
            "src_port",
            "dst_port",
            "tcp_flags",
            "connection_state",
        ],
        "blocks": ["port_scan", "syn_flood", "unauthorized_port"],
        "description": "Анализирует TCP/UDP, порты и состояние соединений.",
    }

    anti_ddos = {
        "name": "Anti-DDoS",
        "type": "anti_ddos",
        "module_code": "anti_ddos",
        "cost": 200,
        "range": 155,
        "damage": 2,
        "osi_level": 4,
        "analyzes": ["packet_rate", "connection_rate", "src_ip", "protocol"],
        "blocks": ["icmp_flood", "udp_flood", "syn_flood", "botnet_ddos"],
        "description": "Обнаруживает аномальную частоту пакетов и DDoS-атаки.",
    }

    snort_ips = {
        "name": "Snort IPS",
        "type": "snort_ips",
        "module_code": "snort_ips",
        "cost": 220,
        "range": 145,
        "damage": 3,
        "osi_level": 7,
        "analyzes": ["signature", "payload", "protocol", "tcp_flags"],
        "blocks": ["known_exploit", "malware_traffic", "port_scan"],
        "description": "Блокирует известные атаки по сигнатурам.",
    }

    dns_filter = {
        "name": "DNS Filter",
        "type": "dns_filter",
        "module_code": "dns_filter",
        "cost": 180,
        "range": 135,
        "damage": 2,
        "osi_level": 7,
        "analyzes": ["domain", "dns_query", "application_protocol"],
        "blocks": ["malicious_domain", "dns_tunneling", "dns_flood"],
        "description": "Фильтрует DNS-запросы к вредоносным доменам.",
    }

    waf = {
        "name": "Web Application Firewall",
        "type": "waf",
        "module_code": "waf",
        "cost": 250,
        "range": 125,
        "damage": 3,
        "osi_level": 7,
        "analyzes": ["http_method", "url", "payload", "signature"],
        "blocks": ["sql_injection", "xss", "path_traversal", "command_injection"],
        "description": "Защищает веб-приложение от атак HTTP-уровня.",
    }

    email_gateway = {
        "name": "Email Security Gateway",
        "type": "email_gateway",
        "module_code": "email_gateway",
        "cost": 230,
        "range": 125,
        "damage": 3,
        "osi_level": 7,
        "analyzes": ["sender_email", "subject", "links", "attachment", "payload"],
        "blocks": ["phishing", "malware_attachment"],
        "description": "Проверяет письма, ссылки и вложения.",
    }

    levels = [
        Level(
            title="Router ACL: базовая фильтрация",
            description="Игрок знакомится с фильтрацией сетевого трафика по протоколу и IP-адресам.",
            topic="Сетевые пакеты",
            topic_id=topic_packet.id if topic_packet else None,
            campaign="Базовая кампания",
            order_number=1,
            difficulty="easy",
            base_health=100,
            start_resources=140,
            map_config=default_map(0, "easy"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 10,
                    "speed": 1.2,
                    "spawn_delay": 0.9,
                    "damage": 5,
                    "dst_port": 80,
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "ICMP",
                    "attack": "ICMP Flood",
                    "attack_type": "icmp_flood",
                    "count": 18,
                    "speed": 1.5,
                    "spawn_delay": 0.45,
                    "damage": 7,
                    "src_ip": "10.0.0.15",
                    "dst_ip": "192.168.1.10",
                    "packet_rate": 120,
                    "osi_level": 3,
                    "is_malicious": True,
                },
            ],
            defense_config=[router_acl],
            is_active=True,
        ),
        Level(
            title="IP-адресация и запрещённые источники",
            description="Уровень показывает, как ACL и firewall блокируют трафик от запрещённых IP-адресов.",
            topic="Firewall",
            topic_id=topic_firewall.id if topic_firewall else None,
            campaign="Базовая кампания",
            order_number=2,
            difficulty="easy",
            base_health=100,
            start_resources=160,
            map_config=default_map(1, "easy"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 12,
                    "speed": 1.2,
                    "spawn_delay": 0.8,
                    "damage": 5,
                    "src_ip": "192.168.1.20",
                    "dst_ip": "192.168.1.10",
                    "dst_port": 443,
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Blocked IP",
                    "attack_type": "blocked_ip",
                    "count": 20,
                    "speed": 1.5,
                    "spawn_delay": 0.5,
                    "damage": 6,
                    "src_ip": "203.0.113.66",
                    "dst_ip": "192.168.1.10",
                    "dst_port": 80,
                    "osi_level": 3,
                    "is_malicious": True,
                },
            ],
            defense_config=[router_acl],
            is_active=True,
        ),
        Level(
            title="Stateful Firewall: TCP/UDP и порты",
            description="Игрок учится фильтровать трафик по портам и состоянию соединений.",
            topic="TCP и UDP",
            topic_id=topic_tcp.id if topic_tcp else None,
            campaign="Базовая кампания",
            order_number=3,
            difficulty="easy",
            base_health=110,
            start_resources=180,
            map_config=default_map(2, "easy"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 12,
                    "speed": 1.2,
                    "spawn_delay": 0.75,
                    "damage": 5,
                    "dst_port": 443,
                    "connection_state": "established",
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Unauthorized Port",
                    "attack_type": "unauthorized_port",
                    "count": 20,
                    "speed": 1.5,
                    "spawn_delay": 0.45,
                    "damage": 6,
                    "dst_port": 22,
                    "connection_state": "new",
                    "osi_level": 4,
                    "is_malicious": True,
                },
            ],
            defense_config=[router_acl, stateful_firewall],
            is_active=True,
        ),
        Level(
            title="Port Scan",
            description="Игрок распознаёт сканирование портов и использует Stateful Firewall.",
            topic="Port Scanning",
            topic_id=topic_port_scan.id if topic_port_scan else None,
            campaign="Продвинутая кампания",
            order_number=4,
            difficulty="medium",
            base_health=120,
            start_resources=190,
            map_config=default_map(0, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5,
                    "dst_port": 80,
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Port Scan",
                    "attack_type": "port_scan",
                    "count": 28,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 6,
                    "dst_port": 22,
                    "tcp_flags": "SYN",
                    "signature": "multiple_ports_scan",
                    "osi_level": 4,
                    "is_malicious": True,
                },
            ],
            defense_config=[router_acl, stateful_firewall, snort_ips],
            is_active=True,
        ),
        Level(
            title="SYN Flood",
            description="Уровень показывает атаку SYN Flood и роль Anti-DDoS.",
            topic="TCP",
            topic_id=topic_syn.id if topic_syn else None,
            campaign="Продвинутая кампания",
            order_number=5,
            difficulty="medium",
            base_health=125,
            start_resources=210,
            map_config=default_map(1, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "attack": None,
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5,
                    "tcp_flags": "SYN,ACK",
                    "connection_state": "established",
                    "dst_port": 443,
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "SYN Flood",
                    "attack_type": "syn_flood",
                    "count": 34,
                    "speed": 1.8,
                    "spawn_delay": 0.3,
                    "damage": 8,
                    "tcp_flags": "SYN",
                    "packet_rate": 250,
                    "connection_state": "half_open",
                    "dst_port": 80,
                    "osi_level": 4,
                    "is_malicious": True,
                },
            ],
            defense_config=[stateful_firewall, anti_ddos],
            is_active=True,
        ),
        Level(
            title="UDP Flood",
            description="Игрок защищает сервер от большого количества UDP-пакетов.",
            topic="UDP",
            topic_id=topic_udp.id if topic_udp else None,
            campaign="Продвинутая кампания",
            order_number=6,
            difficulty="medium",
            base_health=130,
            start_resources=220,
            map_config=default_map(2, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "UDP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5,
                    "dst_port": 53,
                    "packet_rate": 20,
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "UDP",
                    "attack": "UDP Flood",
                    "attack_type": "udp_flood",
                    "count": 34,
                    "speed": 1.9,
                    "spawn_delay": 0.3,
                    "damage": 8,
                    "dst_port": 53,
                    "packet_rate": 300,
                    "osi_level": 4,
                    "is_malicious": True,
                },
            ],
            defense_config=[stateful_firewall, anti_ddos],
            is_active=True,
        ),
        Level(
            title="IP Spoofing",
            description="Уровень демонстрирует подмену IP-адреса источника.",
            topic="IP Spoofing",
            topic_id=topic_ip_spoofing.id if topic_ip_spoofing else None,
            campaign="Продвинутая кампания",
            order_number=7,
            difficulty="medium",
            base_health=135,
            start_resources=230,
            map_config=default_map(0, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5,
                    "src_ip": "192.168.1.25",
                    "dst_ip": "192.168.1.10",
                    "dst_port": 443,
                    "osi_level": 4,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "IP Spoofing",
                    "attack_type": "ip_spoofing",
                    "count": 26,
                    "speed": 1.7,
                    "spawn_delay": 0.4,
                    "damage": 7,
                    "src_ip": "192.168.1.25",
                    "real_src_ip": "198.51.100.44",
                    "dst_ip": "192.168.1.10",
                    "dst_port": 80,
                    "signature": "spoofed_source",
                    "osi_level": 3,
                    "is_malicious": True,
                },
            ],
            defense_config=[router_acl, stateful_firewall, snort_ips],
            is_active=True,
        ),
        Level(
            title="DNS Filter",
            description="Игрок фильтрует DNS-запросы к вредоносным доменам.",
            topic="DNS",
            topic_id=topic_dns.id if topic_dns else None,
            campaign="Экспертная кампания",
            order_number=8,
            difficulty="medium",
            base_health=140,
            start_resources=240,
            map_config=default_map(1, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "DNS",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.65,
                    "damage": 5,
                    "application_protocol": "DNS",
                    "domain": "example.com",
                    "dst_port": 53,
                    "osi_level": 7,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "DNS",
                    "attack": "Malicious Domain",
                    "attack_type": "malicious_domain",
                    "count": 24,
                    "speed": 1.6,
                    "spawn_delay": 0.4,
                    "damage": 7,
                    "application_protocol": "DNS",
                    "domain": "evil-control.net",
                    "dst_port": 53,
                    "signature": "malicious_domain",
                    "osi_level": 7,
                    "is_malicious": True,
                },
                {
                    "wave": 3,
                    "packet_type": "attack",
                    "protocol": "DNS",
                    "attack": "DNS Tunneling",
                    "attack_type": "dns_tunneling",
                    "count": 24,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 8,
                    "application_protocol": "DNS",
                    "domain": "very-long-encoded-subdomain.attacker.net",
                    "dst_port": 53,
                    "signature": "dns_tunneling",
                    "osi_level": 7,
                    "is_malicious": True,
                },
            ],
            defense_config=[stateful_firewall, anti_ddos, dns_filter],
            is_active=True,
        ),
        Level(
            title="Snort IPS: сигнатуры атак",
            description="Игрок использует IPS для блокировки известных атак по сигнатурам.",
            topic="IDS",
            topic_id=topic_ids.id if topic_ids else None,
            campaign="Экспертная кампания",
            order_number=9,
            difficulty="hard",
            base_health=150,
            start_resources=260,
            map_config=default_map(2, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "HTTP",
                    "count": 16,
                    "speed": 1.3,
                    "spawn_delay": 0.6,
                    "damage": 5,
                    "application_protocol": "HTTP",
                    "payload": "GET /index.html",
                    "osi_level": 7,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Known Exploit",
                    "attack_type": "known_exploit",
                    "count": 28,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 8,
                    "signature": "CVE-like exploit attempt",
                    "payload": "EXPLOIT_PATTERN",
                    "osi_level": 7,
                    "is_malicious": True,
                },
            ],
            defense_config=[stateful_firewall, snort_ips],
            is_active=True,
        ),
        Level(
            title="WAF: SQL Injection",
            description="Игрок защищает веб-приложение от SQL-инъекций.",
            topic="Deep Packet Inspection",
            topic_id=topic_payload.id if topic_payload else None,
            campaign="Экспертная кампания",
            order_number=10,
            difficulty="hard",
            base_health=155,
            start_resources=280,
            map_config=default_map(0, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "HTTP",
                    "count": 16,
                    "speed": 1.3,
                    "spawn_delay": 0.6,
                    "damage": 5,
                    "application_protocol": "HTTP",
                    "http_method": "GET",
                    "url": "/login?id=1",
                    "payload": "GET /login?id=1",
                    "dst_port": 80,
                    "osi_level": 7,
                    "is_malicious": False,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "SQL Injection",
                    "attack_type": "sql_injection",
                    "count": 30,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 9,
                    "application_protocol": "HTTP",
                    "http_method": "GET",
                    "url": "/login?id=1 OR 1=1",
                    "payload": "GET /login?id=1 OR 1=1 --",
                    "signature": "sql_injection",
                    "dst_port": 80,
                    "osi_level": 7,
                    "is_malicious": True,
                },
            ],
            defense_config=[stateful_firewall, snort_ips, waf],
            is_active=True,
        ),
        Level(
            title="WAF Advanced: XSS и Path Traversal",
            description="Игрок блокирует атаки XSS и Path Traversal на прикладном уровне.",
            topic="Malicious Payload",
            topic_id=topic_payload.id if topic_payload else None,
            campaign="Экспертная кампания",
            order_number=11,
            difficulty="hard",
            base_health=165,
            start_resources=300,
            map_config=default_map(1, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "XSS",
                    "attack_type": "xss",
                    "count": 24,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 8,
                    "application_protocol": "HTTP",
                    "http_method": "GET",
                    "url": "/search?q=<script>alert(1)</script>",
                    "payload": "<script>alert(1)</script>",
                    "signature": "xss",
                    "dst_port": 80,
                    "osi_level": 7,
                    "is_malicious": True,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "Path Traversal",
                    "attack_type": "path_traversal",
                    "count": 24,
                    "speed": 1.8,
                    "spawn_delay": 0.35,
                    "damage": 8,
                    "application_protocol": "HTTP",
                    "http_method": "GET",
                    "url": "/download?file=../../etc/passwd",
                    "payload": "../../etc/passwd",
                    "signature": "path_traversal",
                    "dst_port": 80,
                    "osi_level": 7,
                    "is_malicious": True,
                },
            ],
            defense_config=[snort_ips, waf],
            is_active=True,
        ),
        Level(
            title="Финальная защита корпоративной сети",
            description="Финальный уровень объединяет DDoS, DNS, web-атаки, фишинг и сигнатурный анализ.",
            topic="Комплексная защита",
            topic_id=topic_dpi.id if topic_dpi else None,
            campaign="Финальная кампания",
            order_number=12,
            difficulty="hard",
            base_health=180,
            start_resources=340,
            map_config=default_map(2, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Port Scan",
                    "attack_type": "port_scan",
                    "count": 22,
                    "speed": 1.6,
                    "spawn_delay": 0.35,
                    "damage": 6,
                    "dst_port": 22,
                    "tcp_flags": "SYN",
                    "signature": "multiple_ports_scan",
                    "osi_level": 4,
                    "is_malicious": True,
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "UDP",
                    "attack": "UDP Flood",
                    "attack_type": "udp_flood",
                    "count": 30,
                    "speed": 1.9,
                    "spawn_delay": 0.28,
                    "damage": 8,
                    "dst_port": 53,
                    "packet_rate": 350,
                    "osi_level": 4,
                    "is_malicious": True,
                },
                {
                    "wave": 3,
                    "packet_type": "attack",
                    "protocol": "DNS",
                    "attack": "DNS Tunneling",
                    "attack_type": "dns_tunneling",
                    "count": 26,
                    "speed": 1.8,
                    "spawn_delay": 0.32,
                    "damage": 8,
                    "application_protocol": "DNS",
                    "domain": "encoded-data.attacker.net",
                    "signature": "dns_tunneling",
                    "osi_level": 7,
                    "is_malicious": True,
                },
                {
                    "wave": 4,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "SQL Injection",
                    "attack_type": "sql_injection",
                    "count": 28,
                    "speed": 1.8,
                    "spawn_delay": 0.3,
                    "damage": 9,
                    "application_protocol": "HTTP",
                    "url": "/login?id=1 OR 1=1",
                    "payload": "GET /login?id=1 OR 1=1 --",
                    "signature": "sql_injection",
                    "osi_level": 7,
                    "is_malicious": True,
                },
                {
                    "wave": 5,
                    "packet_type": "attack",
                    "protocol": "SMTP",
                    "attack": "Phishing",
                    "attack_type": "phishing",
                    "count": 22,
                    "speed": 1.6,
                    "spawn_delay": 0.4,
                    "damage": 8,
                    "application_protocol": "SMTP",
                    "sender_email": "security-update@fake-bank.example",
                    "subject": "Urgent password reset",
                    "links": ["http://fake-bank-login.example"],
                    "signature": "phishing",
                    "osi_level": 7,
                    "is_malicious": True,
                },
            ],
            defense_config=[
                router_acl,
                stateful_firewall,
                anti_ddos,
                snort_ips,
                dns_filter,
                waf,
                email_gateway,
            ],
            is_active=True,
        ),
    ]

    db.add_all(levels)
    db.commit()

    return {
        "message": "Levels created",
        "count": len(levels),
    }


@router.post("/", response_model=LevelRead)
def create_level(
    level_data: LevelCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    level = Level(
        title=level_data.title,
        description=level_data.description,
        topic=level_data.topic,
        topic_id=level_data.topic_id,
        difficulty=level_data.difficulty,
        base_health=level_data.base_health,
        start_resources=level_data.start_resources,
        map_config=level_data.map_config,
        waves_config=level_data.waves_config,
        defense_config=level_data.defense_config,
        is_active=True,
        campaign=level_data.campaign,
        order_number=level_data.order_number,
    )

    db.add(level)
    db.commit()
    db.refresh(level)

    return level


@router.put("/{level_id}", response_model=LevelRead)
def update_level(
    level_id: int,
    level_data: LevelUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    level = db.query(Level).filter(Level.id == level_id).first()

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found",
        )

    update_data = level_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(level, field, value)

    db.commit()
    db.refresh(level)

    return level


@router.delete("/{level_id}")
def delete_level(
    level_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    level = db.query(Level).filter(Level.id == level_id).first()

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found",
        )

    level.is_active = False
    db.commit()

    return {
        "message": "Level disabled",
        "level_id": level_id,
    }


@router.get("/{level_id}/topic")
def get_level_topic(
    level_id: int,
    db: Session = Depends(get_db),
):
    level = (
        db.query(Level)
        .filter(Level.id == level_id, Level.is_active == True)
        .first()
    )

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found",
        )

    if level.topic_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic for this level not found",
        )

    topic = (
        db.query(Topic)
        .filter(Topic.id == level.topic_id, Topic.is_active == True)
        .first()
    )

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )

    return topic