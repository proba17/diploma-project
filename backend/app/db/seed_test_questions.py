from sqlalchemy.orm import Session
from app.models.final_test import TestQuestion

def seed_questions(db: Session):

    db.query(TestQuestion).delete()

    questions = [
        TestQuestion(question="На каком уровне OSI работает Router ACL?", option_a="Канальный", option_b="Сетевой", option_c="Сеансовый", option_d="Прикладной", correct_answer="b", topic="Router ACL", difficulty=1),
        TestQuestion(question="Что анализирует Router ACL?", option_a="IP-адреса и протоколы", option_b="HTML-код", option_c="Файлы", option_d="Пользователей", correct_answer="a", topic="Router ACL", difficulty=1),
        TestQuestion(question="Что такое IP Spoofing?", option_a="Шифрование трафика", option_b="Подмена IP-адреса", option_c="Сжатие данных", option_d="Балансировка нагрузки", correct_answer="b", topic="Router ACL", difficulty=1),
        TestQuestion(question="Какой адрес относится к Private IP?", option_a="8.8.8.8", option_b="1.1.1.1", option_c="192.168.1.10", option_d="91.198.174.192", correct_answer="c", topic="Router ACL", difficulty=1),
        TestQuestion(question="Какую атаку может выявлять Router ACL?", option_a="XSS", option_b="SQL Injection", option_c="IP Spoofing", option_d="Spam", correct_answer="c", topic="Router ACL", difficulty=2),

        TestQuestion(question="На каком уровне OSI работает Stateful Firewall?", option_a="Транспортный", option_b="Канальный", option_c="Физический", option_d="Прикладной", correct_answer="a", topic="Stateful Firewall", difficulty=1),
        TestQuestion(question="Что отслеживает Stateful Firewall?", option_a="Содержимое почты", option_b="Состояние соединения", option_c="Доменные имена", option_d="Пользователей", correct_answer="b", topic="Stateful Firewall", difficulty=1),
        TestQuestion(question="Какой протокол использует SYN-флаг?", option_a="UDP", option_b="ICMP", option_c="DNS", option_d="TCP", correct_answer="d", topic="Stateful Firewall", difficulty=1),
        TestQuestion(question="Что такое Port Scan?", option_a="Сканирование портов", option_b="Сканирование файлов", option_c="Шифрование", option_d="Маршрутизация", correct_answer="a", topic="Stateful Firewall", difficulty=1),
        TestQuestion(question="Какой модуль лучше всего выявляет SYN Flood?", option_a="DNS Filter", option_b="Stateful Firewall", option_c="Email Gateway", option_d="WAF", correct_answer="b", topic="Stateful Firewall", difficulty=2),

        TestQuestion(question="Для чего используется Anti-DDoS?", option_a="Фильтрация почты", option_b="Защита от массовых атак", option_c="Проверка SQL", option_d="Проверка DNS", correct_answer="b", topic="Anti-DDoS", difficulty=1),
        TestQuestion(question="Что означает DDoS?", option_a="Распределенная атака отказа в обслуживании", option_b="Система доменных имен", option_c="Тип шифрования", option_d="Тип маршрутизатора", correct_answer="a", topic="Anti-DDoS", difficulty=1),
        TestQuestion(question="Что такое UDP Flood?", option_a="Подмена IP", option_b="Фишинг", option_c="Перегрузка UDP-трафиком", option_d="XSS", correct_answer="c", topic="Anti-DDoS", difficulty=1),
        TestQuestion(question="Что такое ICMP Flood?", option_a="Перегрузка ICMP-пакетами", option_b="DNS-туннелирование", option_c="SQL Injection", option_d="Спам", correct_answer="a", topic="Anti-DDoS", difficulty=1),
        TestQuestion(question="Что такое Botnet?", option_a="Маршрутизатор", option_b="Сеть зараженных устройств", option_c="DNS-сервер", option_d="Фаервол", correct_answer="b", topic="Anti-DDoS", difficulty=2),

        TestQuestion(question="Что означает IPS?", option_a="Система предотвращения вторжений", option_b="Почтовый сервер", option_c="VPN", option_d="Коммутатор", correct_answer="a", topic="Snort IPS", difficulty=1),
        TestQuestion(question="Что такое сигнатурный анализ?", option_a="Поиск известных шаблонов атак", option_b="Шифрование", option_c="Маршрутизация", option_d="Архивация", correct_answer="a", topic="Snort IPS", difficulty=1),
        TestQuestion(question="Что такое Known Exploit?", option_a="DNS-запрос", option_b="Известный эксплойт", option_c="Легитимный пакет", option_d="Порт", correct_answer="b", topic="Snort IPS", difficulty=1),
        TestQuestion(question="Что такое Malware Traffic?", option_a="Обычный HTTP", option_b="Вредоносный трафик", option_c="DNS-запрос", option_d="SMTP-трафик", correct_answer="b", topic="Snort IPS", difficulty=1),
        TestQuestion(question="Какой модуль лучше всего блокирует известные атаки по сигнатурам?", option_a="Snort IPS", option_b="Router ACL", option_c="DNS Filter", option_d="Email Gateway", correct_answer="a", topic="Snort IPS", difficulty=2),

        TestQuestion(question="Что такое DNS?", option_a="Тип атаки", option_b="Система доменных имен", option_c="Тип коммутатора", option_d="Фильтр", correct_answer="b", topic="DNS Filter", difficulty=1),
        TestQuestion(question="Что такое DNS Tunneling?", option_a="Передача данных через DNS", option_b="SQL Injection", option_c="XSS", option_d="Port Scan", correct_answer="a", topic="DNS Filter", difficulty=1),
        TestQuestion(question="Что такое вредоносный домен?", option_a="Локальный домен", option_b="Внутренний DNS", option_c="Домен злоумышленника", option_d="Почтовый домен", correct_answer="c", topic="DNS Filter", difficulty=1),
        TestQuestion(question="Что такое C2 Domain?", option_a="DNS-сервер", option_b="Командный сервер ботнета", option_c="Прокси", option_d="SMTP", correct_answer="b", topic="DNS Filter", difficulty=2),
        TestQuestion(question="Какой модуль выявляет DNS Tunneling?", option_a="WAF", option_b="Stateful Firewall", option_c="DNS Filter", option_d="Email Gateway", correct_answer="c", topic="DNS Filter", difficulty=2),

        TestQuestion(question="Что означает WAF?", option_a="Wide Area Firewall", option_b="Web Application Firewall", option_c="Wireless Access Filter", option_d="Web Access Framework", correct_answer="b", topic="WAF", difficulty=1),
        TestQuestion(question="На каком уровне работает WAF?", option_a="Сетевой", option_b="Транспортный", option_c="Прикладной", option_d="Канальный", correct_answer="c", topic="WAF", difficulty=1),
        TestQuestion(question="Что такое SQL Injection?", option_a="Внедрение SQL-команд", option_b="Подмена DNS", option_c="Сканирование портов", option_d="DDoS", correct_answer="a", topic="WAF", difficulty=1),
        TestQuestion(question="Что такое XSS?", option_a="Подмена IP", option_b="Выполнение вредоносного JavaScript", option_c="DNS Tunnel", option_d="Спам", correct_answer="b", topic="WAF", difficulty=1),
        TestQuestion(question="Что такое Path Traversal?", option_a="Шифрование", option_b="Маршрутизация", option_c="Получение доступа к файлам через пути", option_d="Сжатие данных", correct_answer="c", topic="WAF", difficulty=1),
        TestQuestion(question="Какой модуль лучше всего защищает от SQL Injection?", option_a="DNS Filter", option_b="Email Gateway", option_c="Router ACL", option_d="WAF", correct_answer="d", topic="WAF", difficulty=2),
        TestQuestion(question="Что анализирует WAF?", option_a="HTTP-запросы", option_b="MAC-адреса", option_c="Кабели", option_d="ARP", correct_answer="a", topic="WAF", difficulty=2),

        TestQuestion(question="Что такое Email Gateway?", option_a="DNS-сервер", option_b="VPN", option_c="Шлюз защиты электронной почты", option_d="Прокси", correct_answer="c", topic="Email Gateway", difficulty=1),
        TestQuestion(question="Что такое фишинг?", option_a="Кража данных через поддельные сообщения", option_b="Маршрутизация", option_c="Шифрование", option_d="Балансировка", correct_answer="a", topic="Email Gateway", difficulty=1),
        TestQuestion(question="Что такое вредоносное вложение?", option_a="PDF", option_b="Файл с вредоносным кодом", option_c="Изображение", option_d="Документ", correct_answer="b", topic="Email Gateway", difficulty=1),
        TestQuestion(question="Что такое спам?", option_a="DNS-запрос", option_b="Нежелательная массовая рассылка", option_c="SQL-запрос", option_d="Сканирование портов", correct_answer="b", topic="Email Gateway", difficulty=1),
        TestQuestion(question="Какой модуль лучше всего защищает от фишинга?", option_a="WAF", option_b="Email Gateway", option_c="DNS Filter", option_d="ACL", correct_answer="b", topic="Email Gateway", difficulty=2),

        TestQuestion(question="Что такое ложное срабатывание?", option_a="Блокировка безопасного трафика", option_b="Пропуск атаки", option_c="DDoS", option_d="Шифрование", correct_answer="a", topic="General", difficulty=1),
        TestQuestion(question="Что такое легитимный трафик?", option_a="Спам", option_b="Ботнет", option_c="Разрешенный нормальный трафик", option_d="Атака", correct_answer="c", topic="General", difficulty=1),
        TestQuestion(question="Что такое вредоносный трафик?", option_a="Трафик связанный с атаками", option_b="Любой TCP", option_c="Любой UDP", option_d="Локальный трафик", correct_answer="a", topic="General", difficulty=1),
        TestQuestion(question="Какая цель системы защиты в игре?", option_a="Установка ОС", option_b="Обнаружение и блокировка угроз", option_c="Настройка BIOS", option_d="Монтаж оборудования", correct_answer="b", topic="General", difficulty=1),
        TestQuestion(question="Что важнее при защите сети?", option_a="Минимизировать ложные срабатывания и блокировать атаки", option_b="Блокировать весь трафик", option_c="Разрешать весь трафик", option_d="Игнорировать события", correct_answer="a", topic="General", difficulty=2),

        TestQuestion(question="Какой модуль лучше подходит для Malware Traffic?", option_a="Email Gateway", option_b="DNS Filter", option_c="Snort IPS", option_d="ACL", correct_answer="c", topic="Scenario", difficulty=3),
        TestQuestion(question="Обнаружены запросы к botnet-command.net. Что использовать?", option_a="DNS Filter", option_b="WAF", option_c="Email Gateway", option_d="ACL", correct_answer="a", topic="Scenario", difficulty=3),
        TestQuestion(question="Обнаружены тысячи SYN-пакетов. Какой модуль наиболее полезен?", option_a="DNS Filter", option_b="Stateful Firewall", option_c="Email Gateway", option_d="WAF", correct_answer="b", topic="Scenario", difficulty=3),
        TestQuestion(question="Пользователь получил письмо с invoice.exe. Какой модуль поможет?", option_a="ACL", option_b="Anti-DDoS", option_c="Email Gateway", option_d="DNS Filter", correct_answer="c", topic="Scenario", difficulty=3),
        TestQuestion(question="В URL найдено выражение OR 1=1. Что это вероятнее всего?", option_a="XSS", option_b="DNS Tunneling", option_c="Botnet", option_d="SQL Injection", correct_answer="d", topic="Scenario", difficulty=3),
        TestQuestion(question="Какой модуль лучше всего защищает веб-приложение?", option_a="WAF", option_b="ACL", option_c="Anti-DDoS", option_d="DNS Filter", correct_answer="a", topic="Scenario", difficulty=3),
        TestQuestion(question="Какой модуль анализирует состояние TCP-соединений?", option_a="DNS Filter", option_b="Email Gateway", option_c="Stateful Firewall", option_d="WAF", correct_answer="c", topic="Scenario", difficulty=3),
        TestQuestion(question="Какой модуль способен обнаруживать вредоносные сигнатуры?", option_a="Snort IPS", option_b="Router ACL", option_c="DNS Filter", option_d="Anti-DDoS", correct_answer="a", topic="Scenario", difficulty=3),
        TestQuestion(question="Какой тип атаки связан с массовой рассылкой сообщений?", option_a="XSS", option_b="Spam", option_c="Port Scan", option_d="SQL Injection", correct_answer="b", topic="Scenario", difficulty=2),
        TestQuestion(question="Что должен делать грамотный специалист ИБ?", option_a="Блокировать весь трафик", option_b="Пропускать все пакеты", option_c="Различать нормальный и вредоносный трафик", option_d="Игнорировать события", correct_answer="c", topic="General", difficulty=2),
    ]

    db.add_all(questions)
    db.commit()
