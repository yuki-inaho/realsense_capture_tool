import click
import cv2
import cvui
import numpy as np
from pathlib import Path
from scripts.realsense import RealSenseManager
from scripts.utils import (
    colorize_depth,
    get_time,
    make_save_dir,
    clean_save_dir,
    count_images,
    draw_frames,
    save_images,
)


SCRIPT_DIR_PATH = Path(__file__).resolve().parent


@click.command()
@click.option("--save-dir", "-s", default="{}/data".format(SCRIPT_DIR_PATH))
@click.option("--view-ir", "-ir", is_flag=True)
@click.option("--laser-off", "-l", is_flag=True)
@click.option("--laser-alternate-mode", "-a", is_flag=True)
def main(save_dir, view_ir, laser_off, laser_alternate_mode):
    make_save_dir(save_dir)
    rs_mng = RealSenseManager()  # default image size = (1280, 720)
    if laser_alternate_mode:
        rs_mng.laser_turn_on()
        rs_mng.enable_emitter_alternate_mode()
    else:
        if laser_off:
            rs_mng.laser_turn_off()
        else:
            rs_mng.laser_turn_on()

    image_width, image_height = rs_mng.image_size
    res_image_width = int(image_width * 2 / 3)
    res_image_height = int(image_height * 2 / 3)
    window_image_width = int(image_width * 4 / 3)
    window_image_height = int(image_height)

    cvui.init("capture")
    frame = np.zeros((window_image_height, window_image_width, 3), np.uint8)
    captured_frame_count = count_images(save_dir)

    while True:
        key = cv2.waitKey(10)
        frame[:] = (49, 52, 49)

        status = rs_mng.update()
        if status:
            # Get Images
            ir_image_left = rs_mng.ir_frame_left
            ir_image_right = rs_mng.ir_frame_right
            color_image = rs_mng.color_frame
            depth_image = rs_mng.depth_frame
            depth_image_aligned2color = rs_mng.depth_frame_aligned2color

            # Visualize Images
            if view_ir:
                ir_image_left_uc8 = cv2.cvtColor(ir_image_left, cv2.COLOR_GRAY2BGR)
                frame = draw_frames(frame, ir_image_left_uc8, depth_image, res_image_width, res_image_height)
            else:
                frame = draw_frames(frame, color_image, depth_image, res_image_width, res_image_height)

            if cvui.button(frame, 50, res_image_height + 50, 130, 50, "Save Result Image") or key & 0xFF == ord("s"):
                save_images(color_image, depth_image, depth_image_aligned2color, ir_image_left, ir_image_right, save_dir)
                captured_frame_count += 1

            if cvui.button(frame, 200, res_image_height + 50, 130, 50, "Clear"):
                clean_save_dir(save_dir)
                captured_frame_count = 0

            if cvui.button(frame, 350, res_image_height + 50, 150, 50, "Toggle Emitter On-Off"):
                if rs_mng.is_emitter_enabled:
                    rs_mng.laser_turn_off()
                else:
                    rs_mng.laser_turn_on()

            if cvui.button(frame, 550, res_image_height + 50, 250, 50, "Toggle Emitter Alternate Mode"):
                if rs_mng.is_emitter_alternate_mode_enabled:
                    rs_mng.disable_emitter_alternate_mode()
                else:
                    rs_mng.enable_emitter_alternate_mode()

            cvui.printf(frame, 50, res_image_height + 150, 0.8, 0x00FF00, "Number of Captured Images : %d", captured_frame_count)
            if key & 0xFF == ord("q"):
                break

            cvui.update()
            cvui.imshow("capture", frame)

    cv2.destroyAllWindows()
    del rs_mng


if __name__ == "__main__":
    main()