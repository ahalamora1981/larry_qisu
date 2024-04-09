import os
import shutil
import pandas as pd

# 设定输入目录和输出目录
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

# 设定BASE目录路径，输入目录路径，输出目录路径
BASE_PATH = os.path.join(os.getcwd(), 'Documents', '2023', '10', '文档自动归类')
INPUT_PATH = os.path.join(BASE_PATH, INPUT_FOLDER)
OUTPUT_PATH = os.path.join(BASE_PATH, OUTPUT_FOLDER)

# 设定表格文件名，律师人名
EXCEL_FILE = 'info.xlsx'
LAWYER_LIST = ['王磊', '张立人', '杨青']

# 设定融担公司
RONGDAN_LIST = [
    '福建智云',
    '海南申信',
    '上海耳序'
]

# 合同号与律师对应关系
contract_to_lawyer = {}

# 证据文档列表
EVIDENCE_LIST = [
    '贷款合同',
    '个人委托担保协议',
    '不可撤销担保函',
    '借款服务协议',
    '债权转让协议'
]

def doc_packing(base_path, input_path, output_path):
    # 读取表格到 Pandas Dataframe
    df = pd.read_excel(os.path.join(input_path, EXCEL_FILE))

    # 创建输出目录
    if OUTPUT_FOLDER not in os.listdir(base_path):
        os.mkdir(output_path)

    # 创建律师目录
    for lawyer in LAWYER_LIST:
        if lawyer not in os.listdir(output_path):
            os.mkdir(os.path.join(output_path, lawyer))

    # 创建每个案件的目录
    for idx, row in enumerate(df[df['是否可诉']=='诉讼'].iterrows()):

        idx = '0' + str(idx + 1) if len(str(idx + 1)) == 1 else str(idx + 1)
        row = row[1]

        for rongdan in RONGDAN_LIST:
            if rongdan in row['融担公司']:
                break

        person = row['用户姓名']

        court = row['管辖法院'].strip('人民法院')

        contract_id = row['合同号']

        contract_to_lawyer[contract_id] = row['承办律师']

        case_folder = f'{idx}{rongdan}_{person} {court}-{contract_id}'
        
        if case_folder not in os.listdir(os.path.join(output_path, row['承办律师'])):
            os.mkdir(os.path.join(output_path, row['承办律师'], case_folder))

        if '委托材料' not in os.listdir(os.path.join(output_path, row['承办律师'], case_folder)):
            os.mkdir(os.path.join(output_path, row['承办律师'], case_folder, '委托材料'))

        if '证据' not in os.listdir(os.path.join(output_path, row['承办律师'], case_folder)):
            os.mkdir(os.path.join(output_path, row['承办律师'], case_folder, '证据'))
            
        if '债转通知' not in os.listdir(os.path.join(output_path, row['承办律师'], case_folder)):
            os.mkdir(os.path.join(output_path, row['承办律师'], case_folder, '债转通知'))
            
    result = "目录已创建"

    # 分发凭证
    pz_list = os.listdir(os.path.join(input_path, '凭证'))

    for pz in pz_list:
        list_id = int(pz.split('-')[0])
        
        if list_id in df['列表ID'].tolist():
            contract_id = df[df['列表ID']==list_id]['合同号'].tolist()[0]

            lawyer = contract_to_lawyer[contract_id]
            case_list = os.listdir(os.path.join(output_path, lawyer))
            case_folder = [folder for folder in case_list if contract_id in folder][0]
            case_path = os.path.join(output_path, lawyer, case_folder)

            if pz.split('-')[-1] not in os.listdir(os.path.join(case_path, '证据')):
                shutil.copy(
                    os.path.join(input_path, '凭证', pz), 
                    os.path.join(case_path, '证据', pz.split('-')[-1])
                )
        else:
            print(f"凭证: {list_id} 不存在")
            
    result += "\n\n凭证已分发"
    
    # 分发债转通知
    zztz_list = os.listdir(os.path.join(input_path, '债转通知'))

    for zztz in zztz_list:
        list_id = int(zztz.split('_')[1].split('.')[0])
        
        if list_id in df['列表ID'].tolist():
            contract_id = df[df['列表ID']==list_id]['合同号'].tolist()[0]
        
            lawyer = contract_to_lawyer[contract_id]
            case_list = os.listdir(os.path.join(output_path, lawyer))
            case_folder = [folder for folder in case_list if contract_id in folder][0]
            case_path = os.path.join(output_path, lawyer, case_folder)

            shutil.copy(
                os.path.join(input_path, '债转通知', zztz), 
                os.path.join(case_path, '债转通知', zztz)
            )
        else:
            print(f"债转通知: {list_id} 不存在")
    
    result += "\n\n债转通知已分发"

    # 分发文档包到证据目录
    doc_pack_level_2 = os.listdir(os.path.join(input_path, '文档包'))[0]
    doc_pack_list = os.listdir(os.path.join(input_path, '文档包', doc_pack_level_2))

    for doc_pack_folder in doc_pack_list:
        # 确定案件的输出目录路径 - 合同号 => 律师 => 案件输出路径
        contract_id = doc_pack_folder
        lawyer = contract_to_lawyer[contract_id]
        case_list = os.listdir(os.path.join(output_path, lawyer))
        case_folder = [folder for folder in case_list if contract_id in folder][0]
        case_path = os.path.join(output_path, lawyer, case_folder)

        # 遍历每个文件，再遍历每个符合要求的证据名称，确认文件是否为证据，是的话就复制到案件输出目录
        for file in os.listdir(os.path.join(input_path, '文档包', doc_pack_level_2, doc_pack_folder)):
            for evidence in EVIDENCE_LIST:
                if evidence in file:
                    if evidence + '.pdf' not in os.listdir(os.path.join(case_path, '证据')):
                        shutil.copy(
                            os.path.join(input_path, '文档包', doc_pack_level_2, doc_pack_folder, file),
                            os.path.join(case_path, '证据', evidence + '.pdf')
                        )
                        # print(os.path.join(case_path, '证据', evidence + '.pdf'))
                        
    result += "\n\n文档包已分发"

    # 分发文件到委托材料目录
    for lawyer in LAWYER_LIST:
        case_list = os.listdir(os.path.join(output_path, lawyer))

        for case_folder in case_list:
            # 确定融担公司
            for rongdan in RONGDAN_LIST:
                if rongdan in case_folder:
                    break
            
            # 确定合同号
            contract_id = case_folder.split('-')[-1]

            # 复制标准文档到委托材料
            standard_doc_list = os.listdir(os.path.join(R'Documents\标准文档', rongdan))
            for standard_doc in standard_doc_list:
                if standard_doc not in os.listdir(os.path.join(output_path, lawyer, case_folder, '委托材料')):
                    shutil.copy(
                        os.path.join(R'Documents\标准文档', rongdan, standard_doc),
                        os.path.join(output_path, lawyer, case_folder, '委托材料')
                    )

            # 复制委托书到委托材料
            wts_list = os.listdir(os.path.join(input_path, '委托书'))

            for wts in wts_list:
                name_wts = wts.split('-')[0].split('委托书')[0]
                number_wts = wts.split('-')[0].split('委托书')[1]
                if name_wts in case_folder and number_wts in case_folder:
                    if '授权委托书.pdf' not in os.listdir(os.path.join(output_path, lawyer, case_folder, '委托材料')):
                        shutil.copy(
                            os.path.join(input_path, '委托书', wts),
                            os.path.join(output_path, lawyer, case_folder, '委托材料', '授权委托书.pdf')
                        )

            # 复制身份证到委托材料
            username = df[df['合同号']==contract_id]['用户名'].tolist()[0]

            id_list = os.listdir(os.path.join(input_path, '身份证_pdf'))

            for id_name in id_list:
                if username in id_name:
                    if '被告-身份证.pdf' not in os.listdir(os.path.join(output_path, lawyer, case_folder)):
                        shutil.copy(
                            os.path.join(input_path, '身份证_pdf', id_name),
                            os.path.join(output_path, lawyer, case_folder, '被告-身份证.pdf')
                        )

            # 复制起诉状到委托材料
            qsz_list = os.listdir(os.path.join(input_path, '起诉状'))

            for qsz in qsz_list:
                name_qsz = qsz.split('-')[0].split('起诉状')[0]
                number_qsz = qsz.split('-')[0].split('起诉状')[1]
                if name_qsz in case_folder and number_qsz in case_folder:
                    if '起诉状.pdf' not in os.listdir(os.path.join(output_path, lawyer, case_folder)):
                        shutil.copy(
                            os.path.join(input_path, '起诉状', qsz),
                            os.path.join(output_path, lawyer, case_folder, '起诉状.pdf')
                        )
                        
    result += "\n\n文件已分发"

    # # 复制一个新的输出目录，按律师要求把案件目录简化(去掉最后的合同号)
    # if 'output_final' not in os.listdir(base_path):
    #     shutil.copytree(output_path, os.path.join(base_path, 'output_final'))

    lawyer_list = os.listdir(output_path)

    for lawyer in lawyer_list:
        case_list = os.listdir(os.path.join(output_path, lawyer))

        for case_folder in case_list:
            if '-' in case_folder:
                os.rename(
                    os.path.join(output_path, lawyer, case_folder),
                    os.path.join(output_path, lawyer, case_folder.split('-')[0]),
                )
    
    return result
            

if __name__ == "__main__":
    doc_packing(
        base_path=BASE_PATH,
        input_path=INPUT_PATH,
        output_path=OUTPUT_PATH
    )