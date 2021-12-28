#데이터 전처리

import numpy as np


from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import joblib
import pandas as pd

from numpy.linalg import norm

import statistics
import math
from math import sqrt
from sklearn.svm import SVC
import datetime

class preprocess:
    def delcolumns(self, X):
        X = X[:, :, :2]

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                for k in range(X.shape[2]):
                    if (round(X[i, j, k], 5) == 0):
                        X[i, j, k] = np.nan
        return X

    def get_vector(self, X, Y): #벡터 - 골격
        X = np.array(X)
        Y = np.array(Y)
        Z = X - Y
        return Z.tolist()

    def vector_joint(self, A):  # 벡터-관절
        get_vector = self.get_vector
        avlist = []
        for i in range(0, len(A)):
            vlist = []
            v1 = get_vector(A[i][6], A[i][5])
            v2 = get_vector(A[i][6], A[i][7])
            v3 = get_vector(A[i][3], A[i][2])
            v4 = get_vector(A[i][3], A[i][4])
            v5 = get_vector(A[i][13], A[i][12])
            v6 = get_vector(A[i][13], A[i][14])
            v7 = get_vector(A[i][10], A[i][9])
            v8 = get_vector(A[i][10], A[i][11])
            v9 = get_vector(A[i][5], A[i][1])
            v10 = get_vector(A[i][2], A[i][1])
            v11 = get_vector(A[i][12], A[i][8])
            v12 = get_vector(A[i][9], A[i][8])
            v13 = get_vector(A[i][1], A[i][0])
            vlist.extend(v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9 + v10 + v11 + v12 + v13)
            avlist.append(vlist)
        return avlist

    def norm_vec(self, X):  # 벡터 간 정규 벡터
        r_list = []
        for i in range(len(X)):
            x_list = []
            y_list = []
            for j in range(len(X[i])):
                x = X[i][j]
                if j % 2 == 0:
                    x_list.append(x)
                else:
                    y_list.append(x)
            t = x_list + y_list
            r_list.append(t)
        return r_list

    def preprocessing(self, keypoint):
        df = self.delcolumns(keypoint)
        vector = self.vector_joint(df)
        # print(vector)
        norm_vector = self.norm_vec(vector)
        # print(norm_vector)
        return norm_vector


class prediction(preprocess):
    def __init__(self, model):
        self.model = joblib.load(model)

    def qmean(self, num):
        return sqrt(sum(n * n for n in num) / len(num))

    def get_feature(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        Xn = 0
        up_X = X
        up_Y = Y
        Xn = 0
        for i in range(0, 13):
            if (np.isnan(X[i]) == True) or (np.isnan(Y[i]) == True):
                up_X = np.delete(up_X, i - Xn)
                up_Y = np.delete(up_Y, i - Xn)
                Xn = Xn + 1
        Yn = 0
        for j in range(13, 26):
            if (np.isnan(X[j]) == True) or (np.isnan(Y[j]) == True):
                up_X = np.delete(up_X, j - Yn - Xn)
                up_Y = np.delete(up_Y, j - Yn - Xn)
                Yn = Yn + 1
        # print(up_X)

        Xx_vec = up_X[:13 - Xn]
        Xy_vec = up_X[13 - Xn:26 - Xn - Yn]

        Yx_vec = up_Y[:13 - Xn]
        Yy_vec = up_Y[13 - Xn:26 - Xn - Yn]
        # print("Xx_vec: ",Xx_vec)
        # print("Xy_vec: ",Xy_vec)
        # print("Yx_vec: ",Yx_vec)
        # print("Yy_vec: ",Yy_vec)

        # Xx_vec 노말라이즈
        Xx_max, Xx_min = max(Xx_vec), min(Xx_vec)
        Xx_term = Xx_max - Xx_min
        Xy_max, Xy_min = max(Xy_vec), min(Xy_vec)
        Xy_term = Xy_max - Xy_min
        for i in range(len(Xx_vec)):
            if Xx_term != 0:
                Xx_vec[i] = (Xx_vec[i] - Xx_min) / Xx_term
        for j in range(len(Xy_vec)):
            if Xy_term != 0:
                Xy_vec[j] = (Xy_vec[j] - Xy_min) / Xy_term
        Yx_max, Yx_min = max(Yx_vec), min(Yx_vec)
        Yx_term = Yx_max - Yx_min
        Yy_max, Yy_min = max(Yy_vec), min(Yy_vec)
        Yy_term = Yy_max - Yy_min

        for i in range(len(Yx_vec)):
            if Yx_term != 0:
                Yx_vec[i] = (Yx_vec[i] - Yx_min) / Yx_term
        for j in range(len(Yy_vec)):
            if Yy_term != 0:
                Yy_vec[j] = (Yy_vec[j] - Yy_min) / Yy_term

        X_dis = Xx_vec - Yx_vec
        Y_dis = Xy_vec - Yy_vec

        Xvec_std = statistics.stdev(X_dis)
        Xvec_avg = statistics.mean(X_dis)
        Xvec_rms = self.qmean(X_dis)

        Yvec_std = statistics.stdev(Y_dis)
        Yvec_avg = statistics.mean(Y_dis)
        Yvec_rms = self.qmean(Y_dis)

        flist = [Xvec_std, Xvec_avg, Xvec_rms, Yvec_std, Yvec_std, Yvec_rms]

        #flist = [Xvec_std, Xvec_avg, Xvec_rms, Yvec_std, Yvec_avg, Yvec_rms]
        return flist

    def feature_list(self, preA, preB):
        features = []
        for i in range(0, len(preA)):
            flist = self.get_feature(preA[i], preB[i])
            # print(flist)
            features.append(flist)
        return features

    def score(self, keypoint_A, keypoint_B):    #model 안의 prediction으로 A와 B의 점수를 구함

        preA = super().preprocessing(keypoint_A)

        preB = super().preprocessing(keypoint_B)

        features = self.feature_list(preA, preB)

        score = self.model.predict_proba(features)
        return score