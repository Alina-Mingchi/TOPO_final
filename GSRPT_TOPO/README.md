# Guided-Superesolution as Pixel-to-Pixel Transformation

## Hierarchy
- baselines: <br>
  function for implementing bicubic baseline approach.
- pix_transform: <br>
  the backbone of this model, and useful functions for the implementation of this model.
- prox_tv-3.30.dist-info: <br>
  essential library that I installed manually. But with different system, it is possible to directly include the library, then no need for this folder
- prox_tv: <br>
  essential library that I installed manually. But with different system, it is possible to directly include the library, then no need for this folder
- utils: <br>
  utility functions for plotting, and futher processing: downsampling, and aligning functions.


- get_upscaling_factor.py: <br>
  function to get the scaling factor, this function gets the sizes of both the high resolution RGB image and the low resolution depth image. Then according to the options the user give, automatically get the scaling factor, and adjust the size of the RGB guide image accordingly. There are three options possible: 
  1. 'center-crop': First center the RGB image, and crop, so that you get rid of the borders. In essence, with this method, you reduce the size of your input
  2. 'zero-pad': First center the RGB image, and pad the empty border regions with 0. In essence, with this method, you increase the size of your input.
  3. 'mirror': First center the RGB image, and pad the empty border regions with the reflection of the image itself. In essence, with this method, you increase the size of your input.
- bar_plot.ipynb: <br>
  To plot out the bars shown in the report.
- fine_plotting.ipynb: <br>
  Plot and save the images in high resolution for the report.
  
- simple_geometry.ipynb: <br>
  data preprocessing, training with different hyper-parameters, testing and fine plotting of this simple geometry dataset
  
- test_run_EPFL.ipynb: <br>
  training and testing with indicated upscaling factor (x8, x40, x90) for EPFL nadir
- test_run_EPFL_oblique.ipynb: <br>
  training and testing with indicated upscaling factor (x8, x40, x90) for EPFL oblique
- test_run_comballaz.ipynb: <br>
  training and testing with indicated upscaling factor (x8, x40, x90) for comballaz, both nadir and oblique in the same notebook



## Adjust the implementation in pytorch
Currently, in all of the notebooks, the upscaling factors have been preselected. However, with this function, it is possible for the user to get the factor automatically, with the corresponding cropped or padded input RGB guide images. The utilization of this function is shown below:

```python
from get_upscaling_factor import get_factor
## define parameters through function
[factor,new_guide]= get_factor(guide_imgs,source_imgs,'center-crop','GSRPT')
```
__guide_imgs__ could be either 3-dim or 4-dim, but with other dimension, you are going to see an error message. <br>
__source_imgs__ are mainly used to extract the low resolution size. <br>
__center-crop__ is one of the three options, the other two are __zero-pad__, and __mirror__. <br>
__GSRPT__ is the indication of GSRPT specific, since the placement of the channel is different from the other two models.

