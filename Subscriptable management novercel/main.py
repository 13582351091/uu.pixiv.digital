import uvicorn

#这个部署linux
if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)
