# Zabbix user configuration

Create a new channel and add the source "Zabbix" in [Notify.Events](https://notify.events):

![notify-events-token](../../images/notify-events-token.png)

After that, go to Zabbix user settings and add new media. In the "Type" field, select the media-type that you created
and specify the token you get on the previous step in the "Send to" field:

![user](../../images/user.png)

Now you can use Notify.Events to get notifications to the messengers you choose.

To test sending notifications from Zabbix to Notify.Events, you can open the media type testing dialog
in the section "Administration" -> "Media types" -> "notify.events (webhook)" and specify the received token in the "To" field.

![test](../../images/test.png)

Also make sure you've enabled the default "Report problems to Zabbix administrators" action or make your own rule (Configurations -> Actions -> Trigger Actions). More information about Notifications and Actions you can find [here](https://www.zabbix.com/documentation/current/manual/config/notifications).
