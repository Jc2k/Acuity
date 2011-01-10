from twisted.application.service import ServiceMaker

Sample = ServiceMaker(
    "acuity",
    "acuity.server",
    "log server",
    "acuity"
    )
