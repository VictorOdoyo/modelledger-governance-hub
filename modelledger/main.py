import uvicorn


def main() -> None:
    uvicorn.run("modelledger.api.app:app", host="127.0.0.1", port=8088, reload=True)


if __name__ == "__main__":
    main()
