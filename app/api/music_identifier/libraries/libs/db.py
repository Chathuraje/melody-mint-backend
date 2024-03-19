from app.utils import config
import pymysql
from app.utils.logging import get_logger

logger = get_logger()  

def get_conn():
    conn = pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_DB
    )
    
    logger.info("Connected to database")

    return [conn, conn.cursor()]
