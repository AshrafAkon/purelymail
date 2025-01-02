from purelymail import PurelymailAPI
import os
pma = PurelymailAPI(api_token=os.environ["PURELYMAIL_API_TOKEN"])
# print(pma.list_users())
# print(pma.list_routing_rules())
print(pma.check_account_credit())
