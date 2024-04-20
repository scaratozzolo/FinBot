import uvicorn

if __name__ == '__main__':

    uvicorn.run(
        "src.app:app",
        reload=True,
        workers=10,
        host="0.0.0.0",
        port=5000,
    )