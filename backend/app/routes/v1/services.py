from fastapi import APIRouter

router = APIRouter()


@router.get("/services")
def get_services():

    return {

        "services": [

            {
                "title": "AI Engineering"
            },

            {
                "title": "Custom Software Development"
            },

            {
                "title": "Intelligent Automation"
            },

            {
                "title": "Data Intelligence & Analytics"
            }

        ]

    }