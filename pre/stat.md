Parameters :    

| File name                                     | T1                    | T2                    |
| --------------------------------------------- | --------------------- | --------------------- |
| ![Mask_0.jpg](../pre/test_img/Mask_0.jpg)     | [M1](#model-1) Y 0.89 | [M1](#model-1) Y 0.61 |
| ![Mask_1.jpg](../pre/test_img/Mask_1.jpg)     | [M1](#model-1) Y 0.95 | [M1](#model-1) Y 0.73 |
| ![Mask_2.jpg](../pre/test_img/Mask_2.jpg)     | [M1](#model-1) Y 1.00 | [M1](#model-1) Y 1.00 |
| ![Mask_3.jpg](../pre/test_img/Mask_3.jpg)     | [M1](#model-1) Y 0.73 | [M1](#model-1) Y 0.75 |
| ![Mask_4.jpg](../pre/test_img/Mask_4.jpg)     | [M1](#model-1) Y 0.69 | [M1](#model-1) Y 1.00 |
| ![Mask_5.jpg](../pre/test_img/Mask_5.jpg)     | [M1](#model-1) Y 0.99 | [M1](#model-1) Y 0.92 |
| ![NoMask_0.jpg](../pre/test_img/NoMask_0.jpg) | [M1](#model-1) Y 0.91 | [M1](#model-1) Y 0.72 |
| ![NoMask_1.jpg](../pre/test_img/NoMask_1.jpg) | [M1](#model-1) N 0.85 | [M1](#model-1) N 0.98 |
| ![NoMask_2.jpg](../pre/test_img/NoMask_2.jpg) | [M1](#model-1) N 0.94 | [M1](#model-1) N 0.99 |
| ![NoMask_3.jpg](../pre/test_img/NoMask_3.jpg) | [M1](#model-1) N 0.90 | [M1](#model-1) N 0.90 |


# Model 1
Epochs : 20  
Model :  
data_augmentation,  
layers.Rescaling(1./255),  
layers.Conv2D(16, 3, padding='same', activation='relu'),  
layers.MaxPooling2D(),  
layers.Dropout(0.2),  
layers.Flatten(),  
layers.Dense(128, activation='relu'),  
layers.Dense(num_classes)  