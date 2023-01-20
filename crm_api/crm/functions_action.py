from crm.schemas.resources.result_object import ResultObject

def action(*args):
    
    result = ResultObject()
    result.detail = 'Entre al action'
    
    return result