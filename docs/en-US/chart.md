# Python script with charts support (Zabbix 3.x and 4.x)

> Experimental functionality

> Unfortunately, we did not have the opportunity to fully test the functionality. We would really appreciate if you
> shared screenshots of how the charts look :) support@notify.events

You need the installed python3 and python3-pip packages for the script to work.

Place the [notify.events.py](../../chart/notify.events.py) python-script,
[notify.events.json](../../chart/notify.events.json) configuration file and
[requirements.txt](../../chart/requirements.txt) to the `AlertScriptPath` directory specified
in the Zabbix configuration file (for example `/usr/lib/zabbix/alertscripts/`)

Create a python virtual environment in the script directory according to the [instructions](https://docs.python.org/3/library/venv.html).

Install the necessary dependencies:
```shell script
pip install -r requirements.txt
```

Set the execute permission to this script:
```shell script
chmod +x notify.events.py
```

Edit the notify.events.json configuration file according to your options:
```json
{
  "zabbix": {
    "host": "http://localhost/",    - zabbix-server address
    "user": "Admin",                - user name (trigger, item and chart permissions are required) 
    "password": "zabbix"            - password
  },
  "chart": {
    "period": 10800,                - chart period (sec)
    "width": 500,                   - chart width (px)
    "height": 250                   - chart height (px)
  }
}
```

Go to the "Administration" -> "Media types" section and add the following parameters to create a media-type:

```text
Type:
    Script

Script name:
    notify.events.py

Script parameters:
    {ALERT.SENDTO}
    {ALERT.SUBJECT}
    {ALERT.MESSAGE}
    {TRIGGER.ID}
```

as you can see below:

![script-media-type-create](../../images/chart/media-type-create.png)

If you have Zabbix 4.4 and higher you can upload [media-type](../../chart/media-type.xml) using import.

Configure your Zabbix user according to the [instructions](user.md).
