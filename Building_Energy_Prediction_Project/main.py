import change
import LHS
import pandas as pd
import numpy as np
import os

if __name__ == "__main__":
    db_path = "data/db_files/umi.sqlite3"
    json_path = "data/json_files/BostonTemplateLibraryModified.json"
    
    modifier = change.Modifier(db_path, json_path)
    # modifier 객체 생성
    modifier.open_db_con()
    # db connection 열기
    modifier.get_template_info()
    # template name과 id들 받아오기
    keys = modifier.get_dict_keys()

    template_df_dicts = dict()
    folder_path = "./data/lhs_sample"

    for key in keys:
        if 'Res' in key:
            res = True
        else: res = False
        LHS.samples_to_csv(key, res)
        file_name = "samples_" + key + ".csv"
        template_df_dicts[key] = pd.read_csv(os.path.join(folder_path, file_name))

    # '열관류율(외벽)','열관류율(지붕)','열관류율(바닥)','열관류율(창호)','창면적비','실내 냉방 설정 온도','실내 난방 설정 온도','재실밀도','기기밀도','조명밀도','침기율'

    for epoch in range(1, 1000+1):
        if epoch % 100 == 0:
            print(epoch, "/ 1000")
        for template_name in keys:
            samples_df = template_df_dicts[template_name]
            epoch_samples = samples_df.loc[epoch-1].values.tolist()
            modifier.modify_template(template_name, epoch_samples, epoch)

        modifier.update_json(epoch)
