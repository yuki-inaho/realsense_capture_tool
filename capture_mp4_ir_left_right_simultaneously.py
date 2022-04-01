import click
import cv2
from pathlib import Path
from scripts.realsense import RealSenseManager
from pytz import timezone
from datetime import datetime


SCRIPT_DIR_PATH = Path(__file__).resolve().parent


def gray2bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def get_time():
    utc_now = datetime.now(timezone("UTC"))
    jst_now = utc_now.astimezone(timezone("Asia/Tokyo"))
    time = str(jst_now).split(".")[0].split(" ")[0] + "_" + str(jst_now).split(".")[0].split(" ")[1]
    time = time.replace(":", "_")
    return time


@click.command()
@click.option("--output-dir-path", "-o", default="{}/data".format(SCRIPT_DIR_PATH))
@click.option("--name-tag-mp4", "-o", default="ir_")
def main(output_dir_path, name_tag_mp4):
    rs_mng = RealSenseManager()  # default image size = (1280, 720)
    rs_mng.laser_turn_off()

    timestamp = get_time()
    output_mp4_path_left = str(Path(output_dir_path, name_tag_mp4 + timestamp + "_left.mp4"))
    output_mp4_path_right = str(Path(output_dir_path, name_tag_mp4 + timestamp + "_right.mp4"))
    print(output_mp4_path_left)

    image_width, image_height = rs_mng.image_size
    size = (image_width, image_height)
    fmt = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    frame_rate = 30.0
    writer_left = cv2.VideoWriter(output_mp4_path_left, fmt, frame_rate, size)
    writer_right = cv2.VideoWriter(output_mp4_path_right, fmt, frame_rate, size)

    writing_mode = False
    while True:
        key = cv2.waitKey(10)
        status = rs_mng.update()
        if status:
            ir_image_left = rs_mng.ir_frame_left
            ir_image_right = rs_mng.ir_frame_right
            ir_image_left_8uc3, ir_image_right_8uc3 = [
                gray2bgr(ir_image) for ir_image in [ir_image_left, ir_image_right]
            ]

            view_image = cv2.hconcat([ir_image_left_8uc3, ir_image_right_8uc3])

            if writing_mode:
                writer_left.write(ir_image_left_8uc3)
                writer_right.write(ir_image_right_8uc3)
                cv2.circle(view_image, (30, 30), 10, (0, 0, 255), -1)
            else:
                cv2.line(view_image, (20, 20), (20, 30), (0, 0, 255), 3)
                cv2.line(view_image, (30, 20), (30, 30), (0, 0, 255), 3)

            view_image = cv2.resize(view_image, None, fx=0.5, fy=0.5)
            cv2.imshow("IR-Left", view_image)
            if key & 0xFF == ord("s"):
                writing_mode = True
            if key & 0xFF == ord("x"):
                writing_mode = False
            if key & 0xFF == ord("q"):
                break

    writer_left.release()
    writer_right.release()

    cv2.destroyAllWindows()
    del rs_mng


if __name__ == "__main__":
    main()
