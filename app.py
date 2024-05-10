import streamlit as st
import os
import shutil
import zipfile

from package.doc_process import doc_process
from package.doc_packing_v2 import doc_packing
from package.zip_process import zip_extract_all, compress_directory


with st.sidebar:
    program = st.selectbox('选择你需要的服务：', (
        '1. 起诉状 & 委托书 - 自动编辑',
        '2. 文档自动归类'
    ))

    # if program == '1. 起诉状 & 委托书 - 自动编辑':
    #     with open('resource/README_1.md', 'r') as f:
    #         readme = f.read()

    #     st.markdown(readme.split('[img]')[0])
    #     st.image('resource/docs_format.jpg')
    #     st.markdown(readme.split('[img]')[1])

    # elif program == '2. 文档自动归类':
    #     with open('resource/README_2.md', 'r') as f:
    #         readme = f.read()

    #     st.markdown(readme.split('[img]')[0])
    #     st.image('resource/docs_format_2.jpg')
    #     st.markdown(readme.split('[img]')[1])

if program == '1. 起诉状 & 委托书 - 自动编辑':

    extract_folder = '起诉状和委托书'
    output_folder = compressed_file_name = "output_起诉状和委托书"
    input_folder = None

    try:
        shutil.rmtree(extract_folder)
    except Exception as e:
        # st.write(f"删除文件夹 {extract_folder} 时发生错误：{str(e)}")
        pass
    
    try:
        os.remove(f"{compressed_file_name}.zip")
    except Exception as e:
        # st.write(f"删除文件 f'{compressed_file_name}.zip' 时发生错误：{str(e)}")
        pass

    st.header('1. 起诉状 & 委托书 - 自动编辑')

    # 添加一个文件上传组件
    uploaded_file_1 = st.file_uploader("选择要上传的文件", type=["zip"])

    # 如果有文件上传
    if uploaded_file_1:
        # 保存上传的ZIP文件到本地临时目录
        with open("temp_1.zip", "wb") as f:
            f.write(uploaded_file_1.read())

        # 创建文档目录
        os.makedirs(extract_folder, exist_ok=True)

        # 解压ZIP文件中的文件并处理文件名和内容
        with zipfile.ZipFile("temp_1.zip", "r") as file:
            # for file_or_path in file.namelist():
            #     print(file_or_path, ' -------> ' , recode(file_or_path))
            zip_extract_all(file, extract_folder)

        # 显示解压缩完成的消息
        st.success(f"ZIP文件已成功解压缩到目录 {extract_folder}")
        input_folder = os.listdir(extract_folder)[0] if 'output' not in os.listdir(extract_folder)[0] else os.listdir(extract_folder)[1]

        # 删除临时文件
        os.remove("temp_1.zip")

    if st.button('自动处理并生成ZIP文件'):
        if input_folder:
            input_path = os.path.join(extract_folder, input_folder)
            output_path = os.path.join(extract_folder, output_folder)
            result = doc_process(input_path, output_path)
        else:
            result = '请先上传ZIP文件'
        st.write(result)

        if input_folder:
            # 在Streamlit中压缩目录
            if compress_directory(os.path.join(extract_folder, output_folder), compressed_file_name):
                st.success("导出目录已成功压缩为ZIP文件")

                # 创建下载链接
                with open(f"{compressed_file_name}.zip", "rb") as file:
                    st.download_button("点击此处下载ZIP文件", file.read(), f"{compressed_file_name}.zip")
            else:
                st.error("目录压缩失败。")

    # if st.button('清空输出文档', type='primary'):
    #     try:
    #         shutil.rmtree(extract_folder)
    #     except Exception as e:
    #         # st.write(f"删除文件夹 {extract_folder} 时发生错误：{str(e)}")
    #         pass
        
    #     try:
    #         os.remove(f"{compressed_file_name}.zip")
    #     except Exception as e:
    #         # st.write(f"删除文件 f'{compressed_file_name}.zip' 时发生错误：{str(e)}")
    #         pass

    #     if extract_folder not in os.listdir() and f"{compressed_file_name}.zip" not in os.listdir():
    #         st.markdown('所有输出文档已清空')

    # if extract_folder in os.listdir() or f"{compressed_file_name}.zip" in os.listdir():
    #     st.markdown(':red[完成任务后请点击“清空输出文档”]')   


if program == '2. 文档自动归类':

    extract_folder = '文档自动归类'
    output_folder = compressed_file_name = "output_文档自动归类"
    input_folder = None

    try:
        shutil.rmtree(extract_folder)
    except Exception as e:
        # st.write(f"删除文件夹 {extract_folder} 时发生错误：{str(e)}")
        pass
    
    try:
        os.remove(f"{compressed_file_name}.zip")
    except Exception as e:
        # st.write(f"删除文件 f'{compressed_file_name}.zip' 时发生错误：{str(e)}")
        pass
    
    st.header('2. 文档自动归类')

    # 添加一个文件上传组件
    uploaded_file_2 = st.file_uploader("选择要上传的文件", type=["zip"])

    # 如果有文件上传
    if uploaded_file_2:
        # 保存上传的ZIP文件到本地临时目录
        with open("temp_2.zip", "wb") as f:
            f.write(uploaded_file_2.read())

        # 创建文档目录
        os.makedirs(extract_folder, exist_ok=True)

        # 解压ZIP文件中的文件并处理文件名和内容
        with zipfile.ZipFile("temp_2.zip", "r") as file:
            # for file_or_path in file.namelist():
            #     print(file_or_path, ' -------> ' , recode(file_or_path))
            zip_extract_all(file, extract_folder)

        # 显示解压缩完成的消息
        st.success(f"ZIP文件已成功解压缩到目录 {extract_folder}")
        input_folder = os.listdir(extract_folder)[0] if 'output' not in os.listdir(extract_folder)[0] else os.listdir(extract_folder)[1]

        # 删除临时文件
        os.remove("temp_2.zip")

    if st.button('自动处理并生成ZIP文件'):
        if input_folder:
            extract_path = os.path.join(os.getcwd(), extract_folder)
            input_path = os.path.join(extract_path, input_folder)
            output_path = os.path.join(extract_path, output_folder)
            result = doc_packing(
                base_path=extract_path,
                input_path=input_path, 
                output_path=output_path
            )
        else:
            result = '请先上传ZIP文件'
        st.write(result)

        if input_folder:
            # 在Streamlit中压缩目录
            if compress_directory(os.path.join(extract_folder, output_folder), compressed_file_name):
                st.success("导出目录已成功压缩为ZIP文件")

                # 创建下载链接
                with open(f"{compressed_file_name}.zip", "rb") as file:
                    st.download_button("点击此处下载ZIP文件", file.read(), f"{compressed_file_name}.zip")
            else:
                st.error("目录压缩失败。")

    # if st.button('清空输出文档', type='primary'):
    #     try:
    #         shutil.rmtree(extract_folder)
    #     except Exception as e:
    #         # st.write(f"删除文件夹 {extract_folder} 时发生错误：{str(e)}")
    #         pass
        
    #     try:
    #         os.remove(f"{compressed_file_name}.zip")
    #     except Exception as e:
    #         # st.write(f"删除文件 f'{compressed_file_name}.zip' 时发生错误：{str(e)}")
    #         pass

    #     if extract_folder not in os.listdir() and f"{compressed_file_name}.zip" not in os.listdir():
    #         st.markdown('所有输出文档已清空')

    # if extract_folder in os.listdir() or f"{compressed_file_name}.zip" in os.listdir():
    #     st.markdown(':red[完成任务后请点击“清空输出文档”]')  