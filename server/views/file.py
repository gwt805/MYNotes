import io, json
from uuid import uuid1
from minio import Minio
from robyn import SubRouter, Request

api_file = SubRouter(__name__, prefix="/api/file")


client = Minio(endpoint="127.0.0.1:9000", access_key='minioadmin', secret_key="minioadmin", secure=False)

async def upload_file(filename: str, file, size):
    if not client.bucket_exists("blog"):
        client.make_bucket(bucket_name="blog")
    client.put_object(bucket_name="blog", object_name=filename, data=file, length=size)

async def remove_file(filename):
    client.remove_object("blog", filename)


@api_file.post("/uploadimg", openapi_name="上传图片")
async def uploadimg(request: Request) -> dict:
    try:
        files = request.files
        uid = str(uuid1())
        file = next(iter(files))
        file_name = file
        file_data = files[file]
        file_size = len(file_data)
        filenew = io.BytesIO(file_data)
        await upload_file(f"{uid}-{file_name}", filenew, file_size)
        return {'errno': 0,  'data': {'url': f"http://127.0.0.1:9000/blog/{uid}-{file_name}", "alt": f"{uid}-{file_name}"}}
    except Exception as e:
        return {'errno': 1,  'message': "上传失败"}

@api_file.post("/delete", openapi_name="删除文件")
async def remove(request: Request) -> dict:
    body = json.loads(request.body)
    remove_file(body['filename'])
    return {'code': 0, 'status': 'success', 'msg': '删除成功'}

@api_file.post("/uploadfile", openapi_name="上传视频")
async def uploadvideo(request: Request) -> dict:
    try:
        files = request.files
        uid = str(uuid1())
        file = next(iter(files))
        file_name = file
        file_data = files[file]
        file_size = len(file_data)
        filenew = io.BytesIO(file_data)
        await upload_file(f"{uid}-{file_name}", filenew, file_size)
        return {'errno': 0,  'data': {'url': f"http://127.0.0.1:9000/blog/{uid}-{file_name}"}}
    except Exception as e:
        return {'errno': 1,  'message': "上传失败"}