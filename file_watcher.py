import time

from watchdog.events import FileCreatedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from config_reader import get_config
from discord_handler import send_image, send_message
from image_manip import (
    add_border,
    add_border_rounded,
    is_valid_image,
    resize_image,
    save_image,
)

config = get_config()


class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileCreatedEvent) -> None:
        file_path = event.src_path
        print(f"File created: {file_path}")
        if is_valid_image(file_path):
            img = resize_image(file_path)
            img = add_border_rounded(file_path)

            filename = save_image(img)
            send_image(filename)


if __name__ == "__main__":
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(
        event_handler, config["FileWatcher"]["Directory"], recursive=False
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
