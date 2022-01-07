import numpy as np

def get_factor(guide_img, source_img, option,model):
    h_shape = guide_img.shape # high resolution shape
    l_shape = source_img.shape #low resolution shape
    
    l_w = l_shape[-1] #width
    l_h = l_shape[-2] #height
    if model == 'GSRPT':
        h_w = h_shape[-1]
        h_h = h_shape[-2]
    else:
        h_w = h_shape[-2]
        h_h = h_shape[-3]
        
    if option == 'center-crop':
        factor = np.min([h_w//l_w,h_h//l_h])
        guide_w = l_w * factor
        guide_h = l_h * factor
        rest_w = h_w - guide_w
        rest_h = h_h = guide_h
        if guide_img.ndim == 3:
            new_guide = guide_img[:,(rest_h//2):(rest_h//2 + h_h),(rest_w//2):(rest_w//2 + h_w)]
        elif guide_img.ndim == 4:
            new_guide = guide_img[:,:,(rest_h//2):(rest_h//2 + h_h),(rest_w//2):(rest_w//2 + h_w)]
        else:
            print('Error in guide image size')
    
    elif option == 'zero-pad':
        factor = np.max([h_w//l_w,h_h//l_h])
        half_h = (factor*l_h - h_h)//2
        half_w = (factor*l_w - h_w)//2
        if guide_img.ndim == 3:
            new_guide = np.zeros((h_shape[-3],factor*l_h,factor*l_w))
            for i in range(h_shape[-3]):
                new_guide[i] = np.pad(guide_img[i],((half_h,half_h),(half_w,half_w)),'constant',constant_values=((0, 0),(0,0)))
        elif guide_img.ndim == 4:
            new_guide = np.zeros((h_shape[-4],h_shape[-3],factor*l_h,factor*l_w))
            for j in range(h_shape[-4]):
                for i in range(h_shape[-3]):
                    new_guide[j,i,:,:] = np.pad(guide_img[j,i,:,:],((half_h,half_h),(half_w,half_w)),'constant',constant_values=((0, 0),(0,0)))
        else:
            print('Error in guide image size')

    elif option == 'mirror':
        factor = np.max([h_w//l_w,h_h//l_h])
        half_h = (factor*l_h - h_h)//2
        half_w = (factor*l_w - h_w)//2
        if guide_img.ndim == 3:
            new_guide = np.zeros((h_shape[-3],factor*l_h,factor*l_w))
            for i in range(h_shape[-3]):
                new_guide[i] = np.pad(guide_img[i],((half_h,half_h),(half_w,half_w)),'symmetric')
        elif guide_img.ndim == 4:
            new_guide = np.zeros((h_shape[-4],h_shape[-3],factor*l_h,factor*l_w))
            for j in range(h_shape[-4]):
                for i in range(h_shape[-3]):
                    new_guide[j,i,:,:] = np.pad(guide_img[j,i,:,:],((half_h,half_h),(half_w,half_w)),'symmetric')
        else:
            print('Error in guide image size')


    return factor, new_guide