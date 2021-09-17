from collections import OrderedDict
from scripts.realsense import RealSenseManager
from pathlib import Path
import toml

SCRIPT_DIR_PATH = Path(__file__).resolve().parent
CFG_DIR_PATH = Path(SCRIPT_DIR_PATH, "cfg")


def set_intrinsics(dict_toml, key_name, intrinsic):
    dict_toml[key_name]["fx"] = intrinsic.fx
    dict_toml[key_name]["fy"] = intrinsic.fy
    dict_toml[key_name]["cx"] = intrinsic.cx
    dict_toml[key_name]["cy"] = intrinsic.cy


def set_translation_l2r(dict_toml, translation):
    dict_toml["IR_L2R_Translation"]["tx"] = float(translation[0])
    dict_toml["IR_L2R_Translation"]["ty"] = float(translation[1])
    dict_toml["IR_L2R_Translation"]["tz"] = float(translation[2])


def set_translation_l2c(dict_toml, translation):
    dict_toml["IR_L2C_Translation"]["tx"] = float(translation[0])
    dict_toml["IR_L2C_Translation"]["ty"] = float(translation[1])
    dict_toml["IR_L2C_Translation"]["tz"] = float(translation[2])


def main():
    cfg_template_path = str(Path(CFG_DIR_PATH, "realsense_toml_template.toml"))
    cfg_output_path = str(Path(CFG_DIR_PATH, "realsense.toml"))

    decoder = toml.TomlDecoder(_dict=OrderedDict)
    encoder = toml.TomlEncoder(_dict=OrderedDict)
    toml.TomlEncoder = encoder
    dict_toml = toml.load(open(cfg_template_path), _dict=OrderedDict, decoder=decoder)

    rs_mng = RealSenseManager()
    intrinsic_depth = rs_mng.intrinsic_depth
    intrinsic_color = rs_mng.intrinsic_color
    translation_l2r = rs_mng.translation_ir_left2right
    translation_l2c = rs_mng.translation_ir_left2color

    set_intrinsics(dict_toml, "RGB_Intrinsics", intrinsic_color)
    set_intrinsics(dict_toml, "Depth_Intrinsics", intrinsic_depth)
    set_translation_l2r(dict_toml, translation_l2r)
    set_translation_l2r(dict_toml, translation_l2c)

    with open(cfg_output_path, "w") as f:
        toml.encoder.dump(dict_toml, f)
        print("generated")


if __name__ == "__main__":
    main()