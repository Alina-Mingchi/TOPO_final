import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
import sys

from pix_transform.pix_transform_net import PixTransformNet

DEFAULT_PARAMS = {'greyscale': False,
                  'channels': -1,
                  'bicubic_input': False,
                  'spatial_features_input': True,
                  'weights_regularizer': [0.0001, 0.001, 0.001],  # spatial color head
                  'loss': 'l1',

                  'optim': 'adam',
                  'lr': 0.001,

                  'batch_size': 32,
                  'iteration': 1024 * 32,

                  'logstep': 512,
                  }

if 'ipykernel' in sys.modules:
    from tqdm import tqdm_notebook as tqdm
else:
    from tqdm import tqdm as tqdm


def PixTransform(source_img, guide_img, params=DEFAULT_PARAMS, target_img=None, path=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if len(guide_img.shape) < 3:
        guide_img = np.expand_dims(guide_img, 0)

    if params["channels"] > 0:
        guide_img = guide_img[0:params["channels"], :, :]

    if params['greyscale']:
        guide_img = np.mean(guide_img, axis=0, keepdims=True)

    n_channels, hr_height, hr_width = guide_img.shape

    source_img = source_img.squeeze()
    lr_height, lr_width = source_img.shape

    D = hr_height // lr_height
    M1 = lr_height
    N1 = hr_height
    M2 = lr_width
    N2 = hr_width

    # normalize guide and source
    guide_img = (guide_img - np.mean(guide_img, axis=(1, 2), keepdims=True)) / np.std(guide_img, axis=(1, 2),
                                                                                      keepdims=True)

    source_img_mean = np.mean(source_img)
    source_img_std = np.std(source_img)
    source_img = (source_img - source_img_mean) / source_img_std
    if target_img is not None:
        target_img = (target_img - source_img_mean) / source_img_std

    if params['spatial_features_input']:
        x = np.linspace(-0.5, 0.5, hr_height)
        y = np.linspace(-0.5, 0.5, hr_width)

        x_grid, y_grid = np.meshgrid(x, y, indexing='ij')

        x_grid = np.expand_dims(x_grid, axis=0)
        y_grid = np.expand_dims(y_grid, axis=0)

        guide_img = np.concatenate([guide_img, x_grid, y_grid], axis=0)


    #### prepare_patches #########################################################################
    # guide_patches is M^2 x C x D x D
    # source_pixels is M^2 x 1

    guide_img = torch.from_numpy(guide_img).float().to(device)
    source_img = torch.from_numpy(source_img).float().to(device)
    if target_img is not None:
        target_img = torch.from_numpy(target_img).float().to(device)

    guide_patches = torch.zeros((M1 * M2, guide_img.shape[0], D, D)).to(device)
    source_pixels = torch.zeros((M1 * M2, 1)).to(device)
    for i in range(0, M1):
        for j in range(0, M2):
            guide_patches[j + i * M2, :, :, :] = guide_img[:, i * D:(i + 1) * D, j * D:(j + 1) * D]
            source_pixels[j + i * M2] = source_img[i:(i + 1), j:(j + 1)]

    train_data = torch.utils.data.TensorDataset(guide_patches, source_pixels)
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=params['batch_size'], shuffle=True)
    ###############################################################################################

    #### setup network ############################################################################
    mynet = PixTransformNet(channels_in=guide_img.shape[0],
                            weights_regularizer=params['weights_regularizer']).train().to(device)
    optimizer = optim.Adam(mynet.params_with_regularizer, lr=params['lr'])
    if params['loss'] == 'mse':
        myloss = torch.nn.MSELoss()
    elif params['loss'] == 'l1':
        myloss = torch.nn.L1Loss()
    else:
        print("unknown loss!")
        return
    ###############################################################################################

    epochs = params["batch_size"] * params["iteration"] // (M1 * M2)
    mse_values = []
    mae_values = []
    with tqdm(range(0, epochs), leave=True) as tnr:
        # tnr.set_description("epoch {}".format(0))
        if target_img is not None:
            tnr.set_postfix(MSE=-1., consistency=-1.)
        else:
            
            tnr.set_postfix(consistency=-1.)
        for epoch in tnr:
            running_loss = 0.0
            loss_values = []
            
            for (x, y) in train_loader:
                optimizer.zero_grad()

                y_pred = mynet(x)
                y_mean_pred = torch.mean(y_pred, dim=[2, 3])

                source_patch_consistency = myloss(y_mean_pred, y)

                source_patch_consistency.backward()
                optimizer.step()
                
                running_loss += source_patch_consistency
                loss_values.append(source_patch_consistency.cpu().detach().numpy())

            if epoch % params['logstep'] == 0:
                with torch.no_grad():
                    mynet.eval()
                    predicted_target_img = mynet(guide_img.unsqueeze(0)).squeeze()
                    mse_predicted_target_img = -1.
                    if target_img is not None:
                        mse_predicted_target_img = F.mse_loss(source_img_std * predicted_target_img,
                                                              source_img_std * target_img)
                        mse_values.append(mse_predicted_target_img.cpu().detach().numpy())
                        
                        mae_predicted_target_img = myloss(source_img_std * predicted_target_img,
                                                              source_img_std * target_img)
                        mae_values.append(mae_predicted_target_img.cpu().detach().numpy())
                    
                    source_image_consistency = myloss(
                        source_img_std * F.avg_pool2d(predicted_target_img.unsqueeze(0), D),
                        source_img_std * source_img.unsqueeze(0))
                    if target_img is not None:
                        tnr.set_postfix(MSE=mse_predicted_target_img.item(),
                                        consistency=source_image_consistency.item())
                    else:
                        tnr.set_postfix(consistency=source_image_consistency.item())
                    mynet.train()
                    
        # plot evolution of the optimization loss and 
        # training loss if target_img is given
        loss_values_array = np.array(loss_values)
#         print(loss_values_array.shape)
#         print(loss_values_array)
        plt.figure()
        plt.plot(loss_values_array[0:len(loss_values_array):2])
        plt.title("loss during training according myloss parameter")

        mse_values_array = np.array(mse_values)
        print("----------MSE----------")
        print(mse_values_array.shape)
        print(mse_values_array)
        plt.figure()
        plt.plot(mse_values_array)
        plt.title("MSE loss, when target image is given")
        
        mae_values_array = np.array(mae_values)
        print("----------MAE----------")
        print(mae_values_array.shape)
        print(mae_values_array)
        plt.figure()
        plt.plot(mae_values_array)
        plt.title("MAE loss, when target image is given")
    
    # save the trained network
    if path != None:
        torch.save(mynet.state_dict(), path)
    
    # compute final prediction, un-normalize, and back to numpy
    mynet.eval()
    predicted_target_img = mynet(guide_img.unsqueeze(0)).squeeze()
    predicted_target_img = source_img_mean + source_img_std * predicted_target_img
    predicted_target_img = predicted_target_img.cpu().detach().squeeze().numpy()

    return predicted_target_img
