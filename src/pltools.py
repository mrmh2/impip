def load_pipeline_by_name(plname):
    pline = __import__(plname)
    return pline.create_pipeline()
