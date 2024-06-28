def convert_to_int(viewer_str):
    viewer_str = viewer_str.split(" ")[0]
    viewer_str = viewer_str.replace(",", "").replace("명", "")
    
    if '천' in viewer_str:
        return int(float(viewer_str.replace('천', '')) * 1000)
    if '만' in viewer_str:
        return int(float(viewer_str.replace('만', '')) * 10000)
    
    return int(viewer_str)