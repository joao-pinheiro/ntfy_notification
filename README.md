ntfy-notification
==============


[ntfy](https://ntfy.sh/) notifications for klipper


## config vars

|parameter|description|
|---|---|
|ntfy_host| ntfy url|
|ntfy_topic| ntfy topic to publish to|
|ntfy_token| optional bearer token|


## Installation

install via shell on an existing klipper installation:

```shell
cd ~
git clone https://github.com/joao-pinheiro/ntfy_notification.git
cd ntfy_notification
./install.sh

```

Add the following section to the config file:

```ini
[ntfy_notification]
ntfy_host = https://ntfy.sh/    # or your own server
ntfy_topic = my_hard_to_guess_topic # custom topic
#ntfy_token = <token> # optional bearer token 

```

**Optional** Add the contents of templates/moonraker-update.txt to the existing mooonraker.conf file.

## Usage
Add GCode ntfy msg="message to send" [title="optional title"] to the event you want to be notifed.

Example on how to send a message on cancel:
```shell
[gcode_macro CANCEL_PRINT]
description: Cancel the actual running print
rename_existing: CANCEL_PRINT_BASE
variable_park: True
gcode:
  ## Move head and retract only if not already in the pause state and park set to true
  {% if printer.pause_resume.is_paused|lower == 'false' and park|lower == 'true'%}
    TOOLHEAD_PARK_PAUSE_CANCEL
  {% endif %}
  TURN_OFF_HEATERS
  M106 S0
  CANCEL_PRINT_BASE
  ntfy msg="print job  {printer.print_stats.filename} cancelled"
```