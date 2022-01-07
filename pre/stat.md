Parameters :    

| File name                                     | [Model 1](#model-1)                         | [Model 2](#model-2)                    |
| --------------------------------------------- | ------------------------------------------- | -------------------------------------- |
| ![Mask_0.jpg](../pre/test_img/Mask_0.jpg)     | Y 0.89 <br> Y 0.61 <br> __N 0.55__          | Y 0.63 <br> Y 0.61 <br> __N 0.56__     |
| ![Mask_1.jpg](../pre/test_img/Mask_1.jpg)     | Y 0.95 <br> Y 0.73 <br> Y 0.99              | Y 0.93 <br> Y 0.98 <br> Y 0.90         |
| ![Mask_2.jpg](../pre/test_img/Mask_2.jpg)     | Y 1.00 <br> Y 1.00 <br> Y 1.00              | Y 1.00 <br> Y 1.00 <br> Y 1.00         |
| ![Mask_3.jpg](../pre/test_img/Mask_3.jpg)     | Y 0.73 <br> Y 0.75 <br> __N 0.51__          | Y 0.85 <br> Y 0.89 <br> Y 0.86         |
| ![Mask_4.jpg](../pre/test_img/Mask_4.jpg)     | Y 0.69 <br> Y 1.00 <br> Y 1.00              | Y 0.99 <br> Y 0.58 <br> Y 0.95         |
| ![Mask_5.jpg](../pre/test_img/Mask_5.jpg)     | Y 0.99 <br> Y 0.92 <br> Y 0.99              | Y 0.94 <br> Y 0.94 <br> Y 0.87         |
| ![NoMask_0.jpg](../pre/test_img/NoMask_0.jpg) | __Y 0.91__ <br> __Y 0.72__  <br> __Y 0.95__ | __Y 0.62__ <br> __Y 0.84__ <br> N 0.55 |
| ![NoMask_1.jpg](../pre/test_img/NoMask_1.jpg) | N 0.85 <br> N 0.98 <br> N 0.99              | N 0.97 <br> N 0.91 <br> N 0.99         |
| ![NoMask_2.jpg](../pre/test_img/NoMask_2.jpg) | N 0.94 <br> N 0.99 <br> N 0.98              | N 1.00 <br> N 0.97 <br> N 0.98         |
| ![NoMask_3.jpg](../pre/test_img/NoMask_3.jpg) | N 0.90 <br> N 0.90 <br> N 0.98              | N 0.92 <br> N 0.62 <br> N 0.98         |


# Model 1
```py
model = keras.models.Sequential([
        data_augmentation,
        layers.Rescaling(1./255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])
```

# Model 2
```py
model = keras.models.Sequential([
        data_augmentation,
        layers.Rescaling(1./255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])
```