import requests as requests


class NtfyNotification:
    def __init__(self, config):
        self.client = None
        self.printer = config.get_printer()

        ntfy_host = config.get('ntfy_host', None)
        ntfy_topic = config.get('ntfy_topic', None)
        ntfy_token = config.get('ntfy_token', None)

        if ntfy_host is not None and ntfy_topic is not None:
            self.client = NtfyClient(ntfy_host, ntfy_topic, ntfy_token)
            gcode = self.printer.lookup_object('gcode')
            gcode.register_command('NTFY', self.gcode_ntfy)

    def gcode_ntfy(self, gcmd):
        msg = gcmd.get('MSG', '')
        title = gcmd.get('TITLE', None)
        if msg != '':
            gcmd.respond_info(msg)
            try:
                self.client.send(msg, title)
                gcmd.respond_info("SMS Notification Sent")

            except Exception as e:
                raise gcmd.error(e)


class NtfyClient:

    def __init__(self, host, topic, token: str = None):
        self.token = token
        if host.endswith('/'):
            self.url = host + topic
        else:
            self.url = host + "/" + topic

    def send(self, message: str, title: str = None, priority: str = None, tags: str = None):
        headers = {}
        if self.token:
            headers["Authorization"] = "Bearer {}".format(self.token)
        if title:
            headers["Title"] = title
        if priority:
            headers["Priority"] = priority
        if tags:
            headers["Tags"] = tags

        if len(headers) > 0:
            requests.post(self.url, data=message, headers=headers)
        else:
            requests.post(self.url, data=message)


def load_config(config):
    return NtfyNotification(config)
