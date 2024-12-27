import argparse
from model import engine
from loguru import logger
from sqlmodel import SQLModel

class Option:
    def create(self):
        try:
            SQLModel.metadata.create_all(bind=engine)
            logger.success("数据库创建成功")
        except Exception as e:
            logger.error(f"数据库创建失败: {e}")

    def delete(self):
        try:
            SQLModel.metadata.drop_all(bind=engine)
            logger.success("数据库删除成功")
        except Exception as e:
            logger.error(f"数据库删除失败: {e}")

if __name__ == "__main__":
    parms = argparse.ArgumentParser(usage="python db.py --type [create | delete]")
    parms.add_argument('-t', '--type', required=True, help="create | delete")
    args = parms.parse_args()
    if args.type == "create": Option().create()
    elif args.type == "delete": Option().delete()
    else: logger.error("--type 参数只有 create 和 delete")