# Plex Manufacturing Cloud (PMC) Automation Tools

This library serves two main functions.

1. Methods to log into PMC and automate tasks under a user's account.
    * Supports classic and UX.
    * This is basically a wrapper around Selenium with specific functions designed around how the PMC screens behave.

2. Methods for calling PMC data sources.
    * Classic SOAP data sources
    * UX REST data sources
    * Modern APIs (developer portal)

## Table of Contents
- [Plex Manufacturing Cloud (PMC) Automation Tools](#plex-manufacturing-cloud-pmc-automation-tools)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [PlexDriver Functions](#plexdriver-functions)
    - [wait\_for\_element](#wait_for_element)
    - [wait\_for\_gears](#wait_for_gears)
    - [wait\_for\_banner](#wait_for_banner)
    - [login](#login)
    - [token\_get](#token_get)
    - [pcn\_switch](#pcn_switch)
    - [click\_button](#click_button)
    - [click\_action\_bar\_item](#click_action_bar_item)
  - [Utilities](#utilities)
    - [create\_batch\_folder](#create_batch_folder)
    - [setup\_logger](#setup_logger)
  - [PlexElement Functions](#plexelement-functions)
    - [sync\_picker](#sync_picker)
    - [sync\_textbox](#sync_textbox)
    - [sync\_checkbox](#sync_checkbox)
    - [screenshot](#screenshot)
  - [Usage Examples](#usage-examples)
      - [Example 1](#example-1)
      - [Example 2](#example-2)
      - [Example 3](#example-3)

## Requirements

* Selenium
* pywin32
* Requests
* urllib3
* zeep

In order to make classic SOAP calls, you will also need the WSDL files from Plex. 

They do not expose their WSDL URL anymore, but the files are on the community.




## PlexDriver Functions

Sub classes `UXDriver` and `ClassicDriver`

Parameters
* driver_type - supports edge and chrome browsers
* debug_level - level of debugging for built in debug printing during operations

Debug commands are printed to stdout for the `PlexDriver` objects.

```python
from pmc_automation_tools import UXDriver, ClassicDriver
u = UXDriver(driver_type='edge')
c = ClassicDriver(driver_type='chrome')
```

### wait_for_element

Waits for until an element condition is met.

Parameters
* selector - Selenium tuple selector
* driver - WebDriver or WebElement as starting point for locating the element
* timeout - How long to wait until the condition is met
* type - What type of condition
    * Visible (default)
    * Invisible
    * Clickable
    * Exists (Don't wait at all, just retun a PlexElement object)
* ignore_exception - Don't raise an exception if the condition is not met.

Returns PlexElement object

```python 
checklist_box = pa.wait_for_element((By.NAME, 'ChecklistKey'), type=CLICKABLE)
```

### wait_for_gears

Waits for the visibiility and then invisibility of the "gears" gif that shows when pages load.

Parameters
* loading_timeout - How long to wait after the gears become visible. Default 10.

The loading gif doesn't always display for long enough to be detected.

If the gif is detected, then the wait for it to become invisible is longer and controlled by the parameter.

```python
pa.wait_for_gears(loading_timeout=30) # Maybe a report takes 20-30 seconds to run.
```

### wait_for_banner

Waits for the banner to appear after a record is updated or if there is an error.

Currently only supported in `UXDriver` class.

### login

Log in to Plex with the provided credentials.

Parameters
* username - PMC username
* password - PMC password
* company_code - PMC company code
* pcn - PCN number
    * Used to lookup the proper PCN to click in a classic login process.
* test_db - If true, log into the test database
* headless - Run the chrome/edge driver in headless mode.
    * Note: UX does not always behave as expected when using this option.

Returns
* driver - The webdriver that can be used with all the Selenium actions and PMC driver actions
* url_comb - The combined url to be used for direct URL navigation within PMC
    * Classic - https://www.plexonline.com/__SESSION_TOKEN__ | https://test.plexonline.com/__SESSION_TOKEN__
    * UX - https://cloud.plex.com | https://test.cloud.plex.com
* token - The current session token. Needed to retain the proper PCN and screen when navigating directly to URLs.
    * Classic - This is built into url_comb since it always comes directly after the domain
    * UX - This is held in a query search parameter, and must be generated after changing PCNs, or the system will navigate using your home PCN.

UX token is supplied with the full query format. __asid=############

Depending on where in the URL it is placed, should be manually prefixed with a ? or &

UX:
```python
pa = UXDriver(driver_type='edge')
driver, url_comb, token = pa.login(username, password, company_code, pcn, test_db=True)
pa.driver.get(f'{url_comb}/VisionPlex/Screen?__actionKey=6531&{token}&__features=novirtual')
```
Classic:
```python
pa = ClassicDriver(driver_type='edge')
driver, url_comb, token = pa.login(username, password, company_code, pcn, test_db=True)
pa.driver.get(f'{url_comb}/Modules/SystemAdministration/MenuSystem/MenuCustomer.aspx') # This is the PCN selection screen.
```

### token_get

Return the current session token from the URL.

This is needed in order to maintain the proper PCN when navigating between them.

Otherwise, the screens may revert back to your home PCN.

### pcn_switch

alias: switch_pcn

Switch to the PCN provided

Paramters
* PCN
    * PCN number for the destination PCN

For UX, the number itself is used to switch PCNs using a static URL: 
```python
pa = UXDriver(driver_type='edge')
driver, url_comb, token = pa.login(username, password, company_code, pcn, test_db=True)

pa.pcn_switch('######')
# Equivalent to: 
driver.get(f'{url_comb}/SignOn/Customer/######?{token}')
```

For classic, you will need to have a JSON file to associate the PCN number to the PCN name. 

This will be prompted with instructions to create it if missing.

### click_button

Clicks a button with the provided text.

Parameters
* button_text - Text to search for
* driver - root driver to start the search from. Can be used to click "Ok" buttons from within popups without clicking the main page's 'Ok' button by mistake.

### click_action_bar_item

Used to click an action bar item on UX screens.

Parameters
* item - Text for the action bar item to click
* sub_item - Text for the sub item if the item is for a drop-down action

If the screen is too small, or there are too many action bar items, the function will automatically check under the "More" drop-down list for the item.

## Utilities

### create_batch_folder

Create a batch folder, useful for recording transactions by run-date.

Parameters
* root - Root directory for where to create the batch folder
* batch_code - Provide your own batch code to be used instead of generating one. Overrides include_time parameter.
* include_time - Include the timestamp in the batch code.
* test - Test batches. Stored in a TEST directory.

Default format: YYYYmmdd

Format with include_time: YYYYmmdd_HHMM

### setup_logger

Setup a logging file.

Parameters
* name - logger name
* log_file - filename for the log file.
* file_format - "DAILY" | "MONTHLY" | "". Will be combined with the log_file filename provided.
* level - log level for the logger. logging module levels.
* formatter - logging formatter
* root_dir - root directory to store the log file

## PlexElement Functions

Plex specific wrappers around Selenium `WebElement` objects.

Standard Selenium functionality should be retained on these objects.

### sync_picker

Updates the picker element's content to match the provided value. Does nothing if the contents match.

Works for the magnifying style pickers and Select style drop-down lists.

- [ ] TODO: Add support for multi-picker value selection
- [ ] TODO: Add support for `ClassicDriver` object

### sync_textbox

Updates a textbox value to match the provided value.

### sync_checkbox

Updates a checkbox state to match the provided state.

### screenshot

Wrapper around Selenium's screenshot functionality.

Saves a screenshot of the element to the screenshots folder using the element's ID and name.

## Usage Examples

#### Example 1

Automate data entry into screens which do not support or have an upload, datasource, or API to make the updates.

This example demonstrates updating a container type's dimensions from a csv file.

```python

from pmc_automation_tools import UXDriver
import csv

csv_file = 'container_types.csv'
pa = UXDriver(driver_type='edge') # edge or chrome is supported
driver, url_comb, token = pa.login(username,password,company_code,pcn,test_db=True)
token = pa.pcn_switch(destination_pcn)
pa.driver.get(f'{url_comb}/VisionPlex/Screen?__actionKey=6531&{token}&__features=novirtual') # &__features=novirtual will stop the results grid from lazy loading.
pa.wait_for_gears()
pa.wait_for_element((By.NAME,'ContainerTypenew'))
pa.ux_click_button('Search')
pa.wait_for_gears()

with open(csv_file,'r',encoding='utf-8-sig') as f:
    c = csv.DictReader(f)
    for r in c:
        container_type = r['container_type']
        cube_width = r['cube_width']
        cube_height = r['cube_height']
        cube_length = r['cube_length']
        cube_unit = r['cube_unit']
        pa.wait_for_element((By.LINK_TEXT,container_type)).click()
        pa.wait_for_gears()
        pa.wait_for_element((By.NAME,'CubeLength')).sync_textbox(cube_length)
        pa.wait_for_element((By.NAME,'CubeWidth')).sync_textbox(cube_width)
        pa.wait_for_element((By.NAME,'CubeHeight')).sync_textbox(cube_height)
        pa.wait_for_element((By.NAME,'UnitKey')).sync_picker(cube_unit)
        pa.ux_click_button('Ok')
        pa.wait_for_banner()
        pa.wait_for_gears()
        pa.wait_for_element((By.NAME,'ContainerTypenew'))
        pa.wait_for_gears()
        pa.wait_for_banner()
```
#### Example 2

Call a UX datasource from a Plex SQL query.

This example demonstrates saving the SQL records to a file in a batch folder which can be referenced to prevent duplicate updates if running in the same batch.

This data source is also for updating a container's dimensions.

```python
from pmc_automation_tools import UXDataSourceInput, UXDataSource, save_update, read_update, setup_logger, create_batch_folder
in_file = 'plex_sql_report.csv'
ds_id = '2360'
pcn = '123456'
update_file = 'updated_records.json'
batch_folder = create_batch_folder(test=True)
logger = setup_logger('Container Updates',log_file='Container_Updates.log',root_dir=batch_folder,level=10) #level=logging.DEBUG
ux = UXDataSource(pcn, test_db=True)
updates = read_update(update_file)
with open(in_file,'r',encoding='utf-8-sig') as f: # use utf-8-sig if exporting a CSV from classic SDE
    c = csv.DictReader(f)
    for r in c:
        container_type = r['Container_Type']
        try:
            u = UXDataSourceInput(ds_id, template_folder='templates')
            u.pop_inputs(keep=[])
            for k,v in r.items():
                setattr(u,k,v)
            log_record = {k:v for k,v in vars(u).items() if not k.startswith('_')}
            u.pop_inputs('Container_Type')
            u.type_reconcile()
            u.purge_empty()
            if log_record in updates:
                continue
            r = ux.call_data_source(u)
            updates.append(log_record)
            logger.info(f'{pcn} - Datasource: {ds_id} - Container Type: {container_type} Updated.')
        except:
            logger.error(f'{pcn} - Datasource: {ds_id} - Container Type: {container_type} Failed to update.')
        finally:
            save_update(update_file, updates)
```
#### Example 3

Call a classic data source from a csv file row.

This demonstrates adding supplier cert records into a new PCN based on the current cert records in another PCN.

```python
from pmc_automation_tools import (
    ClassicDataSource,
    ClassicDataSourceInput,
    ClassicConnectionError,
    create_batch_folder,
    setup_logger,
    read_updated,
    save_updated
)
import csv
import os


batch_folder = create_batch_folder(test=True)
logger = setup_logger('Supplier Cert',log_file='certs_added.log',root_dir=batch_folder)
cert_updates_file = os.path.join(batch_folder,'cert_updates.json')
updated_records = read_updated(cert_updates_file)

input_file = 'cert_reference.csv'
pcn = 'PCN name'

wsdl = os.path.join('resources','Plex_SOAP_prod.wsdl')
pc = ClassicDataSource(auth=pcn,test_db=True,wsdl=wsdl)

with open(input_file,'r',encoding='utf-8-sig') as f:
    c = csv.DictReader(f)
    for r in c:
        try:
            ci = ClassicDataSourceInput(57073)
            supplier_code = r['Delete - Supplier Code'] # just for reference
            cert_name = r['Delete - Certification'] # just for reference
            ci.MP1_Supp_Cert_List_Key = r['Supplier_Cert_List_Key']
            ci.MP1_Begin_Date = r['Begin_Date']
            if not r['Begin_Date']: # Some certs possibly had no begin date in classic which is not allowed.
                logger.warning(f'{pcn} - {supplier_code} - {cert_name} : {r["Note"]} - Missing start date.')
                continue
            ci.MP1_Expiration_Date = r['Expiration_Date']
            ci.MP1_Note = r['Note']
            ci.MP1_Parent = r['Parent']
            ci.MP_Supplier_Cert_Key = r['Supplier_Cert_Key']
            ci.Cert_Supplier_No = r['Cert_Supplier_No']
            log_record = {k:v for k,v in vars(ci).items() if not k.startswith('_')}
            if log_record in updated_records:
                continue
            response = pc.call_data_source(ci)
            logger.info(f'{pcn} - {supplier_code} - {cert_name} - Added')
            updated_records.append(log_record)
        except ClassicConnectionError as e:
            logger.error(f'{pcn} - {supplier_code} - {cert_name} - Failed to be added - {str(e)}')
        finally:
            save_updated(cert_updates_file,updated_records)
```