#!venv/bin/python

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hsweb_1.settings")
django.setup()

# your imports, e.g. Django models
from locations.models import Store, District, Region, Division, DMA, DistrbutionCenter
from circuits.models import Circuit, CommunicationsType
from vendors.models import Vendor
from issues.models import CommunicationsIssue, WorkOn
from phones.models import (PhoneTag, PhoneType, PhoneLine, PhoneEquipment,
                            Carrier, Comment, BillingAccountNumber, LastAudit,
                            CordlessPhoneType, PhoneBilling
                            )
                            
                            
def add_locations():
    print('Creating DMA')
    dma = DMA()
    dma.dma_number = 5
    dma.save()
    
    print('Creating DC')
    dc = DistrbutionCenter()
    dc.dc_number = 25
    dc.dc_status = 'Open'
    dc.save()
    
    print('Creating Division')
    division = Division()
    division.division_number = 4
    division.division_status = 'Open'
    division.save()
    
    print('Creating Region')
    region = Region()
    region.region_number = 37
    region.region_status = 'Open'
    region.save()
    
    print('Creating District')
    district = District()
    district.district_number = 217
    district.district_status = 'Open'
    district.save()
    
    print ('Creating Store 2942')
    store = Store()
    store.store_number = 2924
    store.three_letter_code = 'PR2'
    store.system_name = 'A2942PR2'
    store.longitude = -120.68240700
    store.latitude = 35.6147300
    store.state = 'CA'
    store.district = district
    store.dma = dma
    store.dc = dc
    store.store_status = 'Open'
    store.save()
    
    print ('Creating Store 2583')
    store = Store()
    store.store_number = 2583
    store.three_letter_code = 'PR1'
    store.system_name = 'A2583PR1'
    store.longitude = -120.68240700
    store.latitude = 38.6147300
    store.state = 'CA'
    store.district = district
    store.dma = dma
    store.dc = dc
    store.store_status = 'Open'
    store.save()
    
def add_vendors():
    print('Creating Vendor 1')
    v1 = Vendor()
    v1.vendor_name = 'Verizon'
    v1.notes = 'Verizon'
    v1.save()
    
    print('Creating Vendor 2')
    v2 = Vendor()
    v2.vendor_name = 'CenturyLink'
    v2.notes = 'CenturyLink'
    v2.save()

def add_circuits():
    ct = CommunicationsType()
    ct.comm_type = 'Dynamic T1'
    ct.save()
    
    circuit = Circuit()
    circuit.store = 2942
    circuit.primary_vendor = 1
    circuit.primary_circuit_id = 'A1awr23'
    circuit.communications_type = 1
    circuit.circuit_type = 'P'
    circuit.save()

def add_phones():
    tag = PhoneTag()
    tag.tag = 'HG1'
    tag.description = 'Hunt Group 1'
    tag.save()
    
    line = PhoneLine()
    line.store = 2942
    line.line_number = 1
    line.phone_number = '5555555555'
    line.tag = 1
    line.phone_type = 'PTS'
    line.save()
    
    equipment = PhoneEquipment()
    equipment.phone_equipment = 'NES'
    equipment.save()
    
    phone_type = PhoneType()
    phone_type.phone_type = 'Toshiba'
    phone_type.save()
    
    carrier = Carrier()
    carrier.carrier_name = 1
    carrier.phone_number = '5555555555'
    carrier.email = 'test@verizon.com'
    carrier.save()
    
    comment = Comment()
    comment.store = 2942
    comment.note = 'Simple Test'
    comment.note_type = 'Site'
    comment.user = 1
    comment.save()
    
    account_number = BillingAccountNumber()
    account_number.account_number = 'A12414'
    account_number.description = 'Master'
    account_number.save()
    
    billing = PhoneBilling()
    billing.store = 2942
    billing.master_account_number = account_number
    billing.local_exchange_carrier_1 = carrier
    billing.local_exchange_carrier_2 = carrier
    billing.main_data_carrier = carrier
    billing.backup_data_carrier = carrier
    billing.phone_equipment = equipment
    billing.phone_equipment_purchased_from = carrier
    billing.phone_type_1 = phone_type
    billing.phone_type_2 = phone_type
    billing.stick = 'NA'
    billing.save()
    
def add_issues():
    issue = Store()
    issue.store = 2942
    issue.issue = 'B'
    issue.save()
    
    