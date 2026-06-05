from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_admin
from app.db.database import get_db
from app.models.topic import Topic
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicRead, TopicUpdate


router = APIRouter(prefix="/topics", tags=["Topics"])


@router.post("/", response_model=TopicRead)
def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    topic = Topic(
        title=topic_data.title,
        short_description=topic_data.short_description,
        content=topic_data.content,
        category=topic_data.category,
        order_number=topic_data.order_number,
        is_active=True
    )

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic


@router.get("/", response_model=list[TopicRead])
def get_topics(db: Session = Depends(get_db)):
    topics = (
        db.query(Topic)
        .filter(Topic.is_active == True)
        .order_by(Topic.order_number)
        .all()
    )

    return topics


@router.get("/{topic_id}", response_model=TopicRead)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    topic = (
        db.query(Topic)
        .filter(Topic.id == topic_id, Topic.is_active == True)
        .first()
    )

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    return topic


@router.put("/{topic_id}", response_model=TopicRead)
def update_topic(
    topic_id: int,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    update_data = topic_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(topic, field, value)

    db.commit()
    db.refresh(topic)

    return topic


@router.delete("/{topic_id}")
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()

    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )

    topic.is_active = False

    db.commit()

    return {
        "message": "Topic disabled",
        "topic_id": topic_id
    }


