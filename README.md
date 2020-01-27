# Zabbix notifications in Skype, Telegram, Viber, ...

You can get notifications from Zabbix to [supported messengers](https://notify.events/en-US/features) using the [Notify.Events](https://notify.events) service.

#### Instruction on another languages

- [Русский](docs/ru-RU.md)

---

## Zabbix 4.4 and higher

In version Zabbix 4.4 and higher, you have the option to use the built-in webhook media-type.


Go to the "Administration" -> "Media types" section and click "Import" to upload media-type
for Zabbix 4.4 and higher:

![media-type](docs/images/media-type.png)

Upload [media-type](webhook/media-type.xml) and leave the rest default options:

![media-type-import](docs/images/media-type-import.png)

Create a new channel and add the source "Zabbix" in Notify.Events:

![media-type-token](docs/images/media-type-token.png)

After that, go to the edit page of the imported media-type in Zabbix and specify the token you
get on the previous step:

![media-type-webhook-config](docs/images/media-type-webhook-config.png)

Now you can use this media-type to get notifications to the messengers you choose.

---

## Zabbix 3.0 and higher

Go to the "Administration" -> "Media types" section and click "Import" to upload media-type
for Zabbix 3.0 and higher:

![media-type](docs/images/media-type.png)

Upload [media-type](script/media-type.xml) and leave the rest default options:

![media-type-import](docs/images/media-type-import.png)

Create a new channel and add the source "Zabbix" in Notify.Events:

![media-type-token](docs/images/media-type-token.png)

After that, go to the edit page of the imported media-type in Zabbix and specify the token you get on the previous step:

![media-type-webhook-config](docs/images/media-type-script-config.png)

Place the [notify.events.sh](script/notify.events.sh) script to the `AlertScriptPath` directory specified
in the Zabbix configuration file (for example `/usr/lib/zabbix/alertscripts/`)

Set the execute permission to this script:
`chmod +x notify.events.sh`

Now you can use this media-type to get notifications to the messengers you choose.
