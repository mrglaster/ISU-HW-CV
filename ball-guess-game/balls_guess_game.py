import cv2

CAM_ID = 0
CAM_W_NAME = 'Camera'
BG_W_NAME = 'Background'
ROI_W_NAME = 'ROI'
RESULT_W_NAME = 'RESULT'
AREA_LIMIT = 5000
pos = (0, 0)
blue_ball_lower = (90, 150, 130)
blue_ball_upper = (115, 255, 255)

yellow_ball_lower = (20, 200, 130)
yellow_ball_upper = (30, 250, 160)

green_ball_upper = (80, 180, 130)
green_ball_lower = (50, 160, 60)

red_ball_lower = (170, 220, 80)
red_ball_upper = (190, 230, 150)

current_rule = 'bygr'
rule = 'VERTICAL'


def get_ball(frame, hsv, lower_border, upper_border, color):
    mask = cv2.inRange(hsv, lower_border, upper_border)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        m = cv2.moments(c)
        center = int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])
        if r > 10:
            cv2.circle(frame, (int(x), int(y)), int(r), color, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color, 2)
            return int(x), int(y), int(r), center
    return None, None, None, None


def ball_observer():
    epsilon = 50
    capture = cv2.VideoCapture(CAM_ID)

    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)

    cv2.namedWindow(CAM_W_NAME)
    cv2.namedWindow(BG_W_NAME)

    while capture.isOpened():
        ret, frame = capture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        xb, yb, rb, cb = get_ball(frame, hsv, blue_ball_lower, blue_ball_upper, (255, 0, 0))
        xy, yy, ry, cy = get_ball(frame, hsv, yellow_ball_lower, yellow_ball_upper, (0, 255, 255))
        xg, yg, rg, cg = get_ball(frame, hsv, green_ball_lower, green_ball_upper, (0, 255, 0))
        xr, yr, rr, cr = get_ball(frame, hsv, red_ball_lower, red_ball_upper, (0, 0, 255))
        if xb is not None and xy is not None and xg is not None and xr is not None:
            colors_dict = {'r': cr, 'g': cg, 'b': cb, 'y': cy}
            if colors_dict[current_rule[0]][0] < colors_dict[current_rule[1]][0] and abs(
                    colors_dict[current_rule[0]][1] - colors_dict[current_rule[1]][1]) <= epsilon:
                if colors_dict[current_rule[2]][0] < colors_dict[current_rule[3]][0] and abs(
                        colors_dict[current_rule[2]][1] - colors_dict[current_rule[3]][1]) <= epsilon:
                    cv2.putText(frame, "YOU WON! YAY!", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                else:
                    cv2.putText(frame, "Incorrect! Try again!", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
            else:
                cv2.putText(frame, "Incorrect! Try again!", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        else:
            cv2.putText(frame, "I don't see all the balls!", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

        cv2.imshow(CAM_W_NAME, frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('й'):
            break

    capture.release()
    cv2.destroyAllWindows()


def main():
    ball_observer()


if __name__ == '__main__':
    main()
