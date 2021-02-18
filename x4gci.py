#!/usr/bin/env python3

import argparse
import os
import re
import sys
import webbrowser
from pathlib import Path
from typing import List, Dict
from xml.etree import ElementTree

MODULES = ['module_arg_conn_base_01',
           'module_arg_conn_base_02',
           'module_arg_conn_base_03',
           'module_arg_conn_cross_01',  # struct_arg_cross_01_macro
           'module_arg_conn_vertical_01',
           'module_arg_conn_vertical_02',
           'module_arg_def_claim_01',
           'module_arg_def_disc_01',
           'module_arg_def_tube_01',
           'module_arg_dock_m_01',  # dockarea_arg_m_station_01_lowtech_macro
           'module_arg_dock_m_01_hightech',
           'module_arg_dock_m_01_lowtech',
           'module_arg_dock_m_02',
           'module_arg_dock_m_02_hightech',
           'module_arg_dock_m_02_lowtech',
           'module_arg_dock_tradestation_02',
           'module_arg_hab_l_01',
           'module_arg_hab_m_01',
           'module_arg_hab_s_01',
           'module_arg_pier_l_01',
           'module_arg_pier_l_02',
           'module_arg_pier_l_03',
           'module_arg_prod_foodrations_01',
           'module_arg_prod_meat_01',
           'module_arg_prod_medicalsupplies_01',
           'module_arg_prod_spacefuel_01',
           'module_arg_prod_wheat_01',
           'module_arg_stor_container_l_01',
           'module_arg_stor_container_m_01',
           'module_arg_stor_container_s_01',
           'module_arg_stor_liquid_l_01',  # storage_arg_l_liquid_01_macro
           'module_arg_stor_liquid_m_01',
           'module_arg_stor_liquid_s_01',
           'module_arg_stor_solid_l_01',
           'module_arg_stor_solid_m_01',
           'module_arg_stor_solid_s_01',
           'module_gen_build_dockarea_m_01',
           'module_gen_build_l_01',
           'module_gen_build_xl_01',
           'module_gen_equip_dockarea_m_01',
           'module_gen_equip_l_01',
           'module_gen_equip_xl_01',
           'module_gen_prod_advancedcomposites_01',  # prod_gen_advancedcomposites_macro
           'module_gen_prod_advancedelectronics_01',
           'module_gen_prod_antimattercells_01',
           'module_gen_prod_antimatterconverters_01',
           'module_gen_prod_claytronics_01',
           'module_gen_prod_dronecomponents_01',
           'module_gen_prod_energycells_01',
           'module_gen_prod_engineparts_01',
           'module_gen_prod_fieldcoils_01',
           'module_gen_prod_graphene_01',
           'module_gen_prod_hullparts_01',
           'module_gen_prod_microchips_01',
           'module_gen_prod_missilecomponents_01',
           'module_gen_prod_plasmaconductors_01',
           'module_gen_prod_quantumtubes_01',
           'module_gen_prod_refinedmetals_01',
           'module_gen_prod_scanningarrays_01',
           'module_gen_prod_shieldcomponents_01',
           'module_gen_prod_siliconwafers_01',
           'module_gen_prod_smartchips_01',
           'module_gen_prod_spices_01',
           'module_gen_prod_superfluidcoolant_01',
           'module_gen_prod_turretcomponents_01',
           'module_gen_prod_water_01',
           'module_gen_prod_weaponcomponents_01',
           'module_par_conn_base_01',
           'module_par_conn_base_02',
           'module_par_conn_base_03',
           'module_par_conn_cross_01',
           'module_par_conn_cross_02',
           'module_par_conn_cross_03',
           'module_par_conn_vertical_01',
           'module_par_conn_vertical_02',
           'module_par_def_claim_01',
           'module_par_def_disc_01',
           'module_par_def_tube_01',
           'module_par_hab_l_01',
           'module_par_hab_m_01',
           'module_par_hab_s_01',
           'module_par_pier_l_01',
           'module_par_pier_l_02',
           'module_par_pier_l_03',
           'module_par_prod_majadust_01',
           'module_par_prod_majasnails_01',
           'module_par_prod_medicalsupplies_01',
           'module_par_prod_sojabeans_01',
           'module_par_prod_sojahusk_01',
           'module_par_stor_container_l_01',
           'module_par_stor_container_m_01',
           'module_par_stor_container_s_01',
           'module_par_stor_liquid_l_01',
           'module_par_stor_liquid_m_01',
           'module_par_stor_liquid_s_01',
           'module_par_stor_solid_l_01',
           'module_par_stor_solid_m_01',
           'module_par_stor_solid_s_01',
           'module_tel_conn_base_01',
           'module_tel_conn_base_02',
           'module_tel_conn_base_03',
           'module_tel_conn_cross_01',
           'module_tel_conn_vertical_01',
           'module_tel_conn_vertical_02',
           'module_tel_def_claim_01',
           'module_tel_def_disc_01',
           'module_tel_def_tube_01',
           'module_tel_hab_l_01',
           'module_tel_hab_m_01',
           'module_tel_hab_s_01',
           'module_tel_pier_l_01',
           'module_tel_pier_l_02',
           'module_tel_pier_l_03',
           'module_tel_prod_advancedcomposites_01',
           'module_tel_prod_engineparts_01',
           'module_tel_prod_hullparts_01',
           'module_tel_prod_medicalsupplies_01',
           'module_tel_prod_nostropoil_01',
           'module_tel_prod_scanningarrays_01',
           'module_tel_prod_spaceweed_01',
           'module_tel_prod_sunriseflowers_01',
           'module_tel_prod_swampplant_01',
           'module_tel_prod_teladianium_01',
           'module_tel_stor_container_l_01',
           'module_tel_stor_container_m_01',
           'module_tel_stor_container_s_01',
           'module_tel_stor_liquid_l_01',
           'module_tel_stor_liquid_m_01',
           'module_tel_stor_liquid_s_01',
           'module_tel_stor_solid_l_01',
           'module_tel_stor_solid_m_01',
           'module_tel_stor_solid_s_01',
           'module_spl_conn_base_01',
           'module_spl_conn_base_02',
           'module_spl_conn_base_03',
           'module_spl_conn_cross_01',
           'module_spl_conn_vertical_01',
           'module_spl_conn_vertical_02',
           'module_spl_def_claim_01',
           'module_spl_def_disc_01',
           'module_spl_def_tube_01',
           'module_spl_hab_l_01',
           'module_spl_hab_m_01',
           'module_spl_hab_s_01',
           'module_spl_pier_l_01',
           'module_spl_pier_l_02',
           'module_spl_pier_l_03',
           'module_spl_prod_cheltmeat_01',
           'module_spl_prod_medicalsupplies_01',
           'module_spl_prod_scruffinfruits_01',
           'module_spl_stor_container_l_01',
           'module_spl_stor_container_m_01',
           'module_spl_stor_container_s_01',
           'module_spl_stor_liquid_l_01',
           'module_spl_stor_liquid_m_01',
           'module_spl_stor_liquid_s_01',
           'module_spl_stor_solid_l_01',
           'module_spl_stor_solid_m_01',
           'module_spl_stor_solid_s_01', ]

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Import X4 constructionplan XML to http://x4-game.com')
    arg_parser.add_argument('path', help='Path to the XML file containing the construction plan', type=Path)
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    if not os.path.isfile(parsed_args.path):
        print(f"File not found: {parsed_args.path}")
        exit(1)

    tree = ElementTree.parse(parsed_args.path)
    root = tree.getroot()

    modules: Dict[str, int] = {}

    for entry in root.iter("entry"):
        macro = re.sub('_macro$', '', entry.attrib["macro"]).split('_')
        # prod_gen -> gen_prod
        macro[0], macro[1] = macro[1], macro[0]

        if macro[1] == 'buildmodule':
            macro[1] = "build"
            del macro[2]
            if 'dockarea' in macro:
                macro[2], macro[3] = macro[3], macro[2]
            else:
                macro.append('01')
        elif macro[1] == 'defence':
            macro[1] = "def"
        elif macro[1] == 'dockarea':
            macro[1] = "dock"
            if 'tradestation' in macro:
                macro[5] = macro[3]
                del macro[2]
                del macro[2]
            else:
                del macro[3]
        elif macro[1] == 'hab':
            pass
        elif macro[1] == 'pier':
            if 'harbor' in macro:
                macro[2] = 'l'
        elif macro[1] == 'prod':
            macro.append('01')
            if 'scruffinfruit' in macro:
                macro[2] = macro[2] + 's'

        elif macro[1] == 'storage':
            macro[1] = "stor"
            macro[2], macro[3] = macro[3], macro[2]
        elif macro[1] == 'struct':
            macro[1] = "conn"
            continue

        macro.insert(0, 'module')

        if 'research' not in macro:
            module = '_'.join(macro)
            if module in modules:
                modules[module] = modules[module] + 1
            else:
                modules[module] = 1

    params: List[str] = []
    for module, count in modules.items():
        if module in MODULES:
            params.append(f"$module-{module},count:{count}")
        else:
            print(f"Unknown module: {module}")

    url = "http://www.x4-game.com/#/station-calculator?l=@" + ';,'.join(params)
    print(url)
    webbrowser.open(url)
