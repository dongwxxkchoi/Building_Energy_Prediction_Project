import change
import LHS
import pandas as pd
import numpy as np
import os

if __name__ == "__main__":
    db_path = "umi.sqlite3"
    json_path = "data/json_files/BostonTemplateLibraryModified.json"
    
    modifier = change.Modifier(db_path, json_path)
    # modifier 객체 생성
    modifier.open_db_con()
    # db connection 열기
    modifier.get_template_info()
    # template name과 id들 받아오기
    keys = modifier.get_dict_keys()
    folder_path = "./data"
    columns = ['열관류율(외벽)','열관류율(지붕)','열관류율(바닥)','열관류율(창호)','창면적비','실내 냉방 설정 온도','실내 난방 설정 온도','재실밀도','기기밀도','조명밀도','침기율']

    for epoch in range(1000):
        if epoch % 100 == 0:
            print(epoch, "/ 1000")
        for template_name in keys:
            # LHS sampling
            epoch_samples = LHS.sampling()
            # input_samples = epoch_sample_df[template_name].iloc[epoch]

            # sample 기반 template 별 수정
            if template_name == 'Boston_Res_0_Masonry':
                output_samples = modifier.modify_template(template_name, epoch_samples, res=True)
            else:
                output_samples = modifier.modify_template(template_name, epoch_samples, res=False)

            file_name = "samples_" + template_name + ".csv"
            file_path = os.path.join(folder_path, file_name)

            output_samples = [output_samples]
            epoch_sample_df = pd.DataFrame(output_samples, columns=columns)

            samples_df = pd.read_csv(file_path, encoding='utf-8')
            samples_df = pd.concat([samples_df, epoch_sample_df], ignore_index=True)
            samples_df.to_csv(file_path, encoding='utf-8', index=False)
            # simulation 수행

