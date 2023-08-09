import change
import LHS
import pandas as pd
import os

if __name__ == "__main__":
    db_path = "umi.sqlite3"
    json_path = "BostonTemplateLibrary.json"
    
    modifier = change.Modifier(db_path, json_path)
    # modifier 객체 생성
    
    modifier.open_db_con()
    # db connection 열기
    modifier.get_template_info()
    # template name과 id들 받아오기
    keys = modifier.get_dict_keys()

    sample_df_dict = {}
    folder_path = "./data"

    for template_name in keys:
        LHS.sampling(3, template_name)
        file_name = "samples_" + template_name + ".csv"
        file_path = os.path.join(folder_path, file_name)
        sample_df_dict[template_name] = pd.read_csv(file_path, encoding='utf-8')

    for epoch in range(1):
        for template_name in keys:
            print(modifier.get_building_conductivity(template_name))
            # LHS sampling
            # sample = sample_df_dict[template_name].iloc[epoch]

            # sample 기반 template 별 수정
            # modifier.modify_template(template_name, sample)
        
        # simulation 수행
        