from fastapi import APIRouter
from ..controllers.shinsas import ShinsaController

router = APIRouter(prefix="/shinsas", tags=["Shinsas"])

router.add_api_route("/", ShinsaController.get_filtered_shinsas, methods=["GET"])
