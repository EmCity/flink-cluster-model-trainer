import pandas as pd
#this script generates a new training set for trajectories/volume based on the training set from phase1 and the training set from phase2

#trajectories
training_files_traj = "../../../dataset/training/trajectories(table 5)_training.csv"
training_files__traj_2 = "../../../dataset/training2/trajectories(table_5)_training2.csv"
new_training_files_traj = "../../../new_dataset/training/trajectories(table 5)_training.csv"

#first dataset 109.244 + second dataset 10137 = combined dataset 119381x3
pd.concat([pd.DataFrame.from_csv(training_files_traj), pd.DataFrame.from_csv(training_files__traj_2)]).to_csv(new_training_files_traj)

#volume
training_files_volume = "../../../dataset/training/volume(table 6)_training.csv"
training_files_volume_2 = "../../../dataset/training2/volume(table 6)_training2.csv"
new_training_files_volume = "../../../new_dataset/training/volume(table 6)_training.csv"
#first dataset 543.700 + second dataset 128824 = combined dataset 672.524x6
pd.concat([pd.DataFrame.from_csv(training_files_volume), pd.DataFrame.from_csv(training_files_volume_2)]).to_csv(new_training_files_volume)
