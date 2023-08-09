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
        print("template name:", template_name)
        template_ref, window_ref = self.get_template_ref(template_name)
        construction_ref, _, _, _ = self.get_zone_ref(template_ref)
        facade_ref, ground_ref, roof_ref = self.get_house_parts_ref(construction_ref)
        conductivity_dict = dict()
        facade_layers = []
        ground_layers = []
        roof_layers = []

        facade_thermal_resist = 0
        ground_thermal_resist = 0
        roof_thermal_resist = 0

        # layer에 접근
        for structure in self.json_data['OpaqueConstructions']:

            if structure['$id'] == facade_ref:
                for material in structure['Layers']:
                    material_ref = material['Material']['$ref']
                    facade_layers.append(material['Material']['$ref'])
                    facade_thermal_resist += material['Thickness'] / self.opaque_materials[material_ref]

                facade_thermal_resist = 1 / facade_thermal_resist

            if structure['$id'] == ground_ref:
                for material in structure['Layers']:
                    material_ref = material['Material']['$ref']
                    ground_layers.append(material['Material']['$ref'])
                    ground_thermal_resist += material['Thickness'] / self.opaque_materials[material_ref]

                ground_thermal_resist = 1 / ground_thermal_resist

            if structure['$id'] == roof_ref:
                for material in structure['Layers']:
                    material_ref = material['Material']['$ref']
                    roof_layers.append(material['Material']['$ref'])
                    roof_thermal_resist += material['Thickness'] / self.opaque_materials[material_ref]

                roof_thermal_resist = 1 / roof_thermal_resist

        print(facade_thermal_resist, ground_thermal_resist, roof_thermal_resist)

        return facade_layers, ground_layers, roof_layers

    def get_opaque_materials_info(self):
        material_conductivity = dict()
        for material_info in self.json_data['OpaqueMaterials']:
            material_conductivity[material_info['$id']] = material_info['Conductivity']

        return material_conductivity

    def modify_template(self, template_name, sample):
        # '열관류율(외벽)', '열관류율(지붕)', '열관류율(바닥)', '열관류율(창호)', '창면적비', '실내 냉방 설정 온도', '실내 난방 설정 온도', '재실밀도', '기기밀도', '조명밀도', '침기율'
        # zones에 reference 정보를 통해 사용

        print("template name:", template_name)
        template_ref, window_ref = self.get_template_ref(template_name)

        for template_info in self.json_data['Zones']:
            if template_info['$id'] == template_ref:
                constructions_ref = template_info['Constructions']['$ref']
                condition_ref = template_info['Conditioning']['$ref']
                loads_ref = template_info['Loads']['$ref']
                ventil_ref = template_info['Ventilation']['$ref']

        for construction_set in self.json_data['ZoneConstructionSets']:
            print(construction_set)
            if construction_set['$id'] == constructions_ref:
                facade_ref = construction_set['Facade']['$ref']
                ground_ref = construction_set['Ground']['$ref']
                roof_ref = construction_set['Roof']['$ref']
                int_floor_ref = construction_set['Slab']['$ref']


        XPS_REF = 20
        WINDOW_REF = 7

        # 0 ~ 3 Conductivity
        # Conductivity가 아니라 layer Thickness를 조절함


        for structure in self.json_data['OpaqueConstructions']:
            for layer in structure['Layers']:
                layer['Material']['$ref']
                layer['Thickness']
            if structure['$id'] == facade_ref:
                for material in structure['Layers']:
                    if material['Material']['$ref'] == XPS_REF:
                        pass
            if structure['$id'] == ground_ref:
                for material in structure['Layers']:
                    if material['Material']['$ref'] == XPS_REF:
                        pass
            if structure['$id'] == roof_ref:
                for material in structure['Layers']:
                    if material['Material']['$ref'] == XPS_REF:
                        pass

        # for structure in self.json_data['WindowConstructions']:
        #     if structure['$id'] == window_ref:
        #         for layer in structure['Layers']:
        #             if layer['Material']['$ref'] == WINDOW_REF:
        #                 layer['Thickness'] = sample[3]


        # 4 BuildingTemplates의 'DefaultWindowToWallRatio'
        for building_template_info in self.json_data['BuildingTemplates']:
            if building_template_info['Core']['$ref'] == template_ref:
                window_to_wall_ratio = building_template_info['DefaultWindowToWallRatio']
                print("DefaultWindowToWallRatio:", window_to_wall_ratio)
                building_template_info['DefaultWindowToWallRatio'] = sample[4]
                print("sample:", sample[4])

        
        # 5 ~ 6 ZoneConditionings의 'CoolingSetpoint', 'HeatingSetpoint'
        for zone_condition_info in self.json_data['ZoneConditionings']:
            if zone_condition_info['$id'] == condition_ref:
                cooling_setpoint = zone_condition_info['CoolingSetpoint']
                print("CoolingSetpoint:", cooling_setpoint)
                zone_condition_info['CoolingSetpoint'] = sample[5]
                print("sample:", sample[5])

                heating_setpoint = zone_condition_info['HeatingSetpoint']
                print("HeatingSetpoint:", heating_setpoint)
                zone_condition_info['HeatingSetpoint'] = sample[6]
                print("sample:", sample[6])


        # 7 ~ 9 ZoneLoads의 'EquipmentPowerDensity', 'LightingPowerDensity', 'PeopleDensity'
        for zone_load_info in self.json_data['ZoneLoads']:
            if zone_load_info['$id'] == loads_ref:
                equipment_power_density = zone_load_info['EquipmentPowerDensity']
                print("EquipmentPowerDensity:", equipment_power_density)
                zone_load_info['EquipmentPowerDensity'] = sample[7]
                print("sample:", sample[7])

                lighting_power_density = zone_load_info['LightingPowerDensity']
                print("LightingPowerDensity:", lighting_power_density)
                zone_load_info['LightingPowerDensity'] = sample[8]
                print("sample:", sample[8])

                people_density = zone_load_info['PeopleDensity']
                print("PeopleDensity:", people_density)
                zone_load_info['PeopleDensity'] = sample[9]
                print("sample:", sample[9])

        # 10 VentilationSettings의 'Infiltration'
        for ventilation_info in self.json_data['VentilationSettings']:
            if ventilation_info['$id'] == ventil_ref:
                infiltration = ventilation_info['Infiltration']
                print("Infiltration:", infiltration)
                ventilation_info['Infiltration'] = sample[10]
                print("sample:", sample[10])

        with open(self.json_path, 'w') as json_file:
            json.dump(self.json_data, json_file, indent=2)