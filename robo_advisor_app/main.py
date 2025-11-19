# all_agents/main.py
from fastapi import FastAPI

# Import all agent FastAPI apps
from .services.user_agent.main import app as user_app
from .services.model_agent.main import app as model_app
from .services.planner_agent.main import app as planner_app
from .services.orchestrator_agent.main import app as orch_app
from .services.data_agent.main import app as data_app

from .optimized_services.user_agent.main import app as opt_user_app
from .optimized_services.orchestrator_agent.main import app as opt_orch_app
from .optimized_services.planner_agent.main import app as opt_planner_app
from .optimized_services.model_agent.main import app as opt_model_app

app = FastAPI(title="All Agents Hosted Together")

# Mount each agent under its own path
app.mount("/user", user_app)
app.mount("/model", model_app)
app.mount("/planner", planner_app)
app.mount("/data", data_app)
app.mount("/orchestrator", orch_app)
app.mount("/optimized_user", opt_user_app)
app.mount("/optimized_model", opt_model_app)
app.mount("/optimized_planner", opt_planner_app)
app.mount("/optimized_orchestrator", opt_orch_app)

@app.get("/")
async def root():
    return {"message": "All agents are running"}
