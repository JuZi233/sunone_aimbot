from logic.config_watcher import *

try:
    from screeninfo import get_monitors
except:
    print('install screeninfo: pip install screeninfo')
    exit(0)

try:   
    import ultralytics
    from ultralytics import YOLO
except:
    print('install ultralytics: pip install ultralytics')
    exit(0)

if '.engine' in AI_model_path:
    import tensorrt

try:
    import numpy
except:
    print('install numpy: pip install numpy')
    exit(0)

if Dxcam_capture == True:
    try:
        import dxcam
    except:
        print('Install dxcam: pip install dxcam[cv2]')
        exit(0)

import importlib.metadata
import os

try:
    import cv2
    from cv2 import __version__
except:
    print('install cv2: pip install opencv-python \nor\npip install dxcam[cv2]')
    exit(0)

def run_checks():
    ultralytics.utils.checks.collect_system_info()

    cuda_support = ultralytics.utils.checks.cuda_is_available()
    if cuda_support == True:
        print('\nCuda support True')
    else:
        print('Cuda is not supported. Please reinstall pytorch with GPU support. https://pytorch.org/get-started/locally/\nIf you have reinstalled but there is no GPU support, Google how to solve this problem.')
        quit(0)

    print('OpenCV version: {0}'.format(__version__))

    if '.engine' in AI_model_path:
        print('TensorRT version: {0}'.format(tensorrt.__version__))
    if '.pt' in AI_model_path:
        print(ultralytics.YOLO('models/{}'.format(AI_model_path), task='detect').info())

    print('numpy version: {0}'.format(numpy.version.version))

    if Dxcam_capture:
        print('DXcam devices info:\n{0}'.format(dxcam.output_info()))
    # TODO: ADD OBS_CAPTURE CHECKS
    try:
        print('asyncio version: {0}'.format(importlib.metadata.version('asyncio')))
    except:
        print('Please install asyncio: pip install asyncio')

    print('\n********** Options **********\n')

    print('screen_width', detection_window_width)
    print('screen_height', detection_window_height, '\n')

    print('Dxcam_capture', Dxcam_capture)
    print('dxcam_capture_fps', dxcam_capture_fps)
    print('dxcam_monitor_id', dxcam_monitor_id)
    print('dxcam_gpu_id', dxcam_gpu_id)
    print('dxcam_max_buffer_len', dxcam_max_buffer_len, '\n')

    print('Obs_capture', Obs_capture)
    print('Obs_camera_id', Obs_camera_id)
    print('Obs_capture_fps', Obs_capture_fps, '\n')

    print('native_Windows_capture', native_Windows_capture, '\n')

    print('body_y_offset', body_y_offset)
    print('hideout_targets', hideout_targets, '\n')

    print('mouse_smoothing', mouse_smoothing)
    print('mouse_auto_shoot', mouse_auto_shoot)
    print('mouse_auto_aim', mouse_auto_aim)
    print('mouse_native', mouse_native)
    print('mouse_move_by_arduino', mouse_move_by_arduino)
    print('mouse_shoot_by_arduino', mouse_shoot_by_arduino, '\n')

    print('hotkey_targeting', hotkey_targeting)
    print('hotkey_exit', hotkey_exit)
    print('hotkey_pause', hotkey_pause, '\n')

    print('AI_model_path', AI_model_path)
    print('AI_image_size', AI_image_size)
    print('AI_conf', AI_conf)
    print('AI_iou', AI_iou)
    print('AI_device', AI_device)
    print('AI_max_det', AI_max_det, '\n')

    print('show_window', show_window)
    print('show_speed', show_speed)
    print('show_fps', show_fps)
    print('show_boxes', show_boxes)
    print('show_labels', show_labels)
    print('show_conf', show_conf)
    print('debug_window_scale_percent', debug_window_scale_percent)
    print('debug_window_name', debug_window_name, '\n')

    print('Environment variables:\n')
    for key, value in os.environ.items():
        if key == 'PATH':
            print('--------------------------- PATH ---------------------------')
            for i in value.split(';'):
                print(i)
            print('--------------------------- PATH ---------------------------')
        else:
            print(f'{key}: {value}')
    
    detection_test = detections_check()
    print(detection_test)

def detections_check():
    model = YOLO('models/{}'.format(AI_model_path), task='detect')
    cap = cv2.VideoCapture('media/tests/test_det.mp4')
    clss = []
    while cap.isOpened():
        success, frame = cap.read()

        if success:
            result = model(frame, stream=False, show=False, imgsz=AI_image_size, device=AI_device, verbose=False)
            for frame in result:
                clss.append(frame.boxes.cls)
            annotated_frame = result[0].plot()

            cv2.putText(annotated_frame, 'TEST 1234567890', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            
            cv2.imshow("ETECTION TEST", annotated_frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(clss) <= 0:
        return '\nDetection test: Failed'
    else:
        return '\nDetection test: Passed. Number of detections: {}'.format(len(clss))

if __name__ == "__main__":
    run_checks()