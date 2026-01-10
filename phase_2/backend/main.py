def main():
    print("Hello from backend!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8001, reload=True)