@router.post("/seed")
def seed_topics(db: Session = Depends(get_db)):
    existing_topics = db.query(Topic).count()

    if existing_topics > 0:
        return {
            "message": "Topics already exist",
            "count": existing_topics
        }

    topics = [
        Topic(
            title="Сетевой пакет",
            short_description="Базовое понятие передачи данных в компьютерной сети.",
            content=(
                "Сетевой пакет — это единица данных, которая передаётся между устройствами "
                "в компьютерной сети. В рамках игры пакет представлен как движущийся объект. "
                "Он имеет протокол, адрес источника, адрес назначения, порт и тип. "
                "Пользователь должен анализировать эти параметры и принимать решение, "
                "является ли пакет безопасным или подозрительным."
            ),
            category="Основы сетей",
            order_number=1,
            is_active=True
        ),
        Topic(
            title="Протокол TCP",
            short_description="Надёжный протокол передачи данных с установлением соединения.",
            content=(
                "TCP используется для надёжной передачи данных между устройствами. "
                "Перед обменом данными устанавливается соединение. В игре TCP-пакеты "
                "могут использоваться как обычный трафик, а также как часть атаки SYN-флуд. "
                "Пользователь должен отличать нормальные TCP-запросы от подозрительных."
            ),
            category="Протоколы",
            order_number=2,
            is_active=True
        ),
        Topic(
            title="Протокол UDP",
            short_description="Быстрый протокол передачи данных без установления соединения.",
            content=(
                "UDP передаёт данные без предварительного установления соединения. "
                "Он быстрее TCP, но не гарантирует доставку пакетов. В игре UDP используется "
                "для демонстрации обычного трафика и UDP-флуда, при котором большое количество "
                "пакетов перегружает защищаемый узел."
            ),
            category="Протоколы",
            order_number=3,
            is_active=True
        ),
        Topic(
            title="Протокол ICMP",
            short_description="Служебный протокол для диагностики сетевого взаимодействия.",
            content=(
                "ICMP применяется для передачи служебных сообщений в сети. "
                "Например, он используется командой ping для проверки доступности узла. "
                "В игре ICMP-пакеты могут быть безопасными, но при массовой отправке "
                "они превращаются в ICMP-флуд и создают угрозу доступности сервера."
            ),
            category="Протоколы",
            order_number=4,
            is_active=True
        ),
        Topic(
            title="SYN-флуд",
            short_description="Атака на механизм установления TCP-соединения.",
            content=(
                "SYN-флуд — это атака, при которой злоумышленник отправляет большое количество "
                "TCP SYN-запросов. Сервер выделяет ресурсы на обработку соединений, но они не "
                "завершаются. В игре такая атака отображается как поток вредоносных TCP-пакетов, "
                "для защиты от которых используются firewall или специальная SYN-защита."
            ),
            category="Атаки",
            order_number=5,
            is_active=True
        ),
        Topic(
            title="Firewall",
            short_description="Механизм фильтрации сетевого трафика.",
            content=(
                "Firewall, или межсетевой экран, используется для фильтрации сетевого трафика "
                "по заданным правилам. Он может блокировать пакеты по протоколу, порту или адресу. "
                "В игре firewall представлен как защитный модуль, который помогает останавливать "
                "подозрительные пакеты до того, как они достигнут сервера."
            ),
            category="Защита",
            order_number=6,
            is_active=True
        ),
        Topic(
            title="Rate Limiter",
            short_description="Ограничение частоты запросов.",
            content=(
                "Rate Limiter ограничивает количество запросов за определённый промежуток времени. "
                "Такой механизм помогает защищаться от флуда, когда на сервер отправляется слишком "
                "много однотипных пакетов. В игре этот модуль особенно полезен против ICMP-флуда "
                "и UDP-флуда."
            ),
            category="Защита",
            order_number=7,
            is_active=True
        ),
        Topic(
            title="Протокол HTTP",
            short_description="Прикладной протокол передачи веб-данных.",
            content=(
                "HTTP используется для передачи веб-страниц, API-запросов и других данных "
                "между клиентом и сервером. В игре HTTP-пакеты используются для демонстрации "
                "обычного веб-трафика и вредоносной полезной нагрузки. Для анализа такого "
                "трафика могут применяться Firewall, IDS и DPI."
            ),
            category="Протоколы",
            order_number=8,
            is_active=True
        ),
        Topic(
            title="Протокол DNS",
            short_description="Протокол преобразования доменных имён в IP-адреса.",
            content=(
                "DNS позволяет преобразовывать доменные имена в IP-адреса. Например, при обращении "
                "к сайту сначала выполняется DNS-запрос. В игре DNS-пакеты могут использоваться "
                "как обычный служебный трафик, а также как часть DNS Flood-атаки."
            ),
            category="Протоколы",
            order_number=9,
            is_active=True
        ),
        Topic(
            title="Сканирование портов",
            short_description="Метод выявления открытых портов на сервере.",
            content=(
                "Сканирование портов используется для определения доступных сетевых служб. "
                "Злоумышленник отправляет множество запросов на разные порты, чтобы найти "
                "уязвимые сервисы. В игре такая активность отображается как подозрительный "
                "TCP-трафик, против которого полезны Firewall, ACL-фильтр и IDS."
            ),
            category="Атаки",
            order_number=10,
            is_active=True
        ),
        Topic(
            title="IP Spoofing",
            short_description="Подмена IP-адреса источника сетевого пакета.",
            content=(
                "IP Spoofing — это атака, при которой злоумышленник подменяет адрес источника "
                "пакета. Это может использоваться для обхода простых фильтров или маскировки "
                "источника атаки. Для защиты применяются ACL, Firewall и системы обнаружения "
                "подозрительной активности."
            ),
            category="Атаки",
            order_number=11,
            is_active=True
        ),
        Topic(
            title="IDS",
            short_description="Система обнаружения вторжений.",
            content=(
                "IDS, или Intrusion Detection System, анализирует сетевой трафик и выявляет "
                "признаки атак. В отличие от простого фильтра, IDS может обнаруживать аномалии, "
                "сканирование портов, подмену адресов и вредоносную активность. В игре IDS "
                "эффективна против сложных и подозрительных атак."
            ),
            category="Защита",
            order_number=12,
            is_active=True
        ),
        Topic(
            title="DPI",
            short_description="Глубокий анализ содержимого сетевых пакетов.",
            content=(
                "DPI, или Deep Packet Inspection, выполняет глубокий анализ содержимого пакетов. "
                "Он позволяет обнаруживать вредоносную полезную нагрузку, подозрительные HTTP- "
                "и DNS-запросы, а также сложные атаки, которые нельзя определить только по "
                "протоколу или порту."
            ),
            category="Защита",
            order_number=13,
            is_active=True
        ),
        Topic(
            title="Malicious Payload",
            short_description="Вредоносная полезная нагрузка внутри сетевого пакета.",
            content=(
                "Malicious Payload — это вредоносные данные, передаваемые внутри сетевого пакета. "
                "Обычные фильтры могут не обнаружить такую угрозу, потому что снаружи пакет может "
                "выглядеть как нормальный HTTP-запрос. Для защиты используется глубокий анализ "
                "пакетов, IDS и DPI."
            ),
            category="Атаки",
            order_number=14,
            is_active=True
        ),
        Topic(
            title="Ботнет",
            short_description="Распределённая атака с большого количества заражённых устройств.",
            content=(
                "Ботнет — это сеть заражённых устройств, которые могут одновременно отправлять "
                "запросы к цели. Такая атака создаёт большой поток пакетов разных протоколов. "
                "Для защиты от ботнета применяются Rate Limiter, IDS, DPI и комплексная фильтрация."
            ),
            category="Атаки",
            order_number=15,
            is_active=True
        ),
    ]

    db.add_all(topics)
    db.commit()

    return {
        "message": "Topics created",
        "count": len(topics)
    }