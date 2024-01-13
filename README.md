# convopt4pcd

The functionality of each script should be clear by their name. Most of the scripts should be runnable as-is. Please feel free to contact us if you have any questions.

- `ransac`, `3ds_ransac`: implementation of RANSAC algorithm. `ransac` uses FPFH features, while `3ds_ransac` uses 3DSmoothNet features.
- `kabsch`: implementation of Kabsch algorithm.
- `sdrsac`: implementation of CVPR 2019 SDRSAC paper.
- Other scripts are for testing(e.g., `show_result`), format conversion(e.g., `ply2mat`, `salient2mat`, `feat2mat`), and exploration (e.g.,  `test_rotation`, `render_salient`) purposes.



necessary data files:

```
data
├─3ds-feature
│  ├─128dim
│  └─32dim
├─bunny-pcd
├─room-pcd
└─temple-pcd
```

