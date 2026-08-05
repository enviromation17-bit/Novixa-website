from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/services",
    summary="List Services",
    description="Returns the list of AI engineering and software services offered by Novixa.",
    tags=["Services"]
)
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