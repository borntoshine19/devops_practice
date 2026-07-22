Практический таск №2: «Ротация логов, Graceful Reload и Systemd Timer»
Легенда
У тебя есть Python-скрипт, который имитирует сервис, пишущий важные метрики в файл логов. Тебе нужно оформить его как полноценную службу, реализовать перегрузку конфигурации «на лету» без остановки процесса (сигнал SIGHUP) и настроить автоматическую очистку старых логов раз в минуту через Systemd Timer.

📋 Что нужно сделать (Пошаговые требования):
1. Подготовка скрипта с обработкой сигналов
Создай в /opt/appuser/app/ скрипт logger_app.py. Он должен:

Бесконечно (раз в 3 секунды) писать текущую дату и какую-то строчку в файл /var/log/my_app.log.

Уметь перехватывать сигнал SIGHUP (Signal Hangup). Когда скрипт получает этот сигнал, он должен писать в лог строчку: [INFO] Configuration reloaded!.

Python
#!/usr/bin/env python3
import time
import signal
import sys
from datetime import datetime

LOG_FILE = "/var/log/my_app.log"

def handle_sighup(signum, frame):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - [INFO] Configuration reloaded via SIGHUP!\n")

# Регистрируем обработчик сигнала SIGHUP
signal.signal(signal.SIGHUP, handle_sighup)

while True:
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - [INFO] App is working normally...\n")
    time.sleep(3)
Не забудь дать право пользователю appuser писать в файл /var/log/my_app.log (или создай файл заранее и сделай chown appuser:appuser /var/log/my_app.log).

2. Настройка Graceful Reload в systemd
Создай юнит /etc/systemd/system/metrics-logger.service от имени appuser.

Добавь в секцию [Service] директиву:
ExecReload=/bin/kill -HUP $MAINPID
(Это позволит выполнять команду systemctl reload metrics-logger.service без полного перезапуска и сброса PID!).

3. Создание Systemd Timer (Замена cron)
В Linux вместо устаревшего cron всё чаще используют связку Service + Timer в systemd.
Тебе нужно настроить очистку файла логов /var/log/my_app.log каждую 1 минуту.

Создай сервис очистки /etc/systemd/system/log-cleaner.service:

Тип: Type=oneshot (запустился, выполнил одно действие и сразу завершился).

Команда: ExecStart=/usr/bin/truncate -s 0 /var/log/my_app.log (команда truncate -s 0 мгновенно очищает файл, не удаляя его).

Создай таймер /etc/systemd/system/log-cleaner.timer:

В секции [Timer] укажи запуск каждую минуту: OnCalendar=*:0/1

В секции [Install] укажи WantedBy=timers.target

Запусти и включи таймер: sudo systemctl enable --now log-cleaner.timer.

🧪 Приемочные тесты (Как проверить себя):
Проверка Reload:

Запусти metrics-logger.service.

Выполни sudo systemctl reload metrics-logger.service.

Посмотри лог cat /var/log/my_app.log. В нем должна появиться строчка [INFO] Configuration reloaded via SIGHUP!, при этом PID процесса не должен измениться!

Проверка Таймера:

Посмотри список активных таймеров командой systemctl list-timers. Найди там свой log-cleaner.timer.

Подожди минуту и проверь файл my_app.log — он должен очищаться и начинаться заново.

Жду вопросов, если что-то непонятно, или результатов выполнения!Практический таск №2: «Ротация логов, Graceful Reload и Systemd Timer»
Легенда
У тебя есть Python-скрипт, который имитирует сервис, пишущий важные метрики в файл логов. Тебе нужно оформить его как полноценную службу, реализовать перегрузку конфигурации «на лету» без остановки процесса (сигнал SIGHUP) и настроить автоматическую очистку старых логов раз в минуту через Systemd Timer.

📋 Что нужно сделать (Пошаговые требования):
1. Подготовка скрипта с обработкой сигналов
Создай в /opt/appuser/app/ скрипт logger_app.py. Он должен:

Бесконечно (раз в 3 секунды) писать текущую дату и какую-то строчку в файл /var/log/my_app.log.

Уметь перехватывать сигнал SIGHUP (Signal Hangup). Когда скрипт получает этот сигнал, он должен писать в лог строчку: [INFO] Configuration reloaded!.

Python
#!/usr/bin/env python3
import time
import signal
import sys
from datetime import datetime

LOG_FILE = "/var/log/my_app.log"

def handle_sighup(signum, frame):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - [INFO] Configuration reloaded via SIGHUP!\n")

# Регистрируем обработчик сигнала SIGHUP
signal.signal(signal.SIGHUP, handle_sighup)

while True:
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - [INFO] App is working normally...\n")
    time.sleep(3)
Не забудь дать право пользователю appuser писать в файл /var/log/my_app.log (или создай файл заранее и сделай chown appuser:appuser /var/log/my_app.log).

2. Настройка Graceful Reload в systemd
Создай юнит /etc/systemd/system/metrics-logger.service от имени appuser.

Добавь в секцию [Service] директиву:
ExecReload=/bin/kill -HUP $MAINPID
(Это позволит выполнять команду systemctl reload metrics-logger.service без полного перезапуска и сброса PID!).

3. Создание Systemd Timer (Замена cron)
В Linux вместо устаревшего cron всё чаще используют связку Service + Timer в systemd.
Тебе нужно настроить очистку файла логов /var/log/my_app.log каждую 1 минуту.

Создай сервис очистки /etc/systemd/system/log-cleaner.service:

Тип: Type=oneshot (запустился, выполнил одно действие и сразу завершился).

Команда: ExecStart=/usr/bin/truncate -s 0 /var/log/my_app.log (команда truncate -s 0 мгновенно очищает файл, не удаляя его).

Создай таймер /etc/systemd/system/log-cleaner.timer:

В секции [Timer] укажи запуск каждую минуту: OnCalendar=*:0/1

В секции [Install] укажи WantedBy=timers.target

Запусти и включи таймер: sudo systemctl enable --now log-cleaner.timer.

🧪 Приемочные тесты (Как проверить себя):
Проверка Reload:

Запусти metrics-logger.service.

Выполни sudo systemctl reload metrics-logger.service.

Посмотри лог cat /var/log/my_app.log. В нем должна появиться строчка [INFO] Configuration reloaded via SIGHUP!, при этом PID процесса не должен измениться!

Проверка Таймера:

Посмотри список активных таймеров командой systemctl list-timers. Найди там свой log-cleaner.timer.

Подожди минуту и проверь файл my_app.log — он должен очищаться и начинаться заново.

Жду вопросов, если что-то непонятно, или результатов выполнения!
