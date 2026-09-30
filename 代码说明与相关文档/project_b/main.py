import os
import sys
import conf
import dataSeeking as ds
import preTrainingModelApp as ptma
import dataPreProcessing as dpp
import modelApp as ma
import txtReader


def test():
    if conf.modelSelection == 'cnn':
        ma.CNNTesting()
    if conf.modelSelection == 'rnn':
        ma.RNNTesting()


if __name__ == '__main__':
    # 模式选择提示
    conf.logger.info('mode selected ? (y/n)')
    option = input()
    if option != 'y':
        sys.exit()
    conf.logger.info('mode {}'.format(conf.option))
    # dataSeeking
    if conf.option == 0:
        ds.seeking()
        sys.exit()
    # preTrainging
    if conf.option == 1:
        if conf.pinyinEmbed:
            ptma.preTraining()
        if not conf.pinyinEmbed:
            ptma.preTrainingExPinyin()
        sys.exit()
    # train
    if conf.option == 2:
        if conf.modelSelection == 0:
            ma.RNN080Training()
        if conf.modelSelection == 1:
            ma.CNNCommonTraining()
        if conf.modelSelection == 2:
            ma.CNN080Training()
        if conf.modelSelection == 3:
            ma.RNNCommonTraining()
        sys.exit()
    # test
    if conf.option == 3:
        if conf.modelSelection == 0:
            ma.RNN080Testing()
        if conf.modelSelection == 1:
            ma.CNNCommonTesting()
        if conf.modelSelection == 2:
            ma.CNN080Testing()
        if conf.modelSelection == 3:
            ma.RNNCommonTesting()
        sys.exit()
