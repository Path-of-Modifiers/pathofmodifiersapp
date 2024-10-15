import datetime as dt
import json
import logging

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "hostname",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
    "remote_addr",
    "method",
    "url",
    "status_code",
}


class JSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO


class APIMessageFormatter(JSONFormatter):
    def format(self, record: logging.LogRecord) -> str:
        access_log_map = {
            "h": 0,  # remote address
            "m": 1,  # request method
            "U": 2,  # URL path
            "s": 4,  # status code (correct index for status code)
        }

        # Create a dictionary to hold the values
        log_values = {
            "logger": record.name,  # Adding logger (name)
            "level": record.levelname,  # Adding level (levelname)
            "remote_addr": record.args[access_log_map["h"]],
            "method": record.args[access_log_map["m"]],
            "url": record.args[access_log_map["U"]],
            "status_code": record.args[access_log_map["s"]],
        }

        # Set up the fmt_keys for the JSONFormatter
        self.fmt_keys = {key: key for key in log_values}  # Use keys as fmt_keys

        # Update the record's attributes with log values
        for key, value in log_values.items():
            setattr(record, key, value)

        # Call the parent format method to generate the JSON output
        message = super().format(record)

        # Remove the "message" field from the output
        message_dict = json.loads(message)
        message_dict.pop("message", None)  # Remove "message" if it exists

        return json.dumps(message_dict, default=str)
