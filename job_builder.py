import os
from nvflare.app_common.workflows.scatter_and_gather import ScatterAndGather
from nvflare.app_common.workflows.cross_site_model_eval import CrossSiteModelEval
from nvflare.app_common.aggregators.intime_accumulate_model_aggregator import InTimeAccumulateWeightedAggregator
from nvflare.app_common.widgets.intime_model_selector import IntimeModelSelector
from nvflare.app_opt.pt.file_model_persistor import PTFileModelPersistor
from nvflare.app_opt.pt.file_model_locator import PTFileModelLocator
from nvflare.app_common.widgets.validation_json_generator import ValidationJsonGenerator
from nvflare.app_common.executors.learner_executor import LearnerExecutor
from nvflare.job_config.fed_job_config import FedJobConfig
from nvflare.job_config.fed_app_config import FedAppConfig, ServerAppConfig, ClientAppConfig
from nvflare.app_common.shareablegenerators.full_model_shareable_generator import FullModelShareableGenerator
from pt.networks.nets import CustomModel
from pt.learners.custom_learner import CustomLearner
import json

project_name = str(input("Insert the project name:\n"))
project_sub_dir = str(input("Insert the project sub dir (e.g. 'prod_00'):\n"))

with open('./config/job_builder_setup.json', 'r') as f:
    config = json.load(f)

job_config = FedJobConfig(job_name=config['job_name'], min_clients=config['min_clients'])

NUM_ROUNDS = config['num_rounds']
AGGREGATION_EPOCHS = config['aggregation_epochs']
BATCH_SIZE = config['batch_size']
LR = config['learning_rate']

server_app = ServerAppConfig()
persistor = PTFileModelPersistor(model=CustomModel())
server_app.add_component("persistor", persistor)
server_app.add_component("shareable_generator", FullModelShareableGenerator())
server_app.add_component("aggregator", InTimeAccumulateWeightedAggregator(weigh_by_local_iter=False))
server_app.add_component("model_selector", IntimeModelSelector())
server_app.add_component("model_locator", PTFileModelLocator(pt_persistor_id="persistor"))
server_app.add_component("validation_json_generator", ValidationJsonGenerator())

scatter_and_gather = ScatterAndGather(
    min_clients=job_config.min_clients,
    num_rounds=NUM_ROUNDS,
    start_round=0,
    wait_time_after_min_received=60,
    train_task_name="train",
    aggregator_id="aggregator",
    persistor_id="persistor",
    shareable_generator_id="shareable_generator",
    train_timeout=3600,
    persist_every_n_rounds=1,
    snapshot_every_n_rounds=1,
)
server_app.add_workflow("scatter_and_gather", scatter_and_gather)

cross_site_eval = CrossSiteModelEval(
    model_locator_id="model_locator",
    submit_model_timeout=600,
    validation_timeout=6000,
    cleanup_models=False,
)
server_app.add_workflow("cross_site_model_eval", cross_site_eval)

client_app = ClientAppConfig()
custom_learner = CustomLearner(
    aggregation_epochs=AGGREGATION_EPOCHS,
    lr=LR,
    batch_size=BATCH_SIZE
)
client_app.add_component("custom_learner", custom_learner)

learner_executor = LearnerExecutor(learner_id="custom_learner")
client_app.add_executor(tasks=["train", "submit_model", "validate"], executor=learner_executor)

fed_app = FedAppConfig(server_app=server_app, client_app=client_app)
job_config.add_fed_app("app1", fed_app)
job_config.set_site_app("@ALL", "app1")

job_config.add_resource_spec("site-1", {"num_of_gpus": 1, "mem_per_gpu_in_GiB": 1})
job_config.add_resource_spec("site-2", {"num_of_gpus": 1, "mem_per_gpu_in_GiB": 1})

job_output_dir = os.path.join(os.getcwd(), "workspace", project_name, project_sub_dir, "admin@nvidia.com", "transfer", "jobs")
os.makedirs(job_output_dir, exist_ok=True)
job_config.generate_job_config(job_output_dir)

print(f"Job configuration generated in: {job_output_dir}")