import os
import shutil
import pandas as pd


BASE_PATH = '原始文档\\文档自动归类'
INPUT_PATH = '原始文档\\文档自动归类\\input'
OUTPUT_PATH = '原始文档\\文档自动归类\\output'

def doc_packing(base_path, input_path, output_path):

    wanglei_folder = '王磊'
    zhangliren_folder = '张立人'
    wanglei_path = os.path.join(output_path, wanglei_folder)
    zhangliren_path = os.path.join(output_path, zhangliren_folder)

    df = pd.read_excel(os.path.join(input_path, 'info.xlsx'))

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    if not os.path.exists(wanglei_path):
        os.mkdir(wanglei_path)
        os.mkdir(os.path.join(wanglei_path, '文档包'))

    if not os.path.exists(zhangliren_path):
        os.mkdir(zhangliren_path)
        os.mkdir(os.path.join(zhangliren_path, '文档包'))

    # 获取input folder的文档包名列表
    doc_pack_folder = os.listdir(os.path.join(input_path, '文档包'))[0]
    doc_pack_list = os.listdir(os.path.join(input_path, '文档包', doc_pack_folder))
    doc_pack_path_list = [os.path.join(input_path, '文档包', doc_pack_folder, doc_pack) for doc_pack in doc_pack_list]

    # 把文档分配到律师个人文件夹，文档包名添加用户姓名
    for doc_pack, doc_pack_path in zip(doc_pack_list, doc_pack_path_list):
        if df[df['合同号']==doc_pack]['承办律师'].tolist()[0] == '王磊':
            try:
                shutil.copytree(
                    doc_pack_path, 
                    os.path.join(wanglei_path, '文档包', doc_pack_folder, doc_pack + '_' + df[df['合同号']==doc_pack]['用户姓名'].tolist()[0])
                    )
            except Exception as e:
                print(f'复制文件夹时出错：{e}')
        elif df[df['合同号']==doc_pack]['承办律师'].tolist()[0] == '张立人':
            try:
                shutil.copytree(
                    doc_pack_path, 
                    os.path.join(zhangliren_path, '文档包', doc_pack_folder, doc_pack + '_' + df[df['合同号']==doc_pack]['用户姓名'].tolist()[0])
                    )
            except Exception as e:
                print(f'复制文件夹时出错：{e}')
        else:
            print('律师匹配错误')
    
    result = '文档包已分配到律师，文档包名已添加用户姓名。'

    # 获取input folder的身份证列表
    id_folder = '身份证'
    id_list = [id for id in os.listdir(os.path.join(input_path, id_folder)) if '.jpg' in id]
    id_path_list = [os.path.join(input_path, id_folder, id) for id in id_list]

    id_docx_folder = '身份证_docx'
    id_docx_list = [id for id in os.listdir(os.path.join(input_path, id_docx_folder)) if '.docx' in id]
    id_docx_path_list = [os.path.join(input_path, id_docx_folder, id) for id in id_docx_list]

    # 复制身份证图片到对应律师的文档包
    for id_file_name, id_path in zip(id_list, id_path_list):
        username = id_file_name.split('_')[0]
        case_folder = df[(df['用户名']==username) & (df['是否可诉']=='诉讼')]['合同号'].tolist()[0] + '_' + df[df['用户名']==username]['用户姓名'].tolist()[0]
        if df[df['用户名']==username]['承办律师'].tolist()[0] == '王磊':
            shutil.copy(id_path, os.path.join(
                wanglei_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                id_file_name
                ))
        elif df[df['用户名']==username]['承办律师'].tolist()[0] == '张立人':
            shutil.copy(id_path, os.path.join(
                zhangliren_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                id_file_name
                ))
        else:
            print('律师匹配错误')

    result += '\n\n身份证图片已添加到文档包。'

    # 复制身份证 Word 到对应律师的文档包
    for id_docx, id_docx_path in zip(id_docx_list, id_docx_path_list):
        username = id_docx.split('_')[0]
        case_folder = df[(df['用户名']==username) & (df['是否可诉']=='诉讼')]['合同号'].tolist()[0] + '_' + df[df['用户名']==username]['用户姓名'].tolist()[0]
        if df[df['用户名']==username]['承办律师'].tolist()[0] == '王磊':
            shutil.copy(id_docx_path, os.path.join(
                wanglei_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                id_docx
                ))
        elif df[df['用户名']==username]['承办律师'].tolist()[0] == '张立人':
            shutil.copy(id_docx_path, os.path.join(
                zhangliren_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                id_docx
                ))
        else:
            print('律师匹配错误')

    result += '\n\n身份证正反面Word已添加到文档包。'

    # 获取input folder的起诉状和委托书列表
    qsz_wts_folder = '起诉状和委托书_已盖章'
    qsz_wts_folder_list = os.listdir(os.path.join(input_path, qsz_wts_folder))
    qsz_wts_folder_path_list = [os.path.join(input_path, qsz_wts_folder, sub_folder) for sub_folder in qsz_wts_folder_list]

    qsz_wts_file_folder_list = []
    qsz_wts_file_path_list = []
    
    # 复制起诉状和委托书到对应律师的文档包
    for qsz_wts_folder_path in qsz_wts_folder_path_list:
        for qsz_wts_file_name in os.listdir(qsz_wts_folder_path):
            qsz_wts_file_folder_list.append(qsz_wts_file_name)
            qsz_wts_file_path_list.append(os.path.join(qsz_wts_folder_path, qsz_wts_file_name))

    for file_name, file_path in zip(qsz_wts_file_folder_list, qsz_wts_file_path_list):
        contract_id = file_name.split('_')[1]
        case_folder = contract_id + '_' + df[df['合同号']==contract_id]['用户姓名'].tolist()[0]

        # 判断是哪个律师
        if df[df['合同号']==contract_id]['承办律师'].tolist()[0] == '王磊':
            shutil.copy(file_path, os.path.join(
                wanglei_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                file_name
                ))
        elif df[df['合同号']==contract_id]['承办律师'].tolist()[0] == '张立人':
            shutil.copy(file_path, os.path.join(
                zhangliren_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                file_name
                ))
        else:
            print('律师匹配错误')

    result += '\n\n起诉状和委托书已添加到文档包。'

    evidence_folder = '凭证'
    evidence_list = [evi for evi in os.listdir(os.path.join(input_path, evidence_folder)) if '.pdf' in evi]
    evidence_path_list = [os.path.join(input_path, evidence_folder, evi) for evi in evidence_list]

    # 复制身份证图片到对应律师的文档包
    for evi_file_name, evi_path in zip(evidence_list, evidence_path_list):
        list_id = int(evi_file_name.split('-')[0])
        case_folder = df[(df['列表ID']==list_id)]['合同号'].tolist()[0] + '_' + df[df['列表ID']==list_id]['用户姓名'].tolist()[0]
        if df[df['列表ID']==list_id]['承办律师'].tolist()[0] == '王磊':
            shutil.copy(evi_path, os.path.join(
                wanglei_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                evi_file_name
                ))
        elif df[df['列表ID']==list_id]['承办律师'].tolist()[0] == '张立人':
            shutil.copy(evi_path, os.path.join(
                zhangliren_path, 
                '文档包', 
                doc_pack_folder, 
                case_folder, 
                evi_file_name
                ))
        else:
            print('律师匹配错误')

    result += '\n\n凭证已添加到文档包。'

    return result

if __name__ == '__main__':
    doc_packing(
        base_path=BASE_PATH,
        input_path=INPUT_PATH, 
        output_path=OUTPUT_PATH
    )