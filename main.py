import uvicorn

def main():
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=1998, 
        log_config=None, 
        reload=True, 
    )
    
if __name__ == "__main__":
    main()