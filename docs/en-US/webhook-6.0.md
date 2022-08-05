# Webhook (Zabbix 6.0 and higher)

In Zabbix 6.0 and higher, you have the option to use the built-in webhook media-type.

Go to the "Administration" -> "Media types" section and click "Import" to upload the media type:

![webhook-media-type-import](../../images/webhook/media-type-5.0-import.png)

Upload the [media type](../../webhook/media-type-6.0.xml) and leave the rest of the options as default.

You can change the preset message templates in the "Message templates" section by editing "notify.events (webhook)" media type.

Configure your Zabbix user according to the [instructions](user.md).
