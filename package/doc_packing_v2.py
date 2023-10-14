import os
import shutil
import pandas as pd

# 设定输入目录和输出目录
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

# 设定BASE目录路径，输入目录路径，输出目录路径
BASE_PATH = R'Documents\2023\10\文档自动归类'
INPUT_PATH = os.path.join(BASE_PATH, INPUT_FOLDER)
OUTPUT_PATH = os.path.join(BASE_PATH, OUTPUT_FOLDER)

# 设定表格文件名，律师人名
EXCEL_FILE = 'info.xlsx'
LAWYER_LIST = ['王磊', '张立人']

# 设定融担公司
RONGDAN_LIST = [
    '福建智云',
    '海南申信',
    '上海耳序'
]

# 合同号与律师对应关系
CONTRACT_TO_LAWYER = {}

# 证据文档列表
EVIDENCE_LIST = [
    '贷款合同',
    '个人委托担保协议',
    '不可撤销担保函',
    '借款服务协议',
    '债权转让协议'
]


# 读取表格到 Pandas Dataframe
df = pd.read_excel(os.path.join(INPUT_PATH, EXCEL_FILE))

# 创建输出目录
if OUTPUT_FOLDER not in os.listdir(BASE_PATH):
    os.mkdir(OUTPUT_PATH)

# 创建律师目录
for lawyer in LAWYER_LIST:
    if lawyer not in os.listdir(OUTPUT_PATH):
        os.mkdir(os.path.join(OUTPUT_PATH, lawyer))

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

    CONTRACT_TO_LAWYER[contract_id] = row['承办律师']

    case_folder = f'{idx}{rongdan}_{person} {court}-{contract_id}'
    
    if case_folder not in os.listdir(os.path.join(OUTPUT_PATH, row['承办律师'])):
        os.mkdir(os.path.join(OUTPUT_PATH, row['承办律师'], case_folder))

    if '委托材料' not in os.listdir(os.path.join(OUTPUT_PATH, row['承办律师'], case_folder)):
        os.mkdir(os.path.join(OUTPUT_PATH, row['承办律师'], case_folder, '委托材料'))

    if '证据' not in os.listdir(os.path.join(OUTPUT_PATH, row['承办律师'], case_folder)):
        os.mkdir(os.path.join(OUTPUT_PATH, row['承办律师'], case_folder, '证据'))

# 分发凭证
pz_list = os.listdir(os.path.join(INPUT_PATH, '凭证'))

for pz in pz_list:
    list_id = int(pz.split('-')[0])
    contract_id = df[df['列表ID']==list_id]['合同号'].tolist()[0]

    lawyer = CONTRACT_TO_LAWYER[contract_id]
    case_list = os.listdir(os.path.join(OUTPUT_PATH, lawyer))
    case_folder = [folder for folder in case_list if contract_id in folder][0]
    case_path = os.path.join(OUTPUT_PATH, lawyer, case_folder)

    if pz.split('-')[-1] not in os.listdir(os.path.join(case_path, '证据')):
        shutil.copy(
            os.path.join(INPUT_PATH, '凭证', pz), 
            os.path.join(case_path, '证据', pz.split('-')[-1])
        )

# 分发文档包到证据目录
doc_pack_level_2 = os.listdir(os.path.join(INPUT_PATH, '文档包'))[0]
doc_pack_list = os.listdir(os.path.join(INPUT_PATH, '文档包', doc_pack_level_2))

for doc_pack_folder in doc_pack_list:
    # 确定案件的输出目录路径 - 合同号 => 律师 => 案件输出路径
    contract_id = doc_pack_folder
    lawyer = CONTRACT_TO_LAWYER[contract_id]
    case_list = os.listdir(os.path.join(OUTPUT_PATH, lawyer))
    case_folder = [folder for folder in case_list if contract_id in folder][0]
    case_path = os.path.join(OUTPUT_PATH, lawyer, case_folder)

    # 遍历每个文件，再遍历每个符合要求的证据名称，确认文件是否为证据，是的话就复制到案件输出目录
    for file in os.listdir(os.path.join(INPUT_PATH, '文档包', doc_pack_level_2, doc_pack_folder)):
        for evidence in EVIDENCE_LIST:
            if evidence in file:
                if evidence + '.pdf' not in os.listdir(os.path.join(case_path, '证据')):
                    shutil.copy(
                        os.path.join(INPUT_PATH, '文档包', doc_pack_level_2, doc_pack_folder, file),
                        os.path.join(case_path, '证据', evidence + '.pdf')
                    )
                    print(os.path.join(case_path, '证据', evidence + '.pdf'))

# 分发文件到委托材料
for lawyer in LAWYER_LIST:
    case_list = os.listdir(os.path.join(OUTPUT_PATH, lawyer))

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
            if standard_doc not in os.listdir(os.path.join(OUTPUT_PATH, lawyer, case_folder, '委托材料')):
                shutil.copy(
                    os.path.join(R'Documents\标准文档', rongdan, standard_doc),
                    os.path.join(OUTPUT_PATH, lawyer, case_folder, '委托材料')
                )

        # 复制委托书到委托材料
        wts_list = os.listdir(os.path.join(INPUT_PATH, '委托书'))

        for wts in wts_list:
            if contract_id in wts:
                if '授权委托书.pdf' not in os.listdir(os.path.join(OUTPUT_PATH, lawyer, case_folder, '委托材料')):
                    shutil.copy(
                        os.path.join(INPUT_PATH, '委托书', wts),
                        os.path.join(OUTPUT_PATH, lawyer, case_folder, '委托材料', '授权委托书.pdf')
                    )

        # 复制委托书到委托材料
        username = df[df['合同号']==contract_id]['用户名'].tolist()[0]

        id_list = os.listdir(os.path.join(INPUT_PATH, '身份证_pdf'))

        for id_name in id_list:
            if username in id_name:
                if '被告-身份证.pdf' not in os.listdir(os.path.join(OUTPUT_PATH, lawyer, case_folder)):
                    shutil.copy(
                        os.path.join(INPUT_PATH, '身份证_pdf', id_name),
                        os.path.join(OUTPUT_PATH, lawyer, case_folder, '被告-身份证.pdf')
                    )

        # 复制起诉状到委托材料
        qsz_list = os.listdir(os.path.join(INPUT_PATH, '起诉状'))

        for qsz in qsz_list:
            if contract_id in qsz:
                if '起诉状.pdf' not in os.listdir(os.path.join(OUTPUT_PATH, lawyer, case_folder)):
                    shutil.copy(
                        os.path.join(INPUT_PATH, '起诉状', qsz),
                        os.path.join(OUTPUT_PATH, lawyer, case_folder, '起诉状.pdf')
                    )
