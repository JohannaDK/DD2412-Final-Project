#!/bin/bash	

cd /home/johannakhodaverdian/DD2412-Final-Project/
export PYTHONPATH=$PWD
echo "!!Evaluating model!!"
python3 src/experiments/01_eval_models.py \
    --save_file_name WRN_CIFAR100_VTST_M=1.txt \
    --model_name_file evaluate_wrn_cifar100_vtst_m=1.txt \
    --num_samples 1
echo "!!Evaluation done!!"

