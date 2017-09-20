from __future__ import print_function

import os
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Conv2DTranspose, Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint,ReduceLROnPlateau,EarlyStopping,CSVLogger
from keras import backend as K
from keras.models import load_model

K.set_image_data_format('channels_last')  # TF dimension ordering in this code

img_rows = 128
img_cols = 128

smooth = 1.

# Change this flag if you want to start the training from scratch
reloadFlag = True

oldmodelwtsfname = 'short_weights_dil1x_4conn_cshpaper_normalize_dropout.h5'
modelwtsfname = 'short_weights_dil1x_4conn_cshpaper_normalize_dropout.h5'


def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)

def get_unet_short_dropout():
    inputs = Input((img_rows, img_cols, 1))
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = Dropout(0.2)(conv1) 
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Dropout(0.2)(conv2) 
    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Dropout(0.2)(conv3) 
    conv3 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv3)

    up3 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(conv3), conv2], axis=3)
    conv4 = Conv2D(128, (3, 3), activation='relu', padding='same')(up3)
    conv4 = Dropout(0.2)(conv4) 
    conv4 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv4)

    up4 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(conv2), conv1], axis=3)
    conv5 = Conv2D(64, (3, 3), activation='relu', padding='same')(up4)
    conv5 = Dropout(0.2)(conv5) 
    conv5 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv5)

    conv6 = Conv2D(1, (1, 1), activation='sigmoid')(conv5)

    model = Model(inputs=[inputs], outputs=[conv6])

    return model

def train():

    print('-'*30)
    print('Loading and preprocessing train data...')
    print('-'*30)

    imgs_train_fr = np.load('../input_data/FarRed_Annotated_FISH_Dilation4Conn1Iter_Training_128by128_normalize.npy')
    imgs_mask_train_fr = np.load('../input_data/FarRed_Annotated_FISH_Dilation4Conn1Iter_Training_128by128_normalize_Mask.npy')
    imgs_train_r = np.load('../input_data/Red_Annotated_FISH_Dilation4Conn1Iter_Training_128by128_normalize.npy')
    imgs_mask_train_r = np.load('../input_data/Red_Annotated_FISH_Dilation4Conn1Iter_Training_128by128_normalize_Mask.npy')
    imgs_train_g = np.load('../input_data/Annotated_FISH_Dilation4Conn1Iter_Training_128by128_normalize.npy')
    imgs_mask_train_g = np.load('../input_data/Green_Annotated_FISH_Dilation4Conn1Iter_Training_128by128_normalize_Mask.npy')

    # Let's merge them -- we have to make sure that both are of same shape in axis 1 and 2 (x, y) which isn't checked here.
    imgs_train = np.concatenate((imgs_train_fr, imgs_train_r, imgs_train_g), axis=0) 
    imgs_mask_train = np.concatenate((imgs_mask_train_fr, imgs_mask_train_r,imgs_mask_train_g), axis=0) 


    imgs_train = imgs_train.astype('float32')

    imgs_mask_train = imgs_mask_train.astype('float32')
    imgs_mask_train /= 255.  # scale masks to [0, 1]

    print('-'*30)
    print('Creating and compiling model...')
    print('-'*30)
    
    model = get_unet_short_dropout()
    model.compile(optimizer=Adam(lr=1e-5), loss=dice_coef_loss, metrics=[dice_coef])
    model.summary()

    # Loading previous weights for restarting
    if os.path.isfile(oldmodelwtsfname) and reloadFlag :
       print('-'*30)
       print('Loading previous weights ...')
       model.load_weights(oldmodelwtsfname)

    
    model_checkpoint = ModelCheckpoint(modelwtsfname, monitor='val_loss', save_best_only=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,patience=50, min_lr=0.001,verbose=1)
    model_es = EarlyStopping(monitor='val_loss', min_delta=0.00000001, patience=500, verbose=1, mode='auto')
    csv_logger = CSVLogger('short_weights_dil1x_4conn_cshpaper_normalize_dropout_training.log', append=True)

    print('-'*30)
    print('Fitting model...')
    print('-'*30)
    imgs_train = np.expand_dims(imgs_train, 3)
    imgs_mask_train = np.expand_dims(imgs_mask_train, 3)
    model.fit(imgs_train, imgs_mask_train, batch_size=2, epochs=5000, verbose=1, shuffle=True,
              validation_split=0.10, callbacks=[model_checkpoint, reduce_lr, model_es, csv_logger])

def predict():
    print('-'*30)
    print('Loading and preprocessing test data...')
    print('-'*30)

    imgs_test = np.load('../input_data/Green_Red_FarRed_Annotated_FISH_Dilation4Conn1Iter_Testing_128by128_normalize.npy')
    imgs_mask_test = np.load('../input_data/Green_Red_FarRed_Annotated_FISH_Dilation4Conn1Iter_Testing_128by128_normalize_Mask.npy')
    imgs_test = imgs_test.astype('float32')


    print('-'*30)
    print('Loading saved weights...')
    print('-'*30)

    model = get_unet_short_dropout()
    model.compile(optimizer=Adam(lr=1e-5), loss=dice_coef_loss, metrics=[dice_coef])
    model.summary()

    model.load_weights(modelwtsfname)

    print('-'*30)
    print('Predicting masks on test data...')
    print('-'*30)
    imgs_test = np.expand_dims(imgs_test,3)
    imgs_mask_test = model.predict(imgs_test, batch_size=256,verbose=1)
    np.save('../input_data/Green_Red_FarRed_Annotated_FISH_Dilation4Conn1Iter_Testing_128by128_normalize_dropout_Mask_Pred_cshpaper.npy', np.squeeze(imgs_mask_test))

if __name__ == '__main__':
    train()
    predict()
