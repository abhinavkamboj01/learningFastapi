import uvicorn

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000

    # Runs application normally
    # uvicorn.run("main:app", host=host, port=port)

    # Runs application in reload mode, tracks for python file changes
    uvicorn.run("main:app", host= host, port= port, reload=True)