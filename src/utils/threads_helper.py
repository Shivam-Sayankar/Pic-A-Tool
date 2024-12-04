from threading import Thread

def threaded_task(task_function, *args, **kwargs):

    task_thread = Thread(
        target=task_function,
        args=args,
        kwargs=kwargs,
        daemon=True
    )

    task_thread.start()
