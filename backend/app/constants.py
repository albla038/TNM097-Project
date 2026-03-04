from reportlab.lib.pagesizes import A3, A4, A5

A_FORMAT = {
    "a3": {"scale_factor": 2, "page_size": A3},
    "a4": {"scale_factor": 1, "page_size": A4},
    "a5": {"scale_factor": 0.5, "page_size": A5},
}


FORMAT_KEYS = tuple(A_FORMAT.keys())
