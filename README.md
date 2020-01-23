# `# IN DEVELOPING #`

# Оповещения Zabbix через Notify.Events

Вы можете получать уведомления из Zabbix в Skype, Discord, Slack, Viber, Telegram и многих других через сервис
[Notify.Events](https://notify.events).

## Zabbix 4.4 и выше

В версии Zabbix 4.4 и выше у вас есть возможность использовать встроенных механизм webhook.

## Zabbix 1.8 и выше

Расположите скрипт `notify.events.sh` в `/usr/lib/zabbix/alertscripts/`

### В разделе "Media types"

Создайте новый тип со следующими параметрами:

* Name: `Notify.Events`
* Type: `Script`
* Script name: `notify.events.sh`
* Script parameters:
    * `{ALERT.SENDTO}`
    * `{ALERT.SUBJECT}`
    * `{ALERT.MESSAGE}`

### В разделе "Actions"

Создайте экшн со следующими параметрами:

* Name: `Notify.Events`
* Default subject: `{TRIGGER.STATUS}: {TRIGGER.NAME}`
* Default message:
```json
{
    "date": "{DATE}",
    "time": "{TIME}",
    "host": "{HOST.NAME}",
    "trigger": {
        "name": "{TRIGGER.NAME}",
        "url": "{TRIGGER.URL}",
        "status": "{TRIGGER.STATUS}",
        "severity": "{TRIGGER.SEVERITY}",
    },
    "item": {
        "name": "{ITEM.NAME}",
        "value": "{ITEM.VALUE}"
    }
}
```

Для "Recovery subject/message" задайте параметры аналогично "Default subject/message".

### В разделе "User profile/Medie"
