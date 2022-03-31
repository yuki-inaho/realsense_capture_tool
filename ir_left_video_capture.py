import click
import cv2
from pathlib import Path
from scripts.realsense import RealSenseManager


SCRIPT_DIR_PATH = Path(__file__).resolve().parent


def gray2bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


@click.command()
@click.option("--output-mp4-path", "-o", default="{}/movie.mp4".format(SCRIPT_DIR_PATH))
def main(output_mp4_path):
    rs_mng = RealSenseManager()  # default image size = (1280, 720)
    rs_mng.laser_turn_off()

    image_width, image_height = rs_mng.image_size
    size = (image_width, image_height)
    fmt = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    frame_rate = 30.0
    writer = cv2.VideoWriter(output_mp4_path, fmt, frame_rate, size)

    writing_mode = False
    while True:
        key = cv2.waitKey(10)
        status = rs_mng.update()
        if status:
            ir_image_left = rs_mng.ir_frame_left
            ir_image_left_8uc3 = gray2bgr(ir_image_left)
            view_image = ir_image_left_8uc3
            if writing_mode:
                writer.write(ir_image_left_8uc3)
                cv2.circle(view_image, (30, 30), 10, (0, 0, 255), -1)
            else:
                cv2.line(view_image, (20, 20), (20, 30), (0, 0, 255), 3)
                cv2.line(view_image, (30, 20), (30, 30), (0, 0, 255), 3)

            cv2.imshow("IR-Left", view_image)
            if key & 0xFF == ord("s"):
                writing_mode = True
            if key & 0xFF == ord("x"):
                writing_mode = False
            if key & 0xFF == ord("q"):
                break
    writer.release()
    cv2.destroyAllWindows()
    del rs_mng


if __name__ == "__main__":
    main()
