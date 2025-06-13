import time



def main():
    print("Hello from parser-service!")

    try:
        from logger.setup import setup_logging

        setup_logging()
    except ModuleNotFoundError:
        print("logger.setup not found")

    time.sleep(60*60)


if __name__ == "__main__":
    main()
