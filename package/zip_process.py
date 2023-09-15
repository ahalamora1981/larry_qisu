import os
import shutil
from zipfile import ZipFile


# 压缩目录到zip文件
def compress_directory(directory_path, output_zip):
    try:
        shutil.make_archive(output_zip, 'zip', directory_path)
        return True
    except Exception as e:
        return str(e)

def recode(raw: str) -> str:
    '''
    编码修正
    '''
    
    try:
        return raw.encode('cp437').decode('utf-8')
    
    except:
        return raw.encode('utf-8').decode('utf-8')

def zip_extract_all(src_zip_file: ZipFile, target_path: str) -> None:

    # 遍历压缩包内所有内容，创建所有目录
    for file_or_path in src_zip_file.namelist():
        
        # 若当前节点是文件夹
        if file_or_path.endswith('/'):
            try:
                # 基于当前文件夹节点创建多层文件夹
                os.makedirs(os.path.join(target_path, recode(file_or_path)))
            except FileExistsError:
                # 若已存在则跳过创建过程
                pass
        
        # 否则视作文件进行写出
        else:
            pass

    # 遍历压缩包内所有内容，解压文件
    for file_or_path in src_zip_file.namelist():
        
        # 若当前节点是文件夹
        if file_or_path.endswith('/'):
            pass
        
        # 否则视作文件进行写出
        else:
            # 利用shutil.copyfileobj，从压缩包io流中提取目标文件内容写出到目标路径
            with open(os.path.join(target_path, recode(file_or_path)), 'wb') as z:
                # 这里基于Zipfile.open()提取文件内容时需要使用原始的乱码文件名
                shutil.copyfileobj(src_zip_file.open(file_or_path), z)