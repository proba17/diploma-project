from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.topic import Topic
from app.db.database import get_db
from app.models.level import Level
from app.schemas.level import LevelCreate, LevelRead, LevelUpdate
from app.api.auth import get_current_admin
from app.models.user import User
router = APIRouter(prefix="/levels", tags=["Levels"])


@router.get("/", response_model=list[LevelRead])
def get_levels(db: Session = Depends(get_db)):
    levels = (
        db.query(Level)
        .filter(Level.is_active == True)
        .order_by(Level.order_number, Level.id)
        .all()
    )

    return levels


@router.get("/{level_id}", response_model=LevelRead)
def get_level(
    level_id: int,
    db: Session = Depends(get_db)
):
    level = (
        db.query(Level)
        .filter(Level.id == level_id, Level.is_active == True)
        .first()
    )

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )

    return level


@router.post("/seed")
def seed_levels(db: Session = Depends(get_db)):
    existing_levels = db.query(Level).count()

    if existing_levels > 0:
        return {
            "message": "Levels already exist",
            "count": existing_levels
        }

    topic_packet = db.query(Topic).filter(Topic.title == "Сетевой пакет").first()
    topic_icmp = db.query(Topic).filter(Topic.title == "Протокол ICMP").first()
    topic_tcp = db.query(Topic).filter(Topic.title == "Протокол TCP").first()
    topic_udp = db.query(Topic).filter(Topic.title == "Протокол UDP").first()
    topic_syn = db.query(Topic).filter(Topic.title == "SYN-флуд").first()
    topic_firewall = db.query(Topic).filter(Topic.title == "Firewall").first()
    topic_rate = db.query(Topic).filter(Topic.title == "Rate Limiter").first()
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
                {"x": 860, "y": 220}
            ],
            [
                {"x": 0, "y": 120},
                {"x": 160, "y": 120},
                {"x": 260, "y": 260},
                {"x": 420, "y": 260},
                {"x": 520, "y": 140},
                {"x": 700, "y": 140},
                {"x": 860, "y": 300}
            ],
            [
                {"x": 0, "y": 360},
                {"x": 140, "y": 360},
                {"x": 230, "y": 210},
                {"x": 390, "y": 210},
                {"x": 490, "y": 90},
                {"x": 650, "y": 90},
                {"x": 760, "y": 260},
                {"x": 860, "y": 260}
            ]
        ]

        medium_paths = [
            [
                {"x": 0, "y": 170},
                {"x": 150, "y": 170},
                {"x": 270, "y": 280},
                {"x": 470, "y": 280},
                {"x": 620, "y": 210},
                {"x": 860, "y": 220}
            ],
            [
                {"x": 0, "y": 330},
                {"x": 170, "y": 330},
                {"x": 280, "y": 210},
                {"x": 480, "y": 210},
                {"x": 630, "y": 300},
                {"x": 860, "y": 220}
            ]
        ]

        hard_paths = [
            [
                {"x": 0, "y": 110},
                {"x": 130, "y": 110},
                {"x": 230, "y": 210},
                {"x": 400, "y": 210},
                {"x": 540, "y": 120},
                {"x": 700, "y": 120},
                {"x": 860, "y": 220}
            ],
            [
                {"x": 0, "y": 390},
                {"x": 150, "y": 390},
                {"x": 250, "y": 300},
                {"x": 430, "y": 300},
                {"x": 560, "y": 390},
                {"x": 720, "y": 390},
                {"x": 860, "y": 220}
            ]
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
            "height": 500
        }


    basic_filter = {
        "name": "Базовый фильтр",
        "type": "protocol_filter",
        "cost": 30,
        "range": 120,
        "damage": 1,
        "description": "Фильтрует пакеты по выбранному протоколу."
    }

    firewall = {
        "name": "Firewall",
        "type": "firewall",
        "cost": 70,
        "range": 145,
        "damage": 2,
        "description": "Блокирует подозрительный TCP-трафик и атаки."
    }

    rate_limiter = {
        "name": "Rate Limiter",
        "type": "rate_limiter",
        "cost": 60,
        "range": 150,
        "damage": 2,
        "description": "Ограничивает частоту однотипных запросов."
    }

    icmp_filter = {
        "name": "ICMP-фильтр",
        "type": "icmp_filter",
        "cost": 40,
        "range": 135,
        "damage": 2,
        "description": "Блокирует подозрительные ICMP-пакеты."
    }

    udp_filter = {
        "name": "UDP-фильтр",
        "type": "udp_filter",
        "cost": 50,
        "range": 135,
        "damage": 2,
        "description": "Блокирует подозрительный UDP-трафик."
    }

    syn_protection = {
        "name": "SYN-защита",
        "type": "syn_protection",
        "cost": 80,
        "range": 165,
        "damage": 3,
        "description": "Эффективна против SYN Flood."
    }

    acl_filter = {
        "name": "ACL-фильтр",
        "type": "acl_filter",
        "cost": 65,
        "range": 145,
        "damage": 2,
        "description": "Фильтрует трафик по правилам доступа."
    }

    ids = {
        "name": "IDS",
        "type": "ids",
        "cost": 85,
        "range": 170,
        "damage": 2,
        "description": "Обнаруживает подозрительную сетевую активность."
    }

    dpi = {
        "name": "DPI",
        "type": "dpi",
        "cost": 100,
        "range": 180,
        "damage": 3,
        "description": "Анализирует содержимое пакетов."
    }

    levels = [
        Level(
            title="Основы сетевых пакетов",
            description="Первый уровень знакомит пользователя с движением сетевых пакетов по маршруту.",
            topic="Сетевые пакеты",
            topic_id=topic_packet.id if topic_packet else None,
            campaign="Базовая кампания",
            order_number=1,
            difficulty="easy",
            base_health=100,
            start_resources=130,
            map_config=default_map(0, "easy"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 10,
                    "speed": 1.2,
                    "spawn_delay": 0.9,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "normal",
                    "protocol": "UDP",
                    "count": 12,
                    "speed": 1.3,
                    "spawn_delay": 0.8,
                    "damage": 5
                }
            ],
            defense_config=[basic_filter],
            is_active=True
        ),
        Level(
            title="ICMP и ping-запросы",
            description="Уровень показывает работу ICMP-пакетов и базовую защиту от ICMP-флуда.",
            topic="ICMP",
            topic_id=topic_icmp.id if topic_icmp else None,
            campaign="Базовая кампания",
            order_number=2,
            difficulty="easy",
            base_health=100,
            start_resources=150,
            map_config=default_map(1, "easy"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "ICMP",
                    "count": 10,
                    "speed": 1.2,
                    "spawn_delay": 0.8,
                    "damage": 4
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "ICMP",
                    "attack": "ICMP Flood",
                    "count": 24,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 7
                }
            ],
            defense_config=[basic_filter, icmp_filter, rate_limiter],
            is_active=True
        ),
        Level(
            title="TCP/UDP фильтрация",
            description="Пользователь учится отличать TCP и UDP-пакеты и использовать базовую фильтрацию.",
            topic="TCP и UDP",
            topic_id=topic_tcp.id if topic_tcp else None,
            campaign="Базовая кампания",
            order_number=3,
            difficulty="easy",
            base_health=110,
            start_resources=160,
            map_config=default_map(2, "easy"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 12,
                    "speed": 1.2,
                    "spawn_delay": 0.7,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "normal",
                    "protocol": "UDP",
                    "count": 16,
                    "speed": 1.4,
                    "spawn_delay": 0.6,
                    "damage": 5
                }
            ],
            defense_config=[basic_filter, firewall, udp_filter],
            is_active=True
        ),
        Level(
            title="UDP Flood",
            description="Уровень посвящён UDP-трафику и защите от UDP-флуда.",
            topic="UDP",
            topic_id=topic_udp.id if topic_udp else None,
            campaign="Продвинутая кампания",
            order_number=4,
            difficulty="medium",
            base_health=120,
            start_resources=180,
            map_config=default_map(0, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "UDP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "UDP",
                    "attack": "UDP Flood",
                    "count": 30,
                    "speed": 1.8,
                    "spawn_delay": 0.3,
                    "damage": 8
                }
            ],
            defense_config=[basic_filter, udp_filter, rate_limiter],
            is_active=True
        ),
        Level(
            title="SYN Flood",
            description="Пользователь изучает TCP SYN-запросы и защиту от SYN-флуда.",
            topic="TCP",
            topic_id=topic_syn.id if topic_syn else None,
            campaign="Продвинутая кампания",
            order_number=5,
            difficulty="medium",
            base_health=120,
            start_resources=190,
            map_config=default_map(1, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "SYN Flood",
                    "count": 32,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 8
                }
            ],
            defense_config=[basic_filter, firewall, syn_protection, rate_limiter],
            is_active=True
        ),
        Level(
            title="Сканирование портов",
            description="Игрок должен распознать подозрительную активность, похожую на сканирование портов.",
            topic="Port Scanning",
            topic_id=topic_port_scan.id if topic_port_scan else None,
            campaign="Продвинутая кампания",
            order_number=6,
            difficulty="medium",
            base_health=130,
            start_resources=190,
            map_config=default_map(2, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 12,
                    "speed": 1.2,
                    "spawn_delay": 0.7,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Port Scan",
                    "count": 28,
                    "speed": 1.6,
                    "spawn_delay": 0.35,
                    "damage": 6
                }
            ],
            defense_config=[basic_filter, firewall, acl_filter, ids],
            is_active=True
        ),
        Level(
            title="IP Spoofing",
            description="Уровень демонстрирует подмену IP-адреса источника и необходимость фильтрации по правилам.",
            topic="IP Spoofing",
            topic_id=topic_ip_spoofing.id if topic_ip_spoofing else None,
            campaign="Продвинутая кампания",
            order_number=7,
            difficulty="medium",
            base_health=130,
            start_resources=200,
            map_config=default_map(0, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "TCP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.7,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "IP Spoofing",
                    "count": 30,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 7
                }
            ],
            defense_config=[basic_filter, firewall, acl_filter, ids],
            is_active=True
        ),
        Level(
            title="HTTP и DNS трафик",
            description="Пользователь анализирует HTTP и DNS-пакеты и блокирует подозрительные запросы.",
            topic="HTTP/DNS",
            topic_id=topic_http.id if topic_http else None,
            campaign="Продвинутая кампания",
            order_number=8,
            difficulty="medium",
            base_health=140,
            start_resources=210,
            map_config=default_map(1, "medium"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "HTTP",
                    "count": 14,
                    "speed": 1.3,
                    "spawn_delay": 0.65,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "normal",
                    "protocol": "DNS",
                    "count": 14,
                    "speed": 1.4,
                    "spawn_delay": 0.65,
                    "damage": 5
                },
                {
                    "wave": 3,
                    "packet_type": "attack",
                    "protocol": "DNS",
                    "attack": "DNS Flood",
                    "count": 26,
                    "speed": 1.8,
                    "spawn_delay": 0.35,
                    "damage": 7
                }
            ],
            defense_config=[basic_filter, firewall, rate_limiter, ids],
            is_active=True
        ),
        Level(
            title="Смешанная атака",
            description="Игрок сталкивается сразу с несколькими типами атак и должен комбинировать защитные модули.",
            topic="Комплексная защита",
            topic_id=topic_rate.id if topic_rate else None,
            campaign="Экспертная кампания",
            order_number=9,
            difficulty="hard",
            base_health=150,
            start_resources=240,
            map_config=default_map(2, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "attack",
                    "protocol": "ICMP",
                    "attack": "ICMP Flood",
                    "count": 22,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 7
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "UDP",
                    "attack": "UDP Flood",
                    "count": 24,
                    "speed": 1.8,
                    "spawn_delay": 0.32,
                    "damage": 8
                },
                {
                    "wave": 3,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "SYN Flood",
                    "count": 24,
                    "speed": 1.8,
                    "spawn_delay": 0.35,
                    "damage": 8
                }
            ],
            defense_config=[basic_filter, firewall, icmp_filter, udp_filter, syn_protection, rate_limiter],
            is_active=True
        ),
        Level(
            title="Malicious Payload",
            description="Уровень посвящён вредоносной полезной нагрузке и необходимости глубокого анализа пакетов.",
            topic="Deep Packet Inspection",
            topic_id=topic_payload.id if topic_payload else None,
            campaign="Экспертная кампания",
            order_number=10,
            difficulty="hard",
            base_health=150,
            start_resources=250,
            map_config=default_map(0, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "normal",
                    "protocol": "HTTP",
                    "count": 16,
                    "speed": 1.3,
                    "spawn_delay": 0.6,
                    "damage": 5
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "Malicious Payload",
                    "count": 30,
                    "speed": 1.7,
                    "spawn_delay": 0.35,
                    "damage": 9
                }
            ],
            defense_config=[basic_filter, firewall, ids, dpi],
            is_active=True
        ),
        Level(
            title="Ботнет-атака",
            description="Имитация распределённой атаки с большим количеством пакетов разных протоколов.",
            topic="Botnet",
            topic_id=topic_botnet.id if topic_botnet else None,
            campaign="Экспертная кампания",
            order_number=11,
            difficulty="hard",
            base_health=160,
            start_resources=270,
            map_config=default_map(1, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "attack",
                    "protocol": "ICMP",
                    "attack": "Botnet ICMP",
                    "count": 22,
                    "speed": 1.8,
                    "spawn_delay": 0.32,
                    "damage": 7
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "UDP",
                    "attack": "Botnet UDP",
                    "count": 26,
                    "speed": 1.9,
                    "spawn_delay": 0.28,
                    "damage": 8
                },
                {
                    "wave": 3,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "Botnet HTTP",
                    "count": 28,
                    "speed": 1.9,
                    "spawn_delay": 0.28,
                    "damage": 8
                }
            ],
            defense_config=[basic_filter, firewall, rate_limiter, ids, dpi],
            is_active=True
        ),
        Level(
            title="Финальная комплексная защита",
            description="Финальный уровень объединяет флуд-атаки, подмену адресов, сканирование и вредоносную нагрузку.",
            topic="Комплексная защита",
            topic_id=topic_dpi.id if topic_dpi else None,
            campaign="Экспертная кампания",
            order_number=12,
            difficulty="hard",
            base_health=180,
            start_resources=300,
            map_config=default_map(2, "hard"),
            waves_config=[
                {
                    "wave": 1,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "Port Scan",
                    "count": 22,
                    "speed": 1.6,
                    "spawn_delay": 0.35,
                    "damage": 6
                },
                {
                    "wave": 2,
                    "packet_type": "attack",
                    "protocol": "TCP",
                    "attack": "IP Spoofing",
                    "count": 24,
                    "speed": 1.7,
                    "spawn_delay": 0.32,
                    "damage": 7
                },
                {
                    "wave": 3,
                    "packet_type": "attack",
                    "protocol": "UDP",
                    "attack": "UDP Flood",
                    "count": 28,
                    "speed": 1.9,
                    "spawn_delay": 0.28,
                    "damage": 8
                },
                {
                    "wave": 4,
                    "packet_type": "attack",
                    "protocol": "HTTP",
                    "attack": "Malicious Payload",
                    "count": 30,
                    "speed": 1.8,
                    "spawn_delay": 0.3,
                    "damage": 9
                }
            ],
            defense_config=[basic_filter, firewall, acl_filter, ids, dpi, rate_limiter, syn_protection],
            is_active=True
        ),
    ]

    db.add_all(levels)
    db.commit()

    return {
        "message": "Levels created",
        "count": len(levels)
    }

@router.post("/", response_model=LevelRead)
def create_level(
    level_data: LevelCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
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
        campaign = level_data.campaign,
        order_number = level_data.order_number,
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
    current_admin: User = Depends(get_current_admin)
):
    level = db.query(Level).filter(Level.id == level_id).first()

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
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
    current_admin: User = Depends(get_current_admin)

):
    level = db.query(Level).filter(Level.id == level_id).first()

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )

    level.is_active = False

    db.commit()

    return {
        "message": "Level disabled",
        "level_id": level_id
    }

@router.get("/{level_id}/topic")
def get_level_topic(
    level_id: int,
    db: Session = Depends(get_db)
):
    level = (
        db.query(Level)
        .filter(Level.id == level_id, Level.is_active == True)
        .first()
    )

    if level is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level not found"
        )

    if level.topic_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic for this level not found"
        )

    topic = (
        db.query(Topic)
        .filter(Topic.id == level.topic_id, Topic.is_active == True)
        .first()
    )

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    return topic