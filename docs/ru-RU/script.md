# Shell script (Zabbix 3.0 и выше)

Расположите скрипт [notify.events.sh](../../script/notify.events.sh) в директории соответствующей `AlertScriptPath`,
указанному в файле конфигурации Zabbix (например `/usr/lib/zabbix/alertscripts/`)

Установите права на исполнение данному скрипту:
```shell script
chmod +x notify.events.sh
```

Создайте media-type, для этого перейдите в раздел "Administration" -> "Media types" и добавьте
следующие параметры:

```text
Type:
    Script

Script name:
    notify.events.sh

Script parameters:
    {ALERT.SENDTO}
    {ALERT.SUBJECT}
    {ALERT.MESSAGE}
    {TRIGGER.NSEVERITY}
    {TRIGGER.STATUS}
```

как на примере ниже:

![script-media-type-create](../../images/script/media-type-create.png)

Для версии Zabbix 4.4 и выше вы можете импортировать [media-type](../../script/media-type.xml).

Настройте вашего пользователя Zabbix согласно [инструкции](user.md).
