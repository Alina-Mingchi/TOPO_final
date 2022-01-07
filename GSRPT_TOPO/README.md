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


- get_upscaling_factor.py: function to get the scaling factor, this function gets the sizes of both the high resolution RGB image and the low resolution depth image. Then according to the options the user give, automatically get the scaling factor, and adjust the size of the RGB guide image accordingly. There are three options possible: 1)'center-crop': 
- bar_plot.ipynb
- Load_model.ipynb
- simple_geometry.ipynb
- test_hyperparam.ipynb
- test_implementation.ipynb
- test_ob_implementation.ipynb
- test_run_EPFL.ipynb
- test_run_EPFL_oblique.ipynb
- test_run_comballaz.ipynb



## Adjust the implementation in pytorch

```python
from get_upscaling_factor import get_factor
## define parameters through function
[factor,new_guide]= get_factor(guide_imgs,source_imgs,'center-crop','GSRPT')
```

