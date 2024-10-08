from pmc_automation_tools.api.ux.datasource import (
    UXDataSource,
    UXDataSourceInput,
    UXDataSourceResponse
    )
from pmc_automation_tools.api.classic.datasource import (
    ClassicDataSource,
    ClassicDataSourceInput,
    ClassicDataSourceResponse
    )
from pmc_automation_tools.api.datasource import ApiDataSourceInput, ApiDataSource
import os
from pmc_automation_tools.driver.common import PlexDriver
from pmc_automation_tools.driver.ux.driver import UXDriver
from pmc_automation_tools.driver.classic.driver import ClassicDriver
from pmc_automation_tools.common.utils import create_batch_folder
from pmc_automation_tools.common.exceptions import UXResponseErrorLog
import logging

test = True
# api_key = open('pmc_automation_tools/resources/api', 'r').read()
# a = ApiDataSource(auth=api_key, test_db=test)
# url = 'https://connect.plex.com/mdm/v1/customers'
# method = 'get'
# ai = ApiDataSourceInput(url, method)
# ai.name = 'NISSAN MOTOR'
# ai.status = 'Active'
# r = a.call_data_source('79870', ai)
# cust_id = r.get_response_attribute('id')
# print(r)
ds_id = '338' # Role_Members_Get
ds_id = '287' # Customer_Group_Members_Inclusive_Get 
# ds_id = '9062' # PO_No_From_PO_Key_Get 
# ds_id = '149' # Parts_Get
ui = UXDataSourceInput(ds_id, template_folder='pmc_automation_tools/resources/templates')
ui.pop_inputs(keep=[])
# ui.PO_Key = 2883902
u = UXDataSource(auth='Grand Haven',pcn_config_file='pmc_automation_tools/resources/pcn_config.json')

# access = u.list_data_source_access(pcn='Grand Haven')
# access.save_csv('pmc_automation_tools/resources/all_access.csv')

try:
    r = u.call_data_source(ui)
except UXResponseErrorLog as e:
    print(e)
print(r)
# wsdl = os.path.join(os.getcwd(),'resources','Plex_SOAP_test.wsdl')
# c = ClassicDataSource(wsdl,auth='Grand Haven',test_db=test)
# ci = ClassicDataSourceInput(2145)
# ci.Part_No = '278780-20'
# ci.Active = '1'
# cr = c.call_data_source(ci)
# pa = ClassicDriver(debug=True,debug_level=logging.DEBUG,driver_type='edge')
pa = UXDriver(debug=True, debug_level=logging.DEBUG, driver_type='edge')
username = open('pmc_automation_tools/resources/username', 'r').read()
password = open('pmc_automation_tools/resources/password', 'r').read()
company = open('pmc_automation_tools/resources/company', 'r').read()
pa.login(username, password, company, '79870', test_db=True)
# pa.driver.get(f'{pa.url_comb}/Rendering_Engine/Default.aspx?Request=Show&RequestData=SourceType(Screen)SourceKey(5726)')
e = pa.wait_for_element(('name', 'PartNo'))
e.screenshot()
pa.wait_for_gears()
pa.click_button('Search')
pa.wait_for_gears()
create_batch_folder(test=True)

ai = ApiDataSourceInput('https://connect.plex.com/platform/custom-fields/vi/field-types/','get',json={'asdf':'asdf'})
ai.test_input = 'asdf'

ui.Test_input = 'asfd'
ui.foo = 'bar'
ui.Foo = 'Baz'





driver,urlcomb,token = pa.login()
pa.driver.get(f'{urlcomb}/Engineering/Part?__features=novirtual&{token}')
pa.wait_for_gears()
part_no = pa.wait_for_element(('name','PartNo'))
part_no.send_keys('278780-20')
part_no.send_keys('\n')
pa.wait_for_gears()
pa.debug_logger.debug('searched')
# pa._debug_print('asdfasdf',level=1)

pa.debug_logger.debug('top level debug')