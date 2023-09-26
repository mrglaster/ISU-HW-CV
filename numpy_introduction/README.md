## Task I: Nominal Resolution

For given images (figure1-6), determine the nominal resolution (mm/pixel). Each image is recorded in a text file in the format:

```
    Максимальный размер объекта в миллиметрах по горизонтали
    #
    0 0 0
    0 0 0
    0 0 0
                                                
```

The image contains only the values ​​0 or 1. You can use the `open` or `np.loadtxt` function to read it.


## Task II: Define Shift 

Given two images img1 and img2. It is necessary to determine how much one image is offset relative to another (give the offset y, x). The data is presented in text format. The image contains only the values ​​0 or 1.


