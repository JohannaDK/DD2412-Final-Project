#!/bin/bash	

cd /home/ericbanzuzi/DD2412-Final-Project/
export PYTHONPATH=$PWD
echo "!!Evaluating model!!"
python3 src/experiments/01_eval_models.py \
    --save_file_name WRN_FL_TS.txt \
    --model_name_file evaluate_wrn_fl.txt \
    --temperature_scale
echo "!!Evaluation done!!"