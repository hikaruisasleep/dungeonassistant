from bot import create_bot

if __name__ == "__main__":
    create_bot().run(asyncio_debug=True,coroutine_tracking_depth=20)