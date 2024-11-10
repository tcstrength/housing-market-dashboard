

def my_failure_callback_function(context):
    from common.telegram_api import send_message
    message = f"""Task has failed: 
```
dag_id: {context['task'].dag_id}
task_id: {context['task'].task_id}
```
"""
    send_message(message=message)

tz_string = "Asia/Ho_Chi_Minh"

default_args = {
    "on_failure_callback": my_failure_callback_function,
}
