from scipy.io import loadmat
mat = loadmat(r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\docs\strain_fiber_rate_model3.mat")
for key in mat:
    print(key, type(mat[key]), mat[key].shape if hasattr(mat[key], "shape") else "")
