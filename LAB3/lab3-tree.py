import math

import numpy
from sklearn import datasets
from sklearn.model_selection import train_test_split


class Node:
    def __init__(self, dimension, threshold, isLeaf, left, right, type_if_leaf):
        self.dimension, self.threshold, self.isLeaf, self.left, self.right, self.type_if_leaf = dimension, threshold, isLeaf, left, right, type_if_leaf


iris = datasets.load_iris()
iris_feature = iris['data']
iris_target = iris['target']
iris_target_name = iris['target_names']
numpy.random.seed(42)
feature_train, feature_test, target_train, target_test = train_test_split(iris_feature, iris_target, test_size=0.2)


def entropy(labels):
    entropy_ = 0
    for i in range(len(iris_target_name)):
        p = labels.tolist().count(i) / len(labels)
        if p != 0:
            entropy_ -= p * math.log(p, 2)
    return entropy_


def find_dim(feature, label):  # find best attr to split
    dim, th = 0, 0
    Gain_index_max = -math.inf
    for d in range(len(feature[1])):
        Gain_index, thre = get_gain_index_max(feature, label, d)
        if Gain_index > Gain_index_max:
            Gain_index_max = Gain_index
            dim = d
            th = thre
    return Gain_index_max, th, dim


def get_gain_index_max(feature_li, label_li, dim):
    """
    由于每个属性的值都是连续的，所以要先离散化，每个属性都二分化，每相邻两个值之间画一道线，
    这样会有好多分法，找出使该属性信息增益最大的划分阈值。
    获取某个属性类别的最大GainIndex（最大信息增益）
    :return: Gain_index(最大信息增益值)  threshold(对应划分阈值)
    """
    attr = feature_li[:, dim]
    Gain_index = -math.inf
    threshold = 0
    attr_sort = sorted(attr)
    candicate_thre = []
    # 寻找所有候选阈值，不重复
    for i in range(len(attr_sort) - 1):
        tmp = (attr_sort[i] + attr_sort[i + 1]) / 2
        if tmp not in candicate_thre and tmp != min(attr):
            # 当最小值有两个的时候第一道划分会把数据集划成有0个数据的结点和n个数据的另一个节点，这样的划分无意义，所以不计入候选划分
            candicate_thre.append(tmp)
    # find best gain_index
    for thre_tmp in candicate_thre:
        # 划分两类
        index_small_list = [index for index in range(len(feature_li)) if attr[index] < thre_tmp]
        label_small_tmp = label_li[index_small_list]
        index_large_list = [index for index in range(len(feature_li)) if attr[index] >= thre_tmp]
        label_large_tmp = label_li[index_large_list]

        Gain_index_tmp = entropy(label_li) - (len(label_small_tmp) * entropy(label_small_tmp)) / len(attr) - (
                entropy(label_large_tmp) * len(label_large_tmp)) / len(attr)
        # in LaTeX: Gain_index_tmp = H(D) - H(D|A) = H(D) - (|D1|/|D|)H(D1) - (|D2|/|D|)H(D2)
        if Gain_index_tmp > Gain_index:  # 找出最大信息增益，记录并返回
            Gain_index = Gain_index_tmp
            threshold = thre_tmp
    return Gain_index, threshold  # 已经选好了用于分类的属性，返回的是当前根节点的最大信息增益值和划分阈值


def devide_by_dimension_and_thre(feature_li, label_li, th, dim):
    """
    根据阈值和维度来划分数据集，返回两个树枝，小集和大集
    :returns: feature_small, label_small, feature_large, label_large
    """
    attr = feature_li[:, dim]
    index_small_list = [index for index in range(len(feature_li)) if attr[index] < th]
    feature_small = feature_li[index_small_list]
    label_small = label_li[index_small_list]
    index_large_list = [index for index in range(len(feature_li)) if attr[index] >= th]
    feature_large = feature_li[index_large_list]
    label_large = label_li[index_large_list]
    return feature_small, label_small, feature_large, label_large


def build_tree(feature, label):
    if len(label) > 1:
        Gain_index, threshold, dimension = find_dim(feature, label)
        if Gain_index == 0:  # Gain_index = 0，说明全都是同一种类型，就是叶节点
            return Node(dimension, threshold, True, None, None, label[0])
        else:
            # Gain_index != 0，说明还不纯，继续划分，递归构建左支和右支
            feature_small, label_small, feature_large, label_large = devide_by_dimension_and_thre(feature, label,
                                                                                                  threshold, dimension)
            left = build_tree(feature_small, label_small)
            right = build_tree(feature_large, label_large)
            return Node(dimension, threshold, False, left, right, None)
    else:
        # if only one sample, return leaf node
        return Node(None, None, True, None, None, label[0])


def predict(root: Node, feature_line):
    node = root
    while not node.isLeaf:
        if feature_line[node.dimension] < node.threshold:  # 按照决策树一层层往下走直到叶节点
            node = node.left
        else:
            node = node.right
    return node.type_if_leaf


def score(root, feature, label):
    list_predict = []
    correct = 0
    for index in range(len(feature)):
        type_ = predict(root, feature[index])
        list_predict.append(type_)
        if type_ == label[index]:
            correct += 1
    print('ACC: ', correct / len(feature))


result = build_tree(feature_train, target_train)
score(result, feature_test, target_test)
