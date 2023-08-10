import pandas as pd
import json
import sqlite3
from collections import defaultdict
import LHS
import os

class Modifier:
    def __init__(self, db_path, json_path):
        # db엔 창면적비 등의 템플릿 외부 정보
        # json엔 템플릿 별 속성 등의 템플릿 내부 정보가 담겨 있음
        self.conn = None
        self.cursor = None
        self.db_path = db_path
        self.json_path = json_path
        self.json_data = None
        self.id_template_dict = None
        self.XPS_REF = 20
        self.WINDOW_REF = 7

        with open(json_path, 'r') as f:
            self.json_data = json.load(f)

        self.opaque_materials = self.get_opaque_materials_info()
        self.glazing_materials = self.get_glazing_materials_info()

    def get_dict_keys(self):
        return self.id_template_dict.keys()

    def open_db_con(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_db_con(self):
        with self.conn:
            with open('dump.sql', 'w') as f:
                for line in self.conn.iterdump():
                    f.write('%s\n' % line)
                print('Completed.')

        self.conn.close()

    def execute_db(self, query):
        self.cursor.execute(query)
        tables = self.cursor.fetchall()

        return tables

    def get_template_info(self):
        query = ('SELECT object_id, name, value\n'
                 '                       FROM nonplottable_setting\n')
        tables = self.execute_db(query)
        id_template_dict = defaultdict(list)
        for i, row in enumerate(tables):
            if i % 3 == 0:
                id_template_dict[row[2]].append(row[0])

        self.id_template_dict = id_template_dict


    def get_template_ref(self, template_name):
        template_ref, window_ref = None, None
        for template_info in self.json_data['BuildingTemplates']:
            if template_info['Name'] == template_name:
                template_ref = template_info['Core']['$ref']
                window_ref = template_info['Windows']['Construction']['$ref']

        return template_ref, window_ref


    # construction, conditioning, loads, ventilation ref 받음
    def get_zone_ref(self, template_ref):
        for template_info in self.json_data['Zones']:
            if template_info['$id'] == template_ref:
                constructions_ref = template_info['Constructions']['$ref']
                condition_ref = template_info['Conditioning']['$ref']
                loads_ref = template_info['Loads']['$ref']
                ventil_ref = template_info['Ventilation']['$ref']

        return constructions_ref, condition_ref, loads_ref, ventil_ref

    # construction 구성 요소 ref 받음
    def get_house_parts_ref(self, construction_ref):
        for construction_set in self.json_data['ZoneConstructionSets']:
            if construction_set['$id'] == construction_ref:
                facade_ref = construction_set['Facade']['$ref']
                ground_ref = construction_set['Ground']['$ref']
                roof_ref = construction_set['Roof']['$ref']

        return facade_ref, ground_ref, roof_ref

    def get_building_conductivity(self, template_name):
        template_ref, window_ref = self.get_template_ref(template_name)
        construction_ref, _, _, _ = self.get_zone_ref(template_ref)
        facade_ref, ground_ref, roof_ref = self.get_house_parts_ref(construction_ref)

        conductivity_dict = dict()
        facade_layers = []
        ground_layers = []
        roof_layers = []
        window_layers = []

        facade_thermal_resist = 0
        ground_thermal_resist = 0
        roof_thermal_resist = 0
        window_thermal_resist = 0


        # layer에 접근
        for structure in self.json_data['OpaqueConstructions']:
            if structure['$id'] == facade_ref:
                for layer in structure['Layers']:
                    material_ref = layer['Material']['$ref']
                    facade_layers.append(layer['Material']['$ref'])
                    facade_thermal_resist += layer['Thickness'] / self.opaque_materials[material_ref][-1]

                facade_thermal_resist = 1 / facade_thermal_resist

            if structure['$id'] == ground_ref:
                for layer in structure['Layers']:
                    material_ref = layer['Material']['$ref']
                    ground_layers.append(layer['Material']['$ref'])
                    ground_thermal_resist += layer['Thickness'] / self.opaque_materials[material_ref][-1]

                ground_thermal_resist = 1 / ground_thermal_resist

            if structure['$id'] == roof_ref:
                for layer in structure['Layers']:
                    material_ref = layer['Material']['$ref']
                    roof_layers.append(layer['Material']['$ref'])
                    roof_thermal_resist += layer['Thickness'] / self.opaque_materials[material_ref][-1]

                roof_thermal_resist = 1 / roof_thermal_resist

        for structure in self.json_data['WindowConstructions']:
            if structure['$id'] == window_ref:
                for layer in structure['Layers']:
                    material_ref = layer['Material']['$ref']
                    window_layers.append(layer['Material']['$ref'])
                    if material_ref == '9': ## 유리
                        window_thermal_resist += layer['Thickness'] / self.glazing_materials[material_ref][-1]
                    elif material_ref == '2': ## ARGON
                        window_thermal_resist += layer['Thickness'] / 0.016

                window_thermal_resist = 1 / window_thermal_resist

        return facade_thermal_resist, roof_thermal_resist, ground_thermal_resist, window_thermal_resist

    def get_opaque_materials_info(self):
        material_conductivity = dict()
        for material_info in self.json_data['OpaqueMaterials']:
            material_conductivity[material_info['$id']] = [material_info['Name'], material_info['Conductivity']]

        return material_conductivity

    def get_glazing_materials_info(self):
        material_conductivity = dict()
        for material_info in self.json_data['GlazingMaterials']:
            material_conductivity[material_info['$id']] = [material_info['Name'], material_info['Conductivity']]

        return material_conductivity

    def modify_json(self, keys, data):
        if len(keys) == 1:
            key = keys
            self.json_data[key] = data
        elif len(keys) == 2:
            key1, key2 = keys
            self.json_data[key1][key2] = data
        elif len(keys) == 3:
            key1, key2, key3 = keys
            self.json_data[key1][key2][key3] = data
        elif len(keys) == 4:
            key1, key2, key3, key4 = keys
            self.json_data[key1][key2][key3][key4] = data
        elif len(keys) == 5:
            key1, key2, key3, key4, key5 = keys
            self.json_data[key1][key2][key3][key4][key5] = data

    def modify_template(self, template_name, sample, res=False):
        # '열관류율(외벽)', '열관류율(지붕)', '열관류율(바닥)', '열관류율(창호)', '창면적비', '실내 냉방 설정 온도', '실내 난방 설정 온도', '재실밀도', '기기밀도', '조명밀도', '침기율'
        # zones에 reference 정보를 통해 사용

        # print("template name:", template_name)
        template_ref, window_ref = self.get_template_ref(template_name)
        constructions_ref, condition_ref, loads_ref, ventil_ref = self.get_zone_ref(template_ref)
        facade_ref, ground_ref, roof_ref = self.get_house_parts_ref(constructions_ref)

        XPS_REF = '20'
        ARGON_REF = '2'

        # 0 ~ 3 Conductivity
        # Conductivity가 아니라 layer Thickness를 조절함

        for idx_outer, structure in enumerate(self.json_data['OpaqueConstructions']):
            if structure['$id'] == facade_ref:
                for idx_inner, layer in enumerate(structure['Layers']):
                    if layer['Material']['$ref'] == XPS_REF:
                        self.modify_json(['OpaqueConstructions', idx_outer, 'Layers', idx_inner, 'Thickness'], sample[0])
            if structure['$id'] == roof_ref:
                for idx_inner, layer in enumerate(structure['Layers']):
                    if layer['Material']['$ref'] == XPS_REF:
                        if res:
                            self.modify_json(['OpaqueConstructions', idx_outer, 'Layers', idx_inner, 'Thickness'], sample[2])
                        else:
                            self.modify_json(['OpaqueConstructions', idx_outer, 'Layers', idx_inner, 'Thickness'], sample[1])
            if structure['$id'] == ground_ref: # Off, Ret
                for idx_inner, layer in enumerate(structure['Layers']):
                    if layer['Material']['$ref'] == XPS_REF:
                        self.modify_json(['OpaqueConstructions', idx_outer, 'Layers', idx_inner, 'Thickness'], sample[3])

        for idx_outer, structure in enumerate(self.json_data['WindowConstructions']):
            if structure['$id'] == window_ref:
                for idx_inner, layer in enumerate(structure['Layers']):
                    if layer['Material']['$ref'] == ARGON_REF:
                        self.modify_json(['WindowConstructions', idx_outer, 'Layers', idx_inner, 'Thickness'], sample[4])

        # 4 BuildingTemplates의 'DefaultWindowToWallRatio'
        for idx, building_template_info in enumerate(self.json_data['BuildingTemplates']):
            if building_template_info['Core']['$ref'] == template_ref:
                self.modify_json(['BuildingTemplates', idx, 'DefaultWindowToWallRatio'], sample[5])


        # 5 ~ 6 ZoneConditionings의 'CoolingSetpoint', 'HeatingSetpoint'
        for idx, zone_condition_info in enumerate(self.json_data['ZoneConditionings']):
            if zone_condition_info['$id'] == condition_ref:
                self.modify_json(['ZoneConditionings', idx, 'CoolingSetpoint'], sample[6])
                self.modify_json(['ZoneConditionings', idx, 'HeatingSetpoint'], sample[7])


        # 7 ~ 9 ZoneLoads의 'EquipmentPowerDensity', 'LightingPowerDensity', 'PeopleDensity'
        for idx, zone_load_info in enumerate(self.json_data['ZoneLoads']):
            if zone_load_info['$id'] == loads_ref:
                self.modify_json(['ZoneLoads', idx, 'EquipmentPowerDensity'], sample[8])
                self.modify_json(['ZoneLoads', idx, 'LightingPowerDensity'], sample[9])
                self.modify_json(['ZoneLoads', idx, 'PeopleDensity'], sample[10])

        # 10 VentilationSettings의 'Infiltration'
        for idx, ventilation_info in enumerate(self.json_data['VentilationSettings']):
            if ventilation_info['$id'] == ventil_ref:
                self.modify_json(['VentilationSettings', idx, 'Infiltration'], sample[11])

        total_conductivity = self.get_building_conductivity(template_name)
        # 열관류율(외벽), 열관류율(지붕(Off, Ret)), 열관류율(지붕(Res)), 열관류율(바닥), 열관류율(창호), 창면적비, 실내 냉방 설정 온도, 실내 난방 설정 온도, 재실밀도, 기기밀도, 조명밀도, 침기율
        # print("열관류율(외벽):", total_conductivity[0])
        # print("열관류율(지붕):", total_conductivity[1])
        # print("열관류율(바닥):", total_conductivity[2])
        # print("열관류율(창호):", total_conductivity[3])
        # print("창면적비:", sample[5])
        # print("실내 냉방 설정 온도:", sample[6])
        # print("실내 난방 설정 온도:", sample[7])
        # print("재실밀도:", sample[8])
        # print("기기밀도:", sample[9])
        # print("조명밀도:", sample[10])
        # print("침기율:", sample[11])

        with open('BostonTemplateLibraryModified.json', 'w') as json_file:
            json.dump(self.json_data, json_file, indent=2)

        output_samples = list(total_conductivity)[:] + sample[5:12]

        return output_samples