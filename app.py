from Image import PIL
import base64 
from io import BytesIO
import demo
import imageio
######################################################
# imports for animate
from skimage.transform import resize
import torch
from skimage import img_as_ubyte
from skimage.transform import resize
######################################################
# all settings, exposed here for visibility
config_path = 'config/vox-256.yaml'
checkpoint_path = 'checkpoints/vox.pth.tar'
device = 'cuda'

######################################################
TODO = False
def decodeBase64Image(imageStr: str, name: str) -> PIL.Image:
    image = PIL.Image.open(BytesIO(base64.decodebytes(bytes(imageStr, "utf-8"))))
    print(f'Decoded image "{name}": {image.format} {image.width}x{image.height}')
    return image
def encodeBase64Image(image: PIL.Image, name: str) -> str:
    # https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
def init():
    '''
    creates the globals that will be used every call
    '''
    # CUDA_VISIBLE_DEVICES=0 python demo.py --config config/vox-256.yaml --checkpoint checkpoints/vox.pth.tar --source_image ./source.jpg --driving_video ./driving.mp4
    global model 
    '''
    config_path = 'config/vox-256.yaml'
    checkpoint_path = 'checkpoints/vox.pth.tar'
    device = 'cuda'
    '''
    # model = TODO
    global inpainting, kp_detector, dense_motion_network, avd_network
    inpainting, kp_detector, dense_motion_network, avd_network = demo.load_checkpoints(config_path = config_path, checkpoint_path = checkpoint_path, device = device)
    
def inference(all_inputs:dict) -> dict:
    '''
    takes in dict created from request json, outputs dict
    to be wrapped up into a response json
    '''
    global model
    assert 'image' in all_inputs, 'TODO: what to do if image is not there?'
    image = all_inputs.get("image", None)
    image = decodeBase64Image(image)
    if True and 'prod':
        global inpainting, kp_detector, dense_motion_network, avd_network
        with torch.inference_mode():
            video_base64 = wrapper_for_animate(image,
                            driving_video='./assets/driving.mp4',
                            device='cuda',
                            img_shape = (256,256),
                            inpainting = inpainting, 
                            kp_detector  = kp_detector, 
                            dense_motion_network  = dense_motion_network, 
                            avd_network = avd_network,
                            find_best_frame = False,
                            mode = ['standard', 'relative', 'avd'][1],
                            result_video='./result.mp4',
                            )
        #TODO: or storage to google bucket and send back the link?
        return {'result':video_base64}
    elif True and 'DEBUG: send back the original image':

        img_str = encodeBase64Image(image)
        return {'original_image':img_str}
#######################################################################
# wrapper for animate
#######################################################################

def wrapper_for_animate(source_image,
                        driving_video='./assets/driving.mp4',
                        device='cuda',
                        img_shape = (256,256),
                        inpainting = TODO, 
                        kp_detector  = TODO, 
                        dense_motion_network  = TODO, 
                        avd_network = TODO,
                        find_best_frame = False,
                        mode = ['standard', 'relative', 'avd'][1],
                        result_video='./result.mp4',
                        ):
    # source_image = imageio.imread(opt.source_image)
    reader = imageio.get_reader(driving_video)
    fps = reader.get_meta_data()['fps']
    driving_video = []
    try:
        for im in reader:
            driving_video.append(im)
    except RuntimeError:
        pass
    reader.close()
    

    device = torch.device(device)
    
    source_image = resize(source_image, img_shape)[..., :3]
    driving_video = [resize(frame, img_shape)[..., :3] for frame in driving_video]

 
    if find_best_frame:
        i = demo.find_best_frame(source_image, driving_video, False)
        print ("Best frame: " + str(i))
        driving_forward = driving_video[i:]
        driving_backward = driving_video[:(i+1)][::-1]
        predictions_forward = demo.make_animation(source_image, driving_forward, inpainting, kp_detector, dense_motion_network, avd_network, device = device, mode = mode)
        predictions_backward = demo.make_animation(source_image, driving_backward, inpainting, kp_detector, dense_motion_network, avd_network, device = device, mode = mode)
        predictions = predictions_backward[::-1] + predictions_forward[1:]
    else:
        predictions = demo.make_animation(source_image, driving_video, inpainting, kp_detector, dense_motion_network, avd_network, device = device, mode = mode)
    if False:
        #TODO: dont save the video, return the video
        imageio.mimsave(result_video, [img_as_ubyte(frame) for frame in predictions], fps=fps)    
    else:
        # with tempfile.TemporaryFile(mode='w+b') as f:
        import tempfile
        temp_name = next(tempfile._get_candidate_names())
        temp_name = temp_name + +'.mp4'
        imageio.mimsave(temp_name, [img_as_ubyte(frame) for frame in predictions], fps=fps)    
        # imageio.mimread(temp_name)
        # https://stackoverflow.com/questions/56248567/how-do-i-decode-encode-a-video-to-a-text-file-and-then-back-to-video
        with open(temp_name, "rb") as videoFile:
            video_base64 =  base64.b64encode(videoFile.read())
        return video_base64
