import numpy as np
from tqdm import tqdm

def event_agg(timestamp, x, y, polarity, T_r, M, N):  # t_r as time interval, M as length , N as width
    T_seq = timestamp.max()
    T_frames = int((T_seq // T_r)) + 1

    frames_0 = np.zeros((T_frames, M, N), )  # polarity == 0
    frames_1 = np.zeros((T_frames, M, N))  # polarity == 1

    for i in tqdm(range(T_frames)):
        idx_0 = np.where((timestamp >= i * T_r) & (timestamp < i * T_r + T_r) & (polarity == 0))[0]
        if len(idx_0) > 0:
            frames_0[i] = np.bincount(N * x[idx_0] + y[idx_0], minlength=M * N).reshape(M, N)

        idx_1 = np.where((timestamp >= i * T_r) & (timestamp < i * T_r + T_r) & (polarity == 1))[0]
        if len(idx_1) > 0:
            frames_1[i] = np.bincount(N * x[idx_1] + y[idx_1], minlength=M * N).reshape(M, N)

    superframes = np.concatenate((frames_0, frames_1), axis=-1)
    print('generated superframes with size:', superframes.shape)
    return superframes