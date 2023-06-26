import casbin
import os 
current_directory = os.getcwd()
model_path = os.path.join(current_directory, "resource/model.conf")
policy_path = os.path.join(current_directory, "resource/policy.csv")
authrization = casbin.Enforcer(model_path, policy_path)